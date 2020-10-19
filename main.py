import uuid
import random
from typing import List
import csv
import json
import time

import requests

URL = 'http://10.83.9.33:8080/v1/subscription'
TOKEN = ...
ACCOUNT_UUID = 'aac820c0-3c0c-4b34-a08f-e2cd0df9992b'
CUSTOMER_UUID = '40f86abc-abba-47f8-9247-c0032d7d7702'


def load_data_from_file() -> List:
    triplets = []
    with open('C:/Users/guyg/Downloads/Dell POC SIMS.csv', newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            triplets.append((row[0], row[1], row[2]))
    return triplets


def assign_values_to_subscriber(n: int, data: List, dummy_subscriber: dict) -> List:
    responses = []
    for i in range(1, n):
        dummy_subscriber['uuId'] = str(uuid.uuid4())
        dummy_subscriber['identityNumber'] = str(random.randint(100000000, 399999999))
        dummy_subscriber['keyValue'] = data[i][2]
        dummy_subscriber['imsi'] = data[i][1]
        dummy_subscriber['iccid'] = data[i][0]
        dummy_subscriber['imei'] = str(random.randint(3000000000, 5999999999))
        print(dummy_subscriber)
        responses.append(submit_request_subscription(dummy_subscriber))
    return responses


def submit_request_subscription(subscriber_data: dict) -> bool:
    data = subscriber_data
    headers = {'Content-type': 'application/json', 'Accept': '*/*', 'Connection': 'keep-alive', 'Authorization': TOKEN}
    response = requests.post(URL, data=json.dumps(data), headers=headers)
    time.sleep(1)
    return response.text


subscriber_obj = {'uuId': None, 'personalDetails':
    {'firstName': 'Guy', 'lastName': 'test', 'middleName': 'py', 'gender': 'MALE', 'identityNumber': '',
     'identityType': 'ID', 'birthday': '1990-01-14T10:00:00.000Z'},
     'status': 'ACTIVE', 'type': 'MOBILE', 'account': {'uuId': ACCOUNT_UUID, 'name': 'Dell'},
      'customer': {'name': 'Corp', 'uuId': CUSTOMER_UUID},
      'iccid': '<iccid>', 'imei': '1111111111', 'imsi': '<imsi>', 'keyValue': '<msisdn>'}

data_lst = load_data_from_file()

print('Please enter active token for env')
TOKEN = input()

iterations: int = 6

a = assign_values_to_subscriber(iterations, data_lst, subscriber_obj)
print(len(a))











