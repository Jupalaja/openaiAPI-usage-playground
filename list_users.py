import os
import json
import requests
import datetime
from dateutil.relativedelta import relativedelta

with open("config.json", "r") as f:
    config = json.load(f)

openai_org_id = config["openai_org_id"]
openai_api_key = config["openai_api_key"]

first_day_of_month = datetime.date.today().replace(day=1)
current_day = datetime.date.today()

prompt_token_cost = 0.03
completion_token_cost = 0.06

headers = {
    "method": "GET",
    "authority": "api.openai.com",
    "scheme": "https",
    "path": f"/v1/organizations/{openai_org_id}/users",
    "authorization": f"Bearer {openai_api_key}",
}

users_response = requests.get(f"https://api.openai.com/v1/organizations/{openai_org_id}/users", headers=headers)
users = users_response.json()["members"]["data"]

print(users)