import requests
import json

def push_realtime_metric_to_powerbi(dataset_url: str, rows: list):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(dataset_url, data=json.dumps(rows), headers=headers)
    return response.status_code == 200