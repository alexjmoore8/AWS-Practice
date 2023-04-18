#!/usr/env/bin python3

import boto3
import datetime
import pytz


def List_Roles(client):
    response = client.list_roles(
        MaxItems=123
    )
    return response


def role_names(response):
    role_list = response['Roles']
    roleNames = [] 
    for key in role_list:
        #if somedate > (pytz.utc.localize(datetime.datetime.utcnow())-datetime.timedelta(days=90)):
        roleNames.append(key['RoleName'])
    return roleNames


def role_dates(response):
    role_list = response['Roles']

    createDate = []
    for key in role_list:
        #if somedate > (pytz.utc.localize(datetime.datetime.utcnow())-datetime.timedelta(days=90)):
        createDate.append(key['CreateDate'])
    return createDate

def print_role_names_and_dates(names, dates):
    for i in range(len(names)):
        if dates[i] > (pytz.utc.localize(datetime.datetime.utcnow())-datetime.timedelta(days=90)):
            print(f"Role Name: {names[i]}")
            print(f"Created Date: {dates[i]}")


def List_Role_Policy(client, name, date):
    response = client.list_role_policies(
        RoleName = name
    )

    list_policy_list = response['PolicyNames']

    for key in list_policy_list:
        if date > (pytz.utc.localize(datetime.datetime.utcnow())-datetime.timedelta(days=90)):
            print(key)


def List_Attached_Role_Policies(client, name, date):
    response = client.list_attached_role_policies(
        RoleName= name,
    )

    attached_policy_list = response['AttachedPolicies']

    for key in attached_policy_list:
        if date > (pytz.utc.localize(datetime.datetime.utcnow())-datetime.timedelta(days=90)):
            print(key['PolicyName'])






def main():
    client = boto3.client('iam')
    RoleList = List_Roles(client)
    names = role_names(RoleList)
    dates = role_dates(RoleList)

    print("Roles Created in the Last 90 Days:")
    Printlist = print_role_names_and_dates(names, dates)

    print("")
    print("Policies for Roles Created in the Last 90 Days: ")
    for i in range(len(names)):
        PolicyList = List_Role_Policy(client,names[i], dates[i])
    print("")
    print("Attached Policies for Roles Created in the Last 90 Days: ")
    for i in range(len(names)):
        AtachedPolicyList = List_Attached_Role_Policies(client,names[i], dates[i])  
        


if __name__ == "__main__":
    main()