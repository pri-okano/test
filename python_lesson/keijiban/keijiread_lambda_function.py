import json
import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    keijitable = dynamodb.Table("keijiban")
    response = keijitable.scan()
    
    html = "<html><meta charset=\"UTF-8\"><body><h1>掲示板</h1>"
    for data in sorted(response["Items"], reverse=True, key=lambda d: d["postat"]):
        html = html + "<table>"
        html = html + "<tr>" + "<th>投稿者</th><td>{0}</td>".format(data['name']) + "</tr>"
        html = html + "<tr>" + "<th>投稿日時</th><td>{0}</td>".format(data['postat']) + "</tr>"
        html = html + "<tr>" + "<th>メッセージ</th><td>{0}</td>".format(data['msg']) + "</tr>"
        html = html + "</table>"
    html = html + "</body></html>"

    return {
        'statusCode': '200',
        'body': html,
        'headers': {
            'Content-Type': 'text/html',
        }
    }