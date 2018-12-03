import boto3
import json
from botocore.vendored import requests

def lambda_handler(event, context):
	# TODO implement
	record = event["Records"][0]
	print(event)
	bucket = record["s3"]["bucket"]["name"]
	photoname = record["s3"]["object"]["key"]
	client = boto3.client('rekognition')
	response = client.detect_labels(
	    Image={
	        'S3Object': {
	            'Bucket': bucket,
	            'Name': photoname,
	        },
	    },
	    MaxLabels=10,
	    MinConfidence=90,
	)
	labels = []
	count = 0;
	for item in response["Labels"]:
		labels.append(item["Name"])
		
	jsonResponse = {
		"objectKey": photoname,
		"bucket": bucket,
		"createdTimestamp": record["eventTime"],
		"labels": labels 
	}

	print(jsonResponse)
	res = requests.post('https://vpc-elasticphotos-unknkut2kzumewb3w67boaouye.us-east-1.es.amazonaws.com/elasticphotos/_doc', json=jsonResponse)
	
	# res1 = requests.get('https://vpc-elasticphotos-unknkut2kzumewb3w67boaouye.us-east-1.es.amazonaws.com/elasticphotos/_search?q='+"Tree")
	# print(json.dumps(res1))
		
	# return {
	#     'statusCode': 200,
	#     'body': json.dumps('Hello from Lambda!')
	# }