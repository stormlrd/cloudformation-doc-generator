CloudFormation Template: test.yaml

# test.yaml

# Description
A stack for deploying containerized applications in AWS Fargate. This stack runs containers in a public VPC subnet, and includes a public facing load balancer to register the services in.

# Parameters

The list of parameters for this template:

| Parameter Name | Type |
| -------------- | ----- |
No Parameters defined in template

## Parameter Breakdown
The following sections outlines the parameter definitions for this template:
No Parameters defined in template

# Resources
The following resources form part of this template:

| Resource Name | Type |
| -------------- | ----- |
| VPC | AWS::EC2::VPC | 
| PublicSubnetOne | AWS::EC2::Subnet | 
| PublicSubnetTwo | AWS::EC2::Subnet | 
| InternetGateway | AWS::EC2::InternetGateway | 
| GatewayAttachement | AWS::EC2::VPCGatewayAttachment | 
| PublicRouteTable | AWS::EC2::RouteTable | 
| PublicRoute | AWS::EC2::Route | 
| PublicSubnetOneRouteTableAssociation | AWS::EC2::SubnetRouteTableAssociation | 
| PublicSubnetTwoRouteTableAssociation | AWS::EC2::SubnetRouteTableAssociation | 
| ECSCluster | AWS::ECS::Cluster | 
| FargateContainerSecurityGroup | AWS::EC2::SecurityGroup | 
| EcsSecurityGroupIngressFromPublicALB | AWS::EC2::SecurityGroupIngress | 
| EcsSecurityGroupIngressFromSelf | AWS::EC2::SecurityGroupIngress | 
| PublicLoadBalancerSG | AWS::EC2::SecurityGroup | 
| PublicLoadBalancer | AWS::ElasticLoadBalancingV2::LoadBalancer | 
| DummyTargetGroupPublic | AWS::ElasticLoadBalancingV2::TargetGroup | 
| PublicLoadBalancerListener | AWS::ElasticLoadBalancingV2::Listener | 
| ECSRole | AWS::IAM::Role | 
| ECSTaskExecutionRole | AWS::IAM::Role | 


## Resource Definitions
The following sections breaks down each resource and their properties:


### VPC Resource

#### Resource Type
AWS::EC2::VPC

#### Properties:
| Property Name | Value |
| -------------- | ----- |
| EnableDnsSupport | True || EnableDnsHostnames | True || CidrBlock | {'Fn::FindInMap': ['SubnetConfig', 'VPC', 'CIDR']} |

### PublicSubnetOne Resource

#### Resource Type
AWS::EC2::Subnet

#### Properties:
| Property Name | Value |
| -------------- | ----- |
| AvailabilityZone | {'Fn::Select': [0, {'Fn::GetAZs': {'Ref': 'AWS::Region'}}]} || VpcId | {'Ref': 'VPC'} || CidrBlock | {'Fn::FindInMap': ['SubnetConfig', 'PublicOne', 'CIDR']} || MapPublicIpOnLaunch | True |

### PublicSubnetTwo Resource

#### Resource Type
AWS::EC2::Subnet

#### Properties:
| Property Name | Value |
| -------------- | ----- |
| AvailabilityZone | {'Fn::Select': [1, {'Fn::GetAZs': {'Ref': 'AWS::Region'}}]} || VpcId | {'Ref': 'VPC'} || CidrBlock | {'Fn::FindInMap': ['SubnetConfig', 'PublicTwo', 'CIDR']} || MapPublicIpOnLaunch | True |

### InternetGateway Resource

#### Resource Type
AWS::EC2::InternetGateway

#### Properties:
| Property Name | Value |
| -------------- | ----- |
No Properties defined

### GatewayAttachement Resource

#### Resource Type
AWS::EC2::VPCGatewayAttachment

#### Properties:
| Property Name | Value |
| -------------- | ----- |
| VpcId | {'Ref': 'VPC'} || InternetGatewayId | {'Ref': 'InternetGateway'} |

### PublicRouteTable Resource

#### Resource Type
AWS::EC2::RouteTable

#### Properties:
| Property Name | Value |
| -------------- | ----- |
| VpcId | {'Ref': 'VPC'} |

### PublicRoute Resource

#### Resource Type
AWS::EC2::Route

#### Properties:
| Property Name | Value |
| -------------- | ----- |
| RouteTableId | {'Ref': 'PublicRouteTable'} || DestinationCidrBlock | 0.0.0.0/0 || GatewayId | {'Ref': 'InternetGateway'} |

### PublicSubnetOneRouteTableAssociation Resource

#### Resource Type
AWS::EC2::SubnetRouteTableAssociation

#### Properties:
| Property Name | Value |
| -------------- | ----- |
| SubnetId | {'Ref': 'PublicSubnetOne'} || RouteTableId | {'Ref': 'PublicRouteTable'} |

### PublicSubnetTwoRouteTableAssociation Resource

#### Resource Type
AWS::EC2::SubnetRouteTableAssociation

#### Properties:
| Property Name | Value |
| -------------- | ----- |
| SubnetId | {'Ref': 'PublicSubnetTwo'} || RouteTableId | {'Ref': 'PublicRouteTable'} |

### ECSCluster Resource

#### Resource Type
AWS::ECS::Cluster

#### Properties:
| Property Name | Value |
| -------------- | ----- |
No Properties defined

### FargateContainerSecurityGroup Resource

#### Resource Type
AWS::EC2::SecurityGroup

#### Properties:
| Property Name | Value |
| -------------- | ----- |
| GroupDescription | Access to the Fargate containers || VpcId | {'Ref': 'VPC'} |

### EcsSecurityGroupIngressFromPublicALB Resource

#### Resource Type
AWS::EC2::SecurityGroupIngress

#### Properties:
| Property Name | Value |
| -------------- | ----- |
| Description | Ingress from the public ALB || GroupId | {'Ref': 'FargateContainerSecurityGroup'} || IpProtocol | -1 || SourceSecurityGroupId | {'Ref': 'PublicLoadBalancerSG'} |

### EcsSecurityGroupIngressFromSelf Resource

#### Resource Type
AWS::EC2::SecurityGroupIngress

#### Properties:
| Property Name | Value |
| -------------- | ----- |
| Description | Ingress from other containers in the same security group || GroupId | {'Ref': 'FargateContainerSecurityGroup'} || IpProtocol | -1 || SourceSecurityGroupId | {'Ref': 'FargateContainerSecurityGroup'} |

### PublicLoadBalancerSG Resource

#### Resource Type
AWS::EC2::SecurityGroup

#### Properties:
| Property Name | Value |
| -------------- | ----- |
| GroupDescription | Access to the public facing load balancer || VpcId | {'Ref': 'VPC'} || SecurityGroupIngress | [{'CidrIp': '0.0.0.0/0', 'IpProtocol': -1}] |

### PublicLoadBalancer Resource

#### Resource Type
AWS::ElasticLoadBalancingV2::LoadBalancer

#### Properties:
| Property Name | Value |
| -------------- | ----- |
| Scheme | internet-facing || LoadBalancerAttributes | [{'Key': 'idle_timeout.timeout_seconds', 'Value': '30'}] || Subnets | [{'Ref': 'PublicSubnetOne'}, {'Ref': 'PublicSubnetTwo'}] || SecurityGroups | [{'Ref': 'PublicLoadBalancerSG'}] |

### DummyTargetGroupPublic Resource

#### Resource Type
AWS::ElasticLoadBalancingV2::TargetGroup

#### Properties:
| Property Name | Value |
| -------------- | ----- |
| HealthCheckIntervalSeconds | 6 || HealthCheckPath | / || HealthCheckProtocol | HTTP || HealthCheckTimeoutSeconds | 5 || HealthyThresholdCount | 2 || Name | {'Fn::Join': ['-', [{'Ref': 'AWS::StackName'}, 'drop-1']]} || Port | 80 || Protocol | HTTP || UnhealthyThresholdCount | 2 || VpcId | {'Ref': 'VPC'} |

### PublicLoadBalancerListener Resource

#### Resource Type
AWS::ElasticLoadBalancingV2::Listener

#### Properties:
| Property Name | Value |
| -------------- | ----- |
| DefaultActions | [{'TargetGroupArn': {'Ref': 'DummyTargetGroupPublic'}, 'Type': 'forward'}] || LoadBalancerArn | {'Ref': 'PublicLoadBalancer'} || Port | 80 || Protocol | HTTP |

### ECSRole Resource

#### Resource Type
AWS::IAM::Role

#### Properties:
| Property Name | Value |
| -------------- | ----- |
| AssumeRolePolicyDocument | {'Statement': [{'Effect': 'Allow', 'Principal': {'Service': ['ecs.amazonaws.com']}, 'Action': ['sts:AssumeRole']}]} || Path | / || Policies | [{'PolicyName': 'ecs-service', 'PolicyDocument': {'Statement': [{'Effect': 'Allow', 'Action': ['ec2:AttachNetworkInterface', 'ec2:CreateNetworkInterface', 'ec2:CreateNetworkInterfacePermission', 'ec2:DeleteNetworkInterface', 'ec2:DeleteNetworkInterfacePermission', 'ec2:Describe*', 'ec2:DetachNetworkInterface', 'elasticloadbalancing:DeregisterInstancesFromLoadBalancer', 'elasticloadbalancing:DeregisterTargets', 'elasticloadbalancing:Describe*', 'elasticloadbalancing:RegisterInstancesWithLoadBalancer', 'elasticloadbalancing:RegisterTargets'], 'Resource': '*'}]}}] |

### ECSTaskExecutionRole Resource

#### Resource Type
AWS::IAM::Role

#### Description
Test

#### Properties:
| Property Name | Value |
| -------------- | ----- |
| AssumeRolePolicyDocument | {'Statement': [{'Effect': 'Allow', 'Principal': {'Service': ['ecs-tasks.amazonaws.com']}, 'Action': ['sts:AssumeRole']}]} || Path | / || Policies | [{'PolicyName': 'AmazonECSTaskExecutionRolePolicy', 'PolicyDocument': {'Statement': [{'Effect': 'Allow', 'Action': ['ecr:GetAuthorizationToken', 'ecr:BatchCheckLayerAvailability', 'ecr:GetDownloadUrlForLayer', 'ecr:BatchGetImage', 'logs:CreateLogStream', 'logs:PutLogEvents'], 'Resource': '*'}]}}] |


# Outputs
The list of outputs this template exposes are:

| Output Name | Description | Export name | Value |
| ------------ | ----------- | ----------- | ----- |
| ClusterName | The name of the ECS cluster | {'Fn::Join': [':', [{'Ref': 'AWS::StackName'}, 'ClusterName']]}  | {'Ref': 'ECSCluster'}
| ExternalUrl | The url of the external load balancer | {'Fn::Join': [':', [{'Ref': 'AWS::StackName'}, 'ExternalUrl']]}  | {'Fn::Join': ['', ['http://', {'Fn::GetAtt': ['PublicLoadBalancer', 'DNSName']}]]}
| ECSRole | The ARN of the ECS role | {'Fn::Join': [':', [{'Ref': 'AWS::StackName'}, 'ECSRole']]}  | {'Fn::GetAtt': ['ECSRole', 'Arn']}
| ECSTaskExecutionRole | The ARN of the ECS role | {'Fn::Join': [':', [{'Ref': 'AWS::StackName'}, 'ECSTaskExecutionRole']]}  | {'Fn::GetAtt': ['ECSTaskExecutionRole', 'Arn']}
| PublicListener | The ARN of the public load balancer's Listener | {'Fn::Join': [':', [{'Ref': 'AWS::StackName'}, 'PublicListener']]}  | {'Ref': 'PublicLoadBalancerListener'}
| VPCId | The ID of the VPC that this stack is deployed in | {'Fn::Join': [':', [{'Ref': 'AWS::StackName'}, 'VPCId']]}  | {'Ref': 'VPC'}
| PublicSubnetOne | Public subnet one | {'Fn::Join': [':', [{'Ref': 'AWS::StackName'}, 'PublicSubnetOne']]}  | {'Ref': 'PublicSubnetOne'}
| PublicSubnetTwo | Public subnet two | {'Fn::Join': [':', [{'Ref': 'AWS::StackName'}, 'PublicSubnetTwo']]}  | {'Ref': 'PublicSubnetTwo'}
| FargateContainerSecurityGroup | A security group used to allow Fargate containers to receive traffic | {'Fn::Join': [':', [{'Ref': 'AWS::StackName'}, 'FargateContainerSecurityGroup']]}  | {'Ref': 'FargateContainerSecurityGroup'}

