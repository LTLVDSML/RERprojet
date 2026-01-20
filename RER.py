import requests
import RPi.GPIO as GPIO
from datetime import datetime, timezone
from time import sleep
import pprint

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
# Parametres reglage pin de sortie
pin = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin,GPIO.LOW)

# Parametres recuperation donnees API
gare = '65048'    #473921  41527  473109  65048
url = 'https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring?MonitoringRef=STIF%3AStopArea%3ASP%3A'+ gare +'%3A&LineRef=STIF%3ALine%3A%3AC01742%3A'

# Extraction token depuis fichier texte
with open('ratp', 'r') as fichier:
    token = fichier.read().rstrip()

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
                if (destination == 'Boissy-Saint-Léger' or destination == 'Gare de Boissy-Saint-Léger' or destination == 'Torcy' or destination == 'Marne-la-Vallée Chessy') and len(listeParis) < 3 :
                    ecart = arrivee - maintenant
                    attente = int(ecart.seconds/60)
                    listeParis.append(attente)
                # Vers Cergy    
                if destination == 'Cergy le Haut' and len(listeCergy) < 3 :
                    ecart = arrivee - maintenant
                    attente = int(ecart.seconds/60)
                    listeCergy.append(attente)
        
        # Affichage DEBUG
        print("Paris")
        pprint.pprint(listeParis)
        print("Cergy")
        pprint.pprint(listeCergy)
    
    # Dans le cas ou les donnees n'ont pas ete correctement recues
    else:
        print("echec")
        
    # On attend 30 secondes entre chaque iteration 
    # DEBUG AFFICHAGE
    GPIO.output(pin,GPIO.HIGH)
    sleep(30)
    GPIO.output(pin,GPIO.LOW)
    sleep(5)
