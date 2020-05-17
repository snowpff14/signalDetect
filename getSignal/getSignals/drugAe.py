import json
import boto3
import os
import traceback
from boto3.dynamodb.conditions import Key, Attr
from readDynamoDB import ReadDynamoDB


readDynamoDB=ReadDynamoDB()

def lambda_handler(event, context):

    drugname=event['drugName']
    aename=event['aeName']
    outputList=readDynamoDB.drugAeNameSearch(drugname,aename)
    return {
        "statusCode": 200,
        "body": json.dumps(outputList),
    }


