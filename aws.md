-------------------------------------------
1. [Create a VPC](https://github.com/jsidberry/general-notes/blob/master/aws.md#create-a-vpc)
2. [Create 2 Subnets](https://github.com/jsidberry/general-notes/blob/master/aws.md#create-2-subnets)
3. Create an Internet GateWay - IGW
4. Attach the IGW to a VPC
5. Delete a VPC (with no IGW attached)
6. Create a Route Table for the VPC
7. Create a Route for Internet/Public Traffic
8. Add an EC2 Instance (for Public Access from Internet; i.e. WebServer)
9. Create a Route for Private Traffic
-------------------------------------------

[AWS CLI for EC2](https://docs.aws.amazon.com/cli/latest/reference/ec2/index.html#cli-aws-ec2)


####  create a VPC
`aws ec2 create-vpc --cidr-block 10.0.0.0/16 --amazon-provided-ipv6-cidr-block --instance-tenancy default`
```json
{
    "Vpc": {
        "CidrBlock": "10.0.4.0/24",
        "DhcpOptionsId": "dopt-fa4e2693",
        "State": "pending",
        "VpcId": "vpc-0507...",
        "InstanceTenancy": "default",
        "Ipv6CidrBlockAssociationSet": [
            {
                "AssociationId": "vpc-cidr-assoc-0286...",
                "Ipv6CidrBlock": "",
                "Ipv6CidrBlockState": {
                    "State": "associating"
                }
            }
        ],
        "CidrBlockAssociationSet": [
            {
                "AssociationId": "vpc-cidr-assoc-076f...",
                "CidrBlock": "10.0.4.0/24",
                "CidrBlockState": {
                    "State": "associated"
                }
            }
        ],
        "IsDefault": false,
        "Tags": []
    }
}
```
`aws ec2 create-tags --resources "vpc-0507..." --tags Key=Name,Value=diamondOneVPC`

#### Create at least 2 subnets
`aws ec2 create-subnet --vpc-id "vpc-0507..." --cidr-block "10.0.1.0/24" --availability-zone "us-east-2a"`

`aws ec2 create-subnet --vpc-id "vpc-0507..." --cidr-block "10.0.2.0/24" --availability-zone "us-east-2b"`

`aws ec2 create-tags --resources "subnet-0f1e..." --tags Key=Name,Value="10.0.1.0 - us-east-2a"`

`aws ec2 create-tags --resources "subnet-015c..." --tags Key=Name,Value="10.0.2.0 - us-east-2b"`


#### Create a Internet GateWay - IGW
`aws ec2 create-internet-gateway --dry-run`

`aws ec2 create-tags --resources "igw-08e4..." --tags Key=Name,Value="diamondOneIGW"`


#### Attach the Internet GateWay IGW to a VPC 
`aws ec2 attach-internet-gateway --vpc-id "vpc-0507..." --internet-gateway-id "igw-08e4..." --region "us-east-2"`


#### Delete a VPC (with no IGW attached)
`aws ec2 delete-vpc --vpc-id "vpc-0507..."`


#### Create a Route Table
`aws ec2 create-route-table --vpc-id "vpc-0986..."`

`aws ec2 create-tags --resources "rtb-0d90..." --tags Key=Name,Value=internetRouteOne`

#### Create a Route for Internet/Public Traffic
`aws ec2 create-route --route-table-id "rtb-0d90..." --destination-cidr-block "0.0.0.0/0" --gateway-id "igw-08e4..."`

`aws ec2 associate-route-table --route-table-id "rtb-0d90..." --subnet-id "subnet-0f1e..."`

`aws ec2 modify-subnet-attribute --subnet-id "subnet-0f1e..." --map-public-ip-on-launch`


#### Add an EC2 Instance
```bash
aws ec2 run-instances --profile "jsidberry" --image-id "ami-aa2e..." --count 1 \
	--iam-instance-profile Name=EC2-S3-Full-Access \
	--block-device-mappings 'DeviceName="/dev/xvda",Ebs={DeleteOnTermination=true,VolumeSize=30,VolumeType=gp2}' \
	--key-name "Ohio" --security-group-ids "sg-54f3..." --subnet-id "subnet-b9a3..." \
	--tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=elk-ubuntu-1}]' \
	--instance-type "t2.2xlarge" --user-data "file:///Users/elk-ubuntu.sh"
```

#### Create a Route for Private Traffic
```bash
aws ec2 create-route --route-table-id "rtb-0d90..." \
	--destination-cidr-block "0.0.0.0/0" --destination-ipv6-cidr-block "::/0" \ 
	--gateway-id "igw-08e4..."
```

### Example Python Code for AWS Resources
[Python Code for AWS Resource](https://github.com/awsdocs/aws-doc-sdk-examples)
