#!/usr/env/bin python3

import boto3

DRYRUN = False


def Get_Image(ec2_client):
    image_response = ec2_client.describe_images(
        Filters=[
            {
                'Name': 'description',
                'Values': ['Amazon Linux 2 AMI*']
            },
            {
                'Name': 'architecture',
                'Values': ['x86_64']
            },
            {
                'Name': 'owner-alias',
                'Values': ['amazon']
            }
        ]
    )
    return image_response['Images'][0]['ImageId']
def Create_EC2(ec2_client, AMI):
    response = ec2_client.run_instances(
        ImageId = AMI,
        InstanceType = 't2.micro',
        MaxCount = 1,
        MinCount = 1,
        DryRun=DRYRUN,
        SecurityGroups = ['WebSG'],
        UserData='''#!/bin/bash -ex
            # Updated to use Amazon Linux 2
            yum -y update
            yum -y install httpd php mysql php-mysql
            /usr/bin/systemctl enable httpd
            /usr/bin/systemctl start httpd
            cd /var/www/html
            wget https://aws-tc-largeobjects.s3-us-west-2.amazonaws.com/CUR-TF-100-ACCLFO-2/lab6-scaling/lab-app.zip
            unzip lab-app.zip -d /var/www/html/
            chown apache:root /var/www/html/rds.conf.php
        '''
    )
    return response['Instances'][0]['InstanceId']



def main():
    client = boto3.client('ec2')
    AMI = Get_Image(client)
    instance_id = Create_EC2(client,AMI)
    ec2_instance = boto3.resource('ec2')
    ec2 = ec2_instance.Instance(instance_id)
    tag = ec2.create_tags(
        DryRun=False,
        Tags=[
            {
                'Key': 'Name',
                'Value': 'Alex-instance'
            },
        ]
    )

    print(ec2.instance_id)
    print("Waiting for instance to run...")
    print(f"Instance is {ec2.state['Name']}")
    ec2.wait_until_running()
    print("Instance is now up and running...")
    print(ec2.public_ip_address)
    print(ec2.tags)
    print(f"Instance is {ec2.state['Name']}")
    #ec2.terminate()
    #print("Waiting for instance to terminate...")
    #print(f"Instance is {ec2.state['Name']}")
    #ec2.wait_until_terminated()
    #print("Instance is now terminated...")

if __name__ == "__main__":
    main()