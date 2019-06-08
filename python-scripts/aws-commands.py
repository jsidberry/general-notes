import os
import boto3
from botocore.exceptions import ClientError


def get_aws_access_credentials():
	current_user_home_directory = os.getenv('HOME')
	aws_credential_file = current_user_home_directory + '/.aws/credentials'
	item_key = []
	aws_access_key_id = ""
	aws_secret_access_key = ""
	creds_dict = {}

	with open(aws_credential_file, mode="r") as f:
		for item in f:
			if item[:1] == '[':
				item_len = len(item) - 2
				new_item = item[1:item_len]
				item_key.append(new_item.strip())

			secret_items = item.split('=')

			if secret_items[0].strip() == 'aws_access_key_id':
				aws_access_key_id = secret_items[1].strip()

			if secret_items[0].strip() == 'aws_secret_access_key':
				aws_secret_access_key = secret_items[1].strip()

			creds_dict[new_item] = [aws_access_key_id, aws_secret_access_key]

	return creds_dict


def ec2_describe_instances():
	try:
		# ec2 = boto3.client('ec2')
		response = ec2.describe_instances('i-03b7ac1c035eb6316')
		print(response)
		instancelist = []
		for reservation in (response["Reservations"]):
			for instance in reservation["Instances"]:
				instancelist.append(instance["InstanceId"])
		print(instancelist)

		# instances = ec2.instances.filter(
		# 	Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

		# for instance in instances:
		# 	print(instance.id, instance.instance_type)
		
		print()
	except:
		raise

def ec2_describe_regions():
	try:
		# ec2 = boto3.client('ec2')
		response = ec2.describe_regions()
		print('Regions:', response['Regions'])
		print()
	except:
		raise

def ec2_describe_security_groups():
	try:
		response = ec2.describe_security_groups(GroupIds=['SECURITY_GROUP_ID'])
		print(response)
		print()
	except ClientError as e:
		print(e)


def set_session_by_profile(session_variables):
	session = boto3.Session(
		profile_name=session_variables[profile_name],
		aws_access_key_id=session_variables[access_key],
		aws_secret_access_key=session_variables[secret_key],
		)
	return session


# Set Clients for EC2, S3, etc
ec2 = boto3.client('ec2')
s3 = boto3.client('s3')

profiles = []
num2 = []
session_variables = {}
credentials = get_aws_access_credentials()

# Loop thru all the credentials in the local .aws configuration file
for profile_name, aws_keys in credentials.items():
	profile = profile_name
	access_key = aws_keys[0]
	secret_key = aws_keys[1]
	session_variables[profile] = profile_name
	session_variables[access_key] = aws_keys[0]
	session_variables[secret_key] = aws_keys[1]

	set_session_by_profile(session_variables)

	ec2_describe_instances()
	# ec2_describe_regions()
	# ec2_describe_security_groups()
	print()


num2.append(get_aws_access_credentials().keys())


# for profile in profiles:
# 	print(profile)
# 	session = create_session(profile)

# for profile, access_keys in credentials:
# 	print(profile.keys())

# for credentials.keys() in credentials:
# 	print

# session = boto3.Session(
# 	profile_name=PROFILE,
#     aws_access_key_id=ACCESS_KEY,
#     aws_secret_access_key=SECRET_KEY,
# )
# ec2_instances = ec2.instances.filter(
#     Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
# for ec2_instance in ec2_instances:
#     print(ec2_instance.id, ec2_instance.instance_type)

# instances = ec2.describe_instances(DryRun=True)




# print(get_aws_access_credentials(creds_dict))

# AWS_ACCESS_KEY_ID = creds_dict['jsidberry'][0]

