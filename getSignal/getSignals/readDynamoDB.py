import json
import boto3
import os
import traceback
import decimal
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')




class ReadDynamoDB():


    def drugNameSearch(self,drugName,tableName):
        keyCondition=Key('DrugName').eq(drugName)
        return self.readDatas(keyCondition,tableName)


    def aeNameSearch(self,aeName,tableName):
        keyCondition=Key('AeName').eq(aeName)
        return self.readDatas(keyCondition,tableName)

    def drugAeNameSearch(self,drugname,aeName,tableName):
        keyCondition=Key('DrugName').eq(drugname) & Key('AeName').eq(aeName)
        return self.readDatas(keyCondition,tableName)


    def readDatas(self, keyCondition,tableName):

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
            # outputDict['ROR_signal']=res['ROR_signal']
            outputList.append(outputDict)
        return outputList

