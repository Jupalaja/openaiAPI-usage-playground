"""
Merge of the files to get users API token usage by user
"""
import json
import requests
import datetime
from dateutil.relativedelta import relativedelta

# Read config.json
with open("config.json", "r") as f:
    config = json.load(f)

openai_org_id = config["openai_org_id"]
openai_api_key = config["openai_api_key"]

first_day_of_month = datetime.date.today().replace(day=1)
current_day = datetime.date.today()

headers = {
    "method": "GET",
    "authority": "api.openai.com",
    "scheme": "https",
    "path": f"/v1/organizations/{openai_org_id}/users",
    "authorization": f"Bearer {openai_api_key}",
}

users_response = requests.get(f"https://api.openai.com/v1/organizations/{openai_org_id}/users", headers=headers)
users = users_response.json()["members"]["data"]

for user in users:
    id_of_user = user["user"]["id"]

    daily_costs = {}  # Dictionary to store daily costs

    start_date = first_day_of_month.strftime("%Y-%m-%d")
    end_date = current_day.strftime("%Y-%m-%d")

    usage_headers = {
        "method": "GET",
        "authority": "api.openai.com",
        "authorization": f"Bearer {openai_api_key}",
        "openai-organization": openai_org_id,
    }
    usage_response = requests.get(f"https://api.openai.com/v1/dashboard/billing/usage?start_date={start_date}&end_date={end_date}&user_public_id={id_of_user}", headers=usage_headers)
    user_data = usage_response.json()

    for daily_cost in user_data["daily_costs"]:
        timestamp = daily_cost["timestamp"]
        date = datetime.datetime.fromtimestamp(int(timestamp)).date().strftime("%Y-%m-%d")
        cost = sum([item["cost"] for item in daily_cost["line_items"]])

        daily_costs[date] = cost

    email = user["user"]["email"]
    total_cost = user_data["total_usage"]

    user_json = user["user"].copy()
    user_json["usage"] = user_data
    user_json["total_cost"] = total_cost
    user_json["daily_costs"] = daily_costs  # Add daily costs to the JSON

    user_name = user["user"]["name"].replace(" ", "_")
    with open(f"{user_name}.json", "w") as f:
        json.dump(user_json, f)
