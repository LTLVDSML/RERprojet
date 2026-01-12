// Variables fonctionnement
int delaiEntreAcquisition = 100;  //ms
byte seuilUn              = 100;

// Definition du pin de reception donnees
#define analog      A0

// Variables
byte cpt_zeros = 0;
byte idx_trame = 1;
byte trame[96];
byte idx_donnees = 1;
byte donnees[16];


void setup() {
  // Frequence de lecture pour le debug
  Serial.begin(9600); 

}

void loop() {
  // Intervalle de temps entre chaque acquisition
  delay(delaiEntreAcquisition);
  // Reception signal
  byte entree = analogRead(analog);
  Serial.println(entree);

  // Gestion reception de trame /////////////////////
  // Detection debut de trame
  if (entree > seuilUn){
    trame[0] = 1;
    idx_trame = 1;
    cpt_zeros = 0;
    
    // Tant que la trame continue d'etre recue
    while (cpt_zeros < 12){
      // Reception signal
      byte entree = analogRead(analog);
      Serial.println(entree);
  
      // Si l'entree recoit un 1
      if (entree > seuilUn){
        cpt_zeros = 0;
        trame[idx_trame] = 1;
      }
      
      // Si l'entree recoit un 0
      else{
        cpt_zeros = cpt_zeros + 1;
        trame[idx_trame] = 0;
      }
      // Incrementation index trame
      idx_trame = idx_trame +1;
      if (idx_trame >= 96) {
        break;
      }


      // Intervalle de temps entre chaque acquisition
      delay(delaiEntreAcquisition);
    }
    // Decryptage trame
    idx_donnees = decryptageTrame(&trame[0], &donnees[0], idx_trame);

    // Affichage donnees traduites
    
  }

}

// FONCTIONS //////////////////////////////////////////
// Fonction de dechiffrement de la trame
byte decryptageTrame(byte* addrTrame, byte* addrDonnees, byte tailleTrame){

  byte tailleDonnees = 0;
  byte idxValeur = 1;
  byte valeur[6];

   // pour chaque bit de la trame
  for (byte idxTrame = 0; idxTrame < tailleTrame; idxTrame++){
    idxValeur = 1;
    valeur[6] = {0};
    // pour chaque valeur de la trame
    while(idxValeur < 6){
      valeur[idxValeur] = *(addrDonnees + idxTrame);
      idxValeur = idxValeur + 1;
      idxTrame = idxTrame + 1;
    }
    *(addrDonnees + tailleDonnees) = binaireSix(&valeur[0]);
    tailleDonnees = tailleDonnees + 1;
  }
  return tailleDonnees;
}


// Fonction traduction 6bits -> byte
byte binaireSix(byte* addrValeur){

  byte valeur = 0;
  
  for(byte idxBit = 0; idxBit < 6; idxBit++){
    valeur = valeur + *(addrValeur + idxBit) * 2 ^ idxBit;
  }

  return valeur;
  
}
