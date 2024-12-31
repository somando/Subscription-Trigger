import boto3
from boto3.dynamodb.conditions import Key, Attr

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import const

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(const.DYNAMODB_TABLE_NAME)

def getItems(date):
    
    response = table.query(
        IndexName='NextDateIndex',
        KeyConditionExpression=Key('next_date').eq(date),
        FilterExpression=Attr('pause').eq(False)
    )
    items = response.get('Items', [])
    
    while 'LastEvaluatedKey' in response:
        response = table.query(
            IndexName='NextDateIndex',
            KeyConditionExpression=Key('next_date').eq(date),
            FilterExpression=Attr('pause').eq(False),
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        items.extend(response.get('Items', []))
    
    return items


def pickUserData(datas):
    
    user_datas = {}
    
    for datas in datas:
        
        user = datas['user']
        
        if user in user_datas:
            
            user_datas[user].append(datas)
        
        else:
            
            user_datas[user] = [datas]
    
    return user_datas


def nextDate(date, interval, unit):
    
    now_next_date = datetime.strptime(date, '%Y-%m-%d')
    
    if unit == "day":
        
        next_date = now_next_date + timedelta(days=interval)
    
    elif unit == "week":
        
        next_date = now_next_date + timedelta(weeks=interval)
    
    elif unit == "month":
        
        next_date = now_next_date + relativedelta(months=interval)
    
    elif unit == "year":
        
        next_date = now_next_date + relativedelta(years=interval)
    
    else:
        
        next_date = now_next_date
    
    return next_date.strftime('%Y-%m-%d')


def setNewDate(datas):
    
    for data in datas:
        
        table.update_item(
            Key={
                'id': data['id']
            },
            UpdateExpression="SET next_date = :new_date",
            ExpressionAttributeValues={
                ':new_date': nextDate(data['next_date'], data['interval'], data['unit'])
            },
            ReturnValues="UPDATED_NEW"
        )

