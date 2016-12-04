# coding: utf-8

import time
from os import path
import decimal
from logging import getLogger

import boto3
from jinja2 import Environment, FileSystemLoader

COUNTER_HASH_SIZE = 10

logger = getLogger()

env = Environment(loader=FileSystemLoader(path.join(path.dirname(__file__), 'templates'), encoding='utf8'))

dynamodb = boto3.resource('dynamodb')
count_table  = dynamodb.Table('lamdba-jinja')


def root_view(request):
    count = _count()
    template = env.get_template('index.html', )
    return template.render(title=u"鯖無神社", count=count, request=request)


def handle(event, context):
    logger.info(event)
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": root_view(event)
    }


def _count():
    """
    雑にリクエスト数をカウントするメソッド
    COUNTER_HASH_SIZE 分用意したカウンターに分散してインクリメントする
    :return: 総リクエスト数
    """
    counts = _get_counts()
    index = int(time.time() * 1000) % COUNTER_HASH_SIZE
    _increment_count(index)
    return sum(counts.values()) + 1


def _get_counts():
    counts = count_table.scan(Limit=COUNTER_HASH_SIZE)
    return {str(c['counter_id']): int(c['count']) for c in counts['Items']}


def _increment_count(index):
    count_table.update_item(
            Key={'counter_id': index},
            UpdateExpression="set #count = #count + :val",
            ExpressionAttributeNames={
                '#count': 'count'
            },
            ExpressionAttributeValues={
                ':val': decimal.Decimal(1)
            }
     )


if __name__ == '__main__':
    print(root_view({}))
