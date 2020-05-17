import json
import boto3
import os
import traceback
from boto3.dynamodb.conditions import Key, Attr
from readDynamoDB import ReadDynamoDB

tableName = os.environ['table']

readDynamoDB=ReadDynamoDB()

def lambda_handler(event, context):

    drugname=event['queryStringParameters']['drugName']
    outputList=readDynamoDB.drugNameSearch(drugname,tableName)
    return {
        "statusCode": 200,
        "body": json.dumps(outputList),
    }
