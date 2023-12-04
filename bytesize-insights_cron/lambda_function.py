import json
import requests


print('Loading function')


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    print("Received context:", context)
    print(BACKEND_URL)
    
    res = requests.post(BACKEND_URL)
    
    if response.status_code == 200:
        print(response.json())
    else:
        try:
            print("Error Occurred:", response)
        except ValueError:
            print("Error Occurred:", reponse.json())
            
