#!/usr/env/bin python3

import boto3,botocore
import argparse


parser = argparse.ArgumentParser(description="Arguments to supply security group for our security check")
parser.add_argument('-s','--security-group',dest='security_group', default='', type=str, help='Enter a security group to check')

args = parser.parse_args()


def SG_Names(client):
    response = client.describe_security_groups(
    )
    names = []
    SG = response['SecurityGroups']
    for key in SG:
       names.append(key['GroupName'])
    return names

def SG_IP_Ranges(client):
    response = client.describe_security_groups(
    )
    ip_ranges = []
    IP = response['SecurityGroups']
    for key in IP:
       IP2 = key['IpPermissionsEgress'][0]['IpRanges']
       for key in IP2:
            ip_ranges.append(key['CidrIp'])
    return ip_ranges

def Check_Security(client, name, ip):
    if ip == '0.0.0.0/0' or ip == '/0':
        print(f"{name} is open to the public inernet!")
    else:
        print(f"{name} is not open to the public internet.")
    print("")



def main():
    client = boto3.client('ec2')
    if not args.security_group:
        print(f"No security group was specified, All security groups information will be provided.")
        print("")
        SG_names = SG_Names(client)
        #print(f"Security Group Names: {SG_names}")
        SG_Ip = SG_IP_Ranges(client)
        #print(f"Security Group Ip Ranges: {SG_Ip}")
        for i in range(len(SG_names)):
            print(f"Security Group Name: {SG_names[i]}")
            print(f"Security Group Ip Range: {SG_Ip[i]}")
            SG_Check = Check_Security(client, SG_names[i], SG_Ip[i])

    else:
        print(f"You specified a security group named {args.security_group}.")
        print("")    
        sg_to_check = args.security_group
        SG_names = SG_Names(client)
        #print(f"Security Group: {sg_to_check}")
        SG_Ip = SG_IP_Ranges(client)
        is_found = False
        for i in range(len(SG_names)):
            if (sg_to_check == SG_names[i]):
                print(f"Security Group: {SG_names[i]}")
                print(f"Security Group Ip Range: {SG_Ip[i]}")
                SG_Check = Check_Security(client, SG_names[i], SG_Ip[i])
                is_found = True
            else:
                continue
        if is_found == False:
            print(f"{sg_to_check} was not found!")
        else:
            print("")
   
   







if __name__ == "__main__":
    main()