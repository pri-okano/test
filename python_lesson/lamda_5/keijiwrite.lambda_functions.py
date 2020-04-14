import boto3
import json
from datetime import datetime
import base64

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

    hasimage = 0
    # 画像の処理を追加
    if 'image' in body :
        # 1. ファイル名（XXXXXX.jpg）
        filename = str(nextval) + ".jpg"
        # 2. base64デコードする
        data = base64.b64decode(body['image'])
        # 3. S3に書き込む
        s3 = boto3.resource('s3')
        # ★★ バケット名は書き換えてください ★★
        target = s3.Object('webexample000000', filename)
        target.put(Body = data)
        hasimage = 1
    # 画像の処理ここまで


    # 掲示板データの書き込み
    keijiban = dynamodb.Table('keijiban')
    keijiban.put_item(
        Item = {
            'id' : nextval,
            'name' : name,
            'msg' : msg,
            'postat' : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'hasimage' : hasimage
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