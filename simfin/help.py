import requests

url = "https://backend.simfin.com/api/v3/companies/statements/verbose?ticker=O&statements=PL,BS,CF"

headers = {
    "accept": "application/json",
    "Authorization": "f8d0acc7-1d68-4db0-8532-b38745a47b5e"
}

response = requests.get(url, headers=headers)
import json

print(json.dumps(response.json(),indent=4))