import requests
from datetime import datetime, timezone
from time import sleep

## FONCTIONS ##################################################################

def str2date(str):
    
    #annee + mois
    temp = str.split('-')
    date = [int(temp[0]), int(temp[1])]
    #jours
    temp = temp[2].split('T')
    date.append(int(temp[0]))
    #heures + minutes
    temp = temp[1].split(':')
    date.append(int(temp[0]))
    date.append(int(temp[1]))
    #secondes
    temp = temp[2].split('.')
    date.append(int(temp[0]))
    #millisecondes
    temp = temp[1].split('Z')
    date.append(int(temp[0]))
    
    return datetime(date[0], date[1], date[2], date[3], date[4], date[5], date[6], tzinfo=timezone.utc)
    

## CODE #######################################################################

gare = '41527'    #473921  41527
url = 'https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring?MonitoringRef=STIF%3AStopPoint%3AQ%3A'+ gare +'%3A&LineRef=STIF%3ALine%3A%3AC01742%3A'

token = 'YrYPqXUz8z3UyBvw3D7Vn8MdcGbi31l9'

headers = {
    "apiKey": token,
    "Accept": "application/json"
}

# Boucle infinie
infini =  1
while infini == 1:
    
    # Recuperation des donnees
    response = requests.get(url, headers=headers)
    
    # Si les donnees sont bien recues
    if response.status_code == 200:
        data = response.json()
        
        ## Traitements ############
        # Isolation des donnees pertinentes
        echantillon  = data["Siri"]["ServiceDelivery"]["StopMonitoringDelivery"][0]["MonitoredStopVisit"]
        # Recuperation du temps present en GMT
        maintenant = datetime.now(timezone.utc)
        # On enregitrera les 3 prochains trains dans chaque direction
        listeParis = []
        listeCergy = []
    
        # On traite chaque train recupere
        for idx in echantillon:
            # Temps d'arrivee
            arrivee = str2date(idx["MonitoredVehicleJourney"]["MonitoredCall"]["ExpectedArrivalTime"])
            # On retire les trains deja passes
            if arrivee > maintenant:
                destination = idx["MonitoredVehicleJourney"]["DestinationName"][0]["value"]
                # Vers Paris
                if (destination == 'Gare de Boissy-Saint-Léger' or destination == 'Torcy') and len(listeParis) < 3 :
                    ecart = arrivee - maintenant
                    attente = int(ecart.seconds/60)
                    listeParis.append(attente)
                # Vers Cergy    
                if destination == 'Gare de Cergy-Préfecture' and len(listeCergy) < 3 :
                    ecart = arrivee - maintenant
                    attente = int(ecart.seconds/60)
                    listeCergy.append(attente)
            
    
        ###########################
    # Dans le cas ou les donnees n'ont pas ete correctement recues
    else:
        print("echec")
        
    # On attend 30 secondes entre chaque iteration 
    print(listeParis[0])
    sleep(30)
        


   
    

    