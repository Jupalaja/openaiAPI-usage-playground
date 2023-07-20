"""
Check token usage of OpenAI and multiply by corresponding model price
"""

import requests
from datetime import date
from pprint import pprint
import json


with open("config.json", "r") as f:
    config = json.load(f)

openai_org_id = config["openai_org_id"]
openai_api_key = config["openai_api_key"]
my_public_key = config["my_public_key"]

snapshot_id = {
  "gpt-3.5-turbo-0613": 0.0015,
  "gpt-3.5-turbo-16k-0613": 0.003,
  "gpt-4-0613": 0.03,
  "text-davinci:003": 0.03
}

usage_url = "https://api.openai.com/v1/usage"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai_api_key}"
}

params = {
    "date":"2023-07-19",
    "user_public_id": f"{my_public_key}"
}

pricing = {
  "gpt-3.5-turbo-0613": 0.002,
  "gpt-3.5-turbo-16k-0613": 0.004,
  "gpt-4-0613": 0.06,
  "text-davinci:003": 0.12
}

response = requests.get(usage_url, headers=headers, params=params)

if response.status_code == 200:
    usage_data = response.json()

    list =[] 
    for val in usage_data['data']: 
        cost = ((
            val['n_context_tokens_total'] *  pricing[val['snapshot_id']]
            +
            val['n_generated_tokens_total'] *  pricing[val['snapshot_id']]
            ) * 0.001)


        list.append(cost)

    print (sum(list))
    
else:
    print(f"Request failed with status code: {response.status_code}")

