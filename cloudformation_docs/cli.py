import click
import json
import logging
from cfn_flip import to_json

from jinja2 import Template

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_parameters(template):
    params = template.get('Parameters')
    if not params:
        params = template.get('parameters')
    if not params:
        params = []
    return params


def get_resources(template):
    resources = template.get('Resources')
    if not resources:
        resources = template.get('resources')
    if not resources:
        resources = []
    return resources


def get_outputs(template):
    outputs = template.get('Outputs')
    if not outputs:
        outputs = template.get('outputs')
    if not outputs:
        outputs = []
    return outputs


def get_description(template):
    description = template.get("Description")
    if not description:
        description = template.get('description')
    if not description:
        description = "No Template description set"
    return description

TEMPLATE = """# {{ name }}
# Description
{{ description }}

## Parameters
The list of parameters for this template:
{% for parameter in parameters %}
### {{ parameter }} 
Type: {{ parameters[parameter].Type }} {% if parameters[parameter].Default %}
Default: {{ parameters[parameter].Default}}{% endif %} {% if parameters[parameter].Description %}
Description: {{ parameters[parameter].Description}}{% endif %} {% endfor %}

## Resource List
The following resources form part of this template:
{% for resource in resources %}
- {{ resource }} {% endfor %}

## Resource Definitions
The following sections breaks down each resource and their properties.
{% for resource in resources %}
### {{ resource }} Resource
#### Resource Type
{{ resources[resource].Type }}{% if resources[resource].Description %}
#### Description
{{ resources[resource].Description}}{% endif %} 
#### Properties:
| Property Name | Value |
| -------------- | ----- |{% for property in resources[resource].Properties %}
| {{ property }} | {{ resources[resource].Properties[property] }} |{% endfor %}
{% endfor %}

## Outputs
The list of outputs this template exposes:
| Output Name | Description | Export name |
| ------------| ----------- | ----------- |{% for output in outputs %}
|{{ output }}|{% if outputs[output].Description %}{{ outputs[output].Description}}{% endif %}|{% if outputs[output].Export.Name %}{{ outputs[output].Export.Name }}|{% endif %}{% endfor %}
"""
@click.command()
@click.argument('f', type=click.File())
def generate(f):
    extension = f.name.split(".").pop()
    if extension in ["yaml", "yml"]:
        j = to_json(f)
    elif extension in ["json"]:
        j = f
    else:
        raise Exception("{}: not a valid file extension".format(extension))
    template = json.loads(j)
    description = get_description(template)
    parameters = get_parameters(template)
    resources = get_resources(template)
    outputs = get_outputs(template)
    click.echo(Template(TEMPLATE).render(
        name = f.name.split('\\')[-1:][0],
        description=description,
        parameters=parameters,
        resources=resources,
        outputs=outputs,
    ))

if __name__ == "__main__":
    generate()