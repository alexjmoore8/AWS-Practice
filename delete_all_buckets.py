#!/usr/env/bin python3

import boto3

client = boto3.client('s3')

response = client.list_buckets()
print("Deleted buckets and objects: ")
for bucket in response['Buckets']:
    bucketName = bucket['Name']
    print(bucket['Name'])
    response1 = client.list_objects_v2(
        Bucket = bucketName
    )
    for object in response1['Contents']:
        print(object['Key'])
        key = object['Key']
        client.delete_object(
            Bucket = bucketName,
            Key = key,
        )
    response3 = client.delete_bucket(
        Bucket = bucketName
    )

