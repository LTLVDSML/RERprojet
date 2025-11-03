import requests

url = 'https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring?MonitoringRef=STIF%3AStopPoint%3AQ%3A473921%3A&LineRef=STIF%3ALine%3A%3AC01742%3A'

token = ''

headers = {
    "apiKey": token,
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print("succes")
    
    ## Traitements ############
    
    ###########################
    
else:
    print("echec")
    