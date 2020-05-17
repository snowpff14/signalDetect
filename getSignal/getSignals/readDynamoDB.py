import json
import boto3
import os
import traceback
import decimal
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')

tableName = os.environ['table']



class ReadDynamoDB():


    def drugNameSearch(self,drugName):
        keyCondition=Key('DrugName').eq(drugName)
        return self.readDatas(keyCondition)


    def aeNameSearch(self,aeName):
        keyCondition=Key('AeName').eq(aeName)
        return self.readDatas(keyCondition)

    def drugAeNameSearch(self,drugname,aeName):
        keyCondition=Key('DrugName').eq(drugname) & Key('AeName').eq(aeName)
        return self.readDatas(keyCondition)


    def readDatas(self, keyCondition):

        try:
            table = dynamodb.Table(tableName)
        except:
            print("Error loading DynamoDB table. Check if table was created correctly and environment variable.")
            print(traceback.format_exc())

        responces=table.query(KeyConditionExpression=keyCondition )
        outputList=[]
        for res in responces['Items']:
            outputDict={}
            outputDict['DrugName']=res['DrugName']
            outputDict['AeName']=res['AeName']
            outputDict['n11']=res['n11']
            outputDict['ROR']=res['ROR']
            outputDict['PRR']=res['PRR']
            outputDict['PRR_signal']=res['PRR_signal']
            outputDict['ROR_signal']=res['ROR_signal']
            outputList.append(outputDict)
        return outputList

