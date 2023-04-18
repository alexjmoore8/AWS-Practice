#!/usr/bin/env python3

import boto3,csv

def Get_Instances():
    ec2_client = boto3.client('ec2')
    paginator = ec2_client.get_paginator('describe_instances')
    page_list = paginator.paginate(
         Filters=[
            {
                'Name': 'instance-state-name',
                'Values': [
                    'running',
                ],
                'Name': 'instance-type',
                'Values': [
                    't2.micro',
                ]
            },
        ],

    )
    response = []
    for page in page_list:
        for reservation in page['Reservations']:
            response.append(reservation)
    return response

def CSV_Writer(header, content):
    hFile = open('export.csv','w')
    writer = csv.DictWriter(hFile,fieldnames=header)
    writer.writeheader()
    for line in content:
        writer.writerow(line)
    hFile.close()

def main():


    response = Get_Instances()
    headerRow = ['InstanceId','InstanceType','State','PublicIpAddress','Monitoring']
    content = []
    for instance in response:
        for ec2 in instance['Instances']:
            #print(ec2['InstanceId'])
            content.append(
                {
                    "InstanceId": ec2['InstanceId'],
                    "InstanceType": ec2['InstanceType'],
                    "State": ec2['State']['Name'],
                    "PublicIpAddress": ec2.get('PublicIpAddress',"N/A"),
                    "Monitoring": ec2['State']['Name']   
                }
  
            )
    CSV_Writer(headerRow,content)


if __name__ == "__main__":
    main()