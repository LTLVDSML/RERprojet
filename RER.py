import requests

gare = '41527'    #473921  41527
url = 'https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring?MonitoringRef=STIF%3AStopPoint%3AQ%3A'+ gare +'%3A&LineRef=STIF%3ALine%3A%3AC01742%3A'

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
    echantillon  = data["Siri"]["ServiceDelivery"]["StopMonitoringDelivery"][0]["MonitoredStopVisit"]
    
    cpt_paris = 0
    cpt_cergy = 0
    
    for idx in echantillon:
        # Torcy
        if idx["MonitoringRef"]["value"] == 'STIF:StopPoint:Q:41527:' and cpt_paris <3 :
            cpt_paris = cpt_paris + 1;
            
    
    ###########################
    
else:
    print("echec")
    