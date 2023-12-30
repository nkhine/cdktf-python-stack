#!/usr/bin/env python
from constructs import Construct
from cdktf import Token
from stacks.base_stack import BaseStack
from imports.aws.vpc import Vpc
from imports.aws.subnet import Subnet
from imports.aws.internet_gateway import InternetGateway
from imports.aws.route_table import RouteTable
from imports.aws.route_table_association import RouteTableAssociation
from imports.aws.nat_gateway import NatGateway

from imports.aws.eip import Eip


AWS_REGION = "eu-west-1"
ALL_IP_ADDRESSES = "0.0.0.0/0"
# https://cidr.xyz
VPC_CIDR_BLOCK = "10.0.0.0/16"
PUBLIC_CIDR_BLOCK = "10.0.2.0/24"
PRIVATE_CIDR_BLOCK = "10.0.1.0/24"


class NetworkingStackConfig:
    tag_name_prefix: str
    region: str

    def __init__(self, tag_name_prefix: str):
        self.tag_name_prefix = tag_name_prefix
        self.region = AWS_REGION


class NetworkingStack(BaseStack):
    region: str
    aws_vpc: Vpc
    aws_public_subnet: Subnet
    aws_private_subnet: Subnet

    def __init__(self, scope: Construct, id: str, config: NetworkingStackConfig):
        super().__init__(scope, id, config.region)

        self.region = config.region

        self.aws_vpc = self._create_vpc(config.tag_name_prefix)

        self.aws_internet_gateway = self._create_internet_gateway(
            config.tag_name_prefix
        )

        self.aws_public_subnet = self._create_public_subnet(
            self.aws_internet_gateway.id, config.tag_name_prefix
        )

        self.aws_private_subnet = self._create_private_subnet(
            self.aws_internet_gateway, config.tag_name_prefix
        )

    def _create_vpc(self, tag_name_prefix):
        return Vpc(
            self,
            "vpc",
            cidr_block=VPC_CIDR_BLOCK,
            # Instances in the VPC can use Amazon-provided DNS server
            enable_dns_support=True,
            # Instances in the VPC will be assigned public DNS hostnames
            # if they have public IP addresses
            enable_dns_hostnames=True,
            tags={"Name": f"{tag_name_prefix}vpc"},
        )

    def _create_internet_gateway(self, tag_name_prefix):
        return InternetGateway(
            self,
            "internet-gateway",
            tags={"Name": f"{tag_name_prefix}internet-gateway"},
            vpc_id=self.aws_vpc.id,
        )

    def _create_subnet(self, subnet_id, cidr_block, tag_name_prefix):
        return Subnet(
            self,
            subnet_id,
            cidr_block=cidr_block,
            tags={"Name": f"{tag_name_prefix}{subnet_id}"},
            vpc_id=self.aws_vpc.id,
        )

    def _associate_subnet_to_gateway(
        self, subnet_id, gateway_id, gateway_type, tag_name_prefix
    ):
        aws_route_table = RouteTable(
            self,
            f"{gateway_type}-route-table",
            route=[{"cidrBlock": ALL_IP_ADDRESSES, "gatewayId": gateway_id}],
            tags={"Name": f"{tag_name_prefix}route-table"},
            vpc_id=Token.as_string(self.aws_vpc.id),
        )

        RouteTableAssociation(
            self,
            f"{gateway_type}-route-table-association",
            route_table_id=aws_route_table.id,
            subnet_id=subnet_id,
        )

    def _create_public_subnet(self, internet_gateway_id, tag_name_prefix):
        subnet = self._create_subnet(
            "public-subnet", PUBLIC_CIDR_BLOCK, tag_name_prefix
        )

        self._associate_subnet_to_gateway(
            subnet.id, internet_gateway_id, "internet", tag_name_prefix
        )

        return subnet

    def _create_elastic_ip(self, internet_gateway, tag_name_prefix):
        return Eip(
            self,
            "eip",
            # domain="vpc",
            tags={"Name": f"{tag_name_prefix}eip"},
            depends_on=[internet_gateway],
        )

    def _create_nat_gateway(self, elastic_ip_id, tag_name_prefix):
        return NatGateway(
            self,
            "nat-gateway",
            connectivity_type="public",
            allocation_id=elastic_ip_id,
            subnet_id=self.aws_public_subnet.id,
            tags={"Name": f"{tag_name_prefix}nat-gateway"},
        )

    def _create_private_subnet(self, internet_gateway, tag_name_prefix):
        eip = self._create_elastic_ip(internet_gateway, tag_name_prefix)

        nat_gateway = self._create_nat_gateway(eip.id, tag_name_prefix)

        subnet = self._create_subnet(
            "private-subnet", PRIVATE_CIDR_BLOCK, tag_name_prefix
        )

        self._associate_subnet_to_gateway(
            subnet.id, nat_gateway.id, "nat", tag_name_prefix
        )

        return subnet
