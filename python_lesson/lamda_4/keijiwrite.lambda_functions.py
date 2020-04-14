import boto3
import json
from datetime import datetime

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # 渡されたデータを取得
    body = json.loads(event['body'])
    name = body['name']
    msg = body['msg']
    
    # 連番を更新ならびに取得
    seqtable = dynamodb.Table('sequence')
    response = seqtable.update_item(
        Key={ 'tablename' : 'keijiban' },
        UpdateExpression='set seq = seq + :val',
        ExpressionAttributeValues= { 
           ':val' : 1 
       }, 
       ReturnValues='UPDATED_NEW'
    ) 
    nextval = response['Attributes']['seq']

    # 掲示板データの書き込み
    keijiban = dynamodb.Table('keijiban')
    keijiban.put_item(
        Item = {
            'id' : nextval,
            'name' : name,
            'msg' : msg,
            'postat' : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }    
    )

    return {
        'statusCode' : 200,
        'headers' : {
            'access-control-allow-origin' : '*',
            'content-type' : 'application/json'
        },
        'body' : json.dumps({'result' : 1})
    }