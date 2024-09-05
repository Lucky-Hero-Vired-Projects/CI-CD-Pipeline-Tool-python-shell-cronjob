import boto3
import paramiko
import time

#Define the Required variables
aws_region = "ap-south-1" 
key_pair_name = "lucky"  
instance_type = "t2.micro"  
ami_id = "ami-0522ab6e1ddcc7055"  

# Path to your PEM key file
key_path = "/Users/A2354661/Desktop/python-practice/HeroVired/assignment/CI-CD-Pipeline-Tool-python-shell-cronjob/lucky.pem"  

# Path to the packages file
packages_file = "packages.txt"

# List of local files to copy to ec2
files_to_copy = [
    ("index.html", "/var/www/html/index.html"),
    ("default", "/etc/nginx/sites-available/default")
]

# Initialize Boto3 EC2 client
ec2 = boto3.client('ec2', region_name=aws_region)

# Function to create an EC2 instance
def create_ec2_instance():
    # Read the user data script from the packages file
    with open(packages_file, "r") as f:
        packages = f.read().splitlines()
    user_data_script = "#!/bin/bash\n" + "\n".join([f"sudo apt-get install -y {package}" for package in packages])

    # Create EC2 instance
    instance = ec2.run_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        KeyName=key_pair_name,
        MinCount=1,
        MaxCount=1,
        UserData=user_data_script,
        TagSpecifications=[{
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': 'Lucky'}]
        }]
    )

    instance_id = instance['Instances'][0]['InstanceId']
    print(f"EC2 instance created with Instance ID: {instance_id}")

    # Wait for the instance to be running
    waiter = ec2.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance_id])
    print("EC2 instance is now running.")

    return instance_id

# Function to get the public IP address of the EC2 instance
def get_instance_public_ip(instance_id):
    response = ec2.describe_instances(InstanceIds=[instance_id])
    public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
    return public_ip

# Function to copy multiple files to EC2 using Paramiko
def copy_files_to_ec2(public_ip):
    # Load your PEM key file
    key = paramiko.RSAKey.from_private_key_file(key_path)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the EC2 instance
    ssh.connect(public_ip, username="ubuntu", pkey=key)
    print("Connected to EC2 instance.")

    # Use SCP to copy the files to the EC2 instance
    sftp = ssh.open_sftp()
    for local_file, remote_file in files_to_copy:
        sftp.put(local_file, remote_file)
        print(f"File {local_file} copied to EC2 instance at {remote_file}.")
    sftp.close()

    # Close the SSH connection
    ssh.close()

def main():
    instance_id = create_ec2_instance()
    time.sleep(60) 
    public_ip = get_instance_public_ip(instance_id)
    print(f"Public IP address of the EC2 instance: {public_ip}")
    copy_files_to_ec2(public_ip)
    print("All tasks completed.")

if __name__ == "__main__":
    main()
