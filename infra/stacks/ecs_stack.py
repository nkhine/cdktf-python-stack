from constructs import Construct
from cdktf import Fn, Token

from stacks.base_stack import BaseStack

from imports.aws.internet_gateway import InternetGateway

from imports.aws.subnet import Subnet
from imports.aws.vpc import Vpc
from imports.aws.ecs_cluster import EcsCluster
from imports.aws.ecs_cluster_capacity_providers import EcsClusterCapacityProviders
from imports.aws.ecs_service import EcsService
from imports.aws.ecs_task_definition import EcsTaskDefinition

from imports.aws.service_discovery_public_dns_namespace import (
    ServiceDiscoveryPublicDnsNamespace,
)
from imports.aws.service_discovery_service import ServiceDiscoveryService


class EcsStackConfig:
    region: str
    aws_vpc: Vpc
    internet_gateway: InternetGateway
    aws_public_subnet: Subnet

    def __init__(
        self,
        region: str,
        aws_vpc: Vpc,
        internet_gateway: InternetGateway,
        aws_public_subnet: Subnet,
    ):
        self.region = region
        self.aws_vpc = aws_vpc
        self.internet_gateway = internet_gateway
        self.aws_public_subnet = aws_public_subnet


class EcsStack(BaseStack):
    def __init__(self, scope: Construct, id: str, config: EcsStackConfig, **kwargs):
        super().__init__(scope, id, config.region, **kwargs)

        ecs_cluster = EcsCluster(
            self,
            "ecs_cluster",
            name="ecs_ecs_cluster",
            setting=[{"name": "containerInsights", "value": "enabled"}],
        )
        EcsClusterCapacityProviders(
            self,
            "example",
            capacity_providers=["FARGATE"],
            cluster_name=ecs_cluster.name,
            default_capacity_provider_strategy=[
                {"capacityProvider": "FARGATE", "weight": 1}
            ],
        )

        task_registration = EcsTaskDefinition(
            self,
            "task_registration",
            container_definitions=Token.as_string(
                Fn.jsonencode(
                    [
                        {
                            "essential": True,
                            "image": "httpd:2.4",
                            "name": "dotnet",
                            "port_mappings": [{"container_port": 80, "host_port": 80}],
                        }
                    ]
                )
            ),
            cpu=".5vCPU",
            family="task_definition_demo",
            memory="1024",
            network_mode="awsvpc",
            requires_compatibilities=["FARGATE"],
            runtime_platform={
                "cpu_architecture": "ARM64",
                "operating_system_family": "LINUX",
            },
        )
        cloud_map_dns = ServiceDiscoveryPublicDnsNamespace(
            self,
            "cloud_map_dns",
            description="cloud map",
            name="serverless.terraform.com",
        )
        cloud_map_service = ServiceDiscoveryService(
            self,
            "cloud_map_service",
            dns_config={
                "dns_records": [{"ttl": 10, "type": "A"}],
                "namespace_id": cloud_map_dns.id,
            },
            name="cloudmapservice",
            namespace_id=cloud_map_dns.id,
        )

        EcsService(
            self,
            "ecs_service",
            cluster=ecs_cluster.name,
            deployment_maximum_percent=200,
            deployment_minimum_healthy_percent=100,
            desired_count=2,
            enable_ecs_managed_tags=Token.as_any(True),
            launch_type="FARGATE",
            name="ecs-fargate-service",
            network_configuration={
                "assign_public_ip": Token.as_any(True),
                # FIXME
                # "security_groups": [allow_http.id],
                "subnets": [config.aws_public_subnet.id],
            },
            service_registries={"registry_arn": cloud_map_service.arn},
            task_definition=task_registration.arn,
        )
