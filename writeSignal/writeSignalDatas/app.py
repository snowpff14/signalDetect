import json
import boto3
import os
import csv
import codecs
import sys
import traceback
import collections
from datetime import datetime

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

bucket = os.environ['bucket']
key = os.environ['key']
tableName = os.environ['table']

def lambda_handler(event, context):


   #get() does not store in memory
   try:
       obj = s3.Object(bucket, key).get()['Body']
   except:
       print("S3 Object could not be opened. Check environment variable. ")
       print(traceback.format_exc())
   try:
       table = dynamodb.Table(tableName)
   except:
       print("Error loading DynamoDB table. Check if table was created correctly and environment variable.")
       print(traceback.format_exc())

   batch_size = 100
   batch = []
   date =datetime.now()
   dateStr=date.strftime('%Y%m%d')

   #DictReader is a generator; not stored in memory
   for row in csv.DictReader(codecs.getreader('utf-8')(obj)):
      if len(batch) >= batch_size:
         write_to_dynamo(batch)
         batch.clear()
      listRow=list(row.items())
      drugAeName=row['DrugName']+'_'+row['AeName']
      listRow.append(('DrugAeName',drugAeName))
      listRow.append(('inputDate',dateStr))
      del listRow[0]
      row = collections.OrderedDict(listRow)

      batch.append(row)

   if batch:
      write_to_dynamo(batch)

   return {
      'statusCode': 200,
      'body': json.dumps('Uploaded to DynamoDB Table')
   }


def write_to_dynamo(rows):
   try:
      table = dynamodb.Table(tableName)
   except:
      print("Error loading DynamoDB table. Check if table was created correctly and environment variable.")

   try:
      with table.batch_writer() as batch:
         for i in range(len(rows)):
            row=rows[i]
            batch.put_item(
               Item=row
            )
   except:
      print(traceback.format_exc())
      print("Error executing batch_writer")