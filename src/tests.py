from utils import AWSOperations

aws = AWSOperations()

print(aws.__class__)

aws.stop_database_ec2_if_running()

ip = aws.get_database_public_ip()

print("The public IP is:", ip)
