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
        # 画像を追加
        if data.get('hasimage'):
            # ★ S3バケットのURLに修正してください
            html = html + "<tr><th colspan='1'><img src='http://webexample000000.s3-website-ap-northeast-1.amazonaws.com/{0}.jpg' width='320'></th></tr>".format(data['id'])
        html = html + "</table>"
    html = html + "</body></html>"

    return {
        'statusCode': '200',
        'body': html,
        'headers': {
            'Content-Type': 'text/html',
        }
    }
