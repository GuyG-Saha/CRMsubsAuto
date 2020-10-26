import uuid
import random
from typing import List
import csv
import json
import time

import requests

CRM_URL = 'http://10.83.9.33:8080/v1/subscription'
TOKEN = ...
ACCOUNT_UUID = 'aac820c0-3c0c-4b34-a08f-e2cd0df9992b'
CUSTOMER_UUID = '40f86abc-abba-47f8-9247-c0032d7d7702'

preconfigured_subscriber_uuIds = ['4df46114-5679-407c-ae20-73c628f3ae60', 'fd4bfd1e-35d8-4ffa-80f8-2c070e063a3a']


def load_device_data_from_file() -> List:
    triplets = []
    with open('C:/Users/guyg/Downloads/Dell POC SIMS (2).csv', newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            triplets.append((row[0], row[1], row[2]))
    return triplets


def load_subscriber_uuids() -> List:
    uuids = []
    with open('C:/Users/guyg/Downloads/Dell 102 subscriber uuid', newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row not in preconfigured_subscriber_uuIds:
                uuids.append(row[0])
    return uuids


def load_csv_file_data():
    d = {}
    with open('C:/Users/guyg/Downloads/Dell 104 subscriber uuid and lookup', "r") as file:
        for line in file:
            splited_line = line.replace(" ", "").replace("\n", "").split(",")
            uuid = splited_line[0]
            sim_data = splited_line[1]
            if uuid in d.keys():
                d[uuid].append(int(sim_data))
            else:
                d[uuid] = [int(sim_data)]

        for v in d.values():
            v.sort()

        for k, v in d.items():
            print("{}:{}".format(k, v))
    return d


def assign_values_to_subscriber(n: int, data: List, dummy_subscriber: dict, subscriber_uuids: List, flag=False) -> List:
    responses = []
    if not flag:
        for i in range(1, n):
            dummy_subscriber['uuId'] = subscriber_uuids[i - 1]
            dummy_subscriber['identityNumber'] = str(random.randint(100000000, 399999999))
            dummy_subscriber['keyValue'] = data[i][2]
            dummy_subscriber['imsi'] = data[i][1]
            dummy_subscriber['iccid'] = data[i][0]
            dummy_subscriber['imei'] = str(random.randint(3000000000, 5999999999))
            print(dummy_subscriber)
            responses.append(submit_request_subscription(dummy_subscriber))
    else:
        j = 0
        for i in range(-1, -n, -1):
            dummy_subscriber['uuId'] = preconfigured_subscriber_uuIds[j]
            dummy_subscriber['identityNumber'] = str(random.randint(100000000, 399999999))
            dummy_subscriber['keyValue'] = data[i][2]
            dummy_subscriber['imsi'] = data[i][1]
            dummy_subscriber['iccid'] = data[i][0]
            dummy_subscriber['imei'] = str(random.randint(3000000000, 5999999999))
            j += 1
            print(dummy_subscriber)
            responses.append(submit_request_subscription(dummy_subscriber))
    return responses


def submit_request_subscription(subscriber_data: dict) -> bool:
    data = subscriber_data
    headers = {'Content-type': 'application/json', 'Accept': '*/*', 'Connection': 'keep-alive', 'Authorization': TOKEN}
    response = requests.post(CRM_URL, data=json.dumps(data), headers=headers)
    time.sleep(1)
    return response.text


uuIds = load_subscriber_uuids()
print(uuIds)

subscriber_obj = {'uuId': None, 'personalDetails':
    {'firstName': 'Guy', 'lastName': 'test', 'middleName': 'py', 'gender': 'MALE', 'identityNumber': '',
     'identityType': 'ID', 'birthday': '1990-01-14T10:00:00.000Z'},
                  'status': 'ACTIVE', 'type': 'MOBILE', 'account': {'uuId': ACCOUNT_UUID, 'name': 'Dell'},
                  'customer': {'name': 'Corp', 'uuId': CUSTOMER_UUID},
                  'iccid': '<iccid>', 'imei': '1111111111', 'imsi': '<imsi>', 'keyValue': '<msisdn>'}

data_lst = load_device_data_from_file()

print('Please enter active token for env')
TOKEN = input()

iterations: int = len(data_lst) - 2

a = assign_values_to_subscriber(iterations, data_lst, subscriber_obj, uuIds)
print(a)



