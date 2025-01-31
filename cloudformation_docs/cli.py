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

def get_conditions(template):
    conditions = template.get('Conditions')
    if not conditions:
        conditions = template.get('conditions')
    if not conditions:
        conditions = []
    return conditions

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

TEMPLATE = """CloudFormation Template: {{ name }}

# {{ name }}

# Description
{{ description }}

# Parameters

The list of parameters for this template:

| Parameter Name | Type |
| -------------- | ----- |
{% for parameter in parameters %}| {{ parameter }} | {{ parameters[parameter].Type }} |
{% else %}No Parameters defined in template{% endfor %}

## Parameter Breakdown
The following sections outlines the parameter definitions for this template:
{% for parameter in parameters %}

### {{ parameter }} 
{% if parameters[parameter].Description %}Description: {{ parameters[parameter].Description}}{% endif %} 

Type: {{ parameters[parameter].Type }} 

{% if parameters[parameter].Default %}Default: {{ parameters[parameter].Default}}{% endif %} 

{% endfor %}

# Conditions
The following conditions form part of this template:

| Condition Name |
| -------------- |
{% for condition in conditions %}| {{ condition }} |
{% else %}No Conditions defined in template{% endfor %}


# Resources
The following resources form part of this template:

| Resource Name | Type |
| -------------- | ----- |
{% for resource in resources %}| {{ resource }} | {{ resources[resource].Type }} | 
{% else %}No Resources defined in template{% endfor %}

## Resource Definitions
The following sections breaks down each resource and their properties:

{% for resource in resources %}
### {{ resource }} Resource

#### Resource Type
{{ resources[resource].Type }}

#### Description
{% if resources[resource].Description %}{{ resources[resource].Description}}{% endif %}

#### DependsOn
{% if resources[resource].DependsOn %}{{ resources[resource].DependsOn}}{% endif %}

#### Condition
{% if resources[resource].Condition %}{{ resources[resource].Condition}}{% endif %}

#### Properties:
| Property Name | Value |
| -------------- | ----- |
{% for property in resources[resource].Properties %}| {{ property }} | {{ resources[resource].Properties[property] }} |
{% else %}No Properties defined{% endfor %}
{% else %}No Resources defined in template{% endfor %}

# Outputs
The list of outputs this template exposes are:

| Output Name | Description | Export name | Value |
| ------------ | ----------- | ----------- | ----- |
{% for output in outputs %}| {{ output }} | {% if outputs[output].Description %}{{ outputs[output].Description}}{% endif %} | {% if outputs[output].Export %}{% if outputs[output].Export.Name %}{{ outputs[output].Export.Name }} {% else %} Not Defined {% endif %}{% endif %} | {{ outputs[output].Value }}
{% else %}No Outputs defined in template{% endfor %}
"""
@click.command()
@click.argument('f', type=click.File())
def generate(f):
    extension = f.name.split(".").pop()
    if extension in ["yaml", "yml"]:
        j = to_json(f)
        template = json.loads(j)
    elif extension in ["json"]:
        j = f
        template = json.load(j)
    else:
        raise Exception("{}: not a valid file extension".format(extension))
    description = get_description(template)
    parameters = get_parameters(template)
    conditions = get_conditions(template)
    resources = get_resources(template)
    outputs = get_outputs(template)
    click.echo(Template(TEMPLATE).render(
        name = f.name.split('\\')[-1:][0],
        description=description,
        parameters=parameters,
        conditions=conditions,
        resources=resources,
        outputs=outputs,
    ))

if __name__ == "__main__":
    generate()