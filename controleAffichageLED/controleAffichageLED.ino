// Variables fonctionnement
int delaiEnvoiBit         = 1000;  //ms
int delaiDetection        = 100;   //ms
int seuilUn               = 200;

// Definition du pin de reception donnees
#define analog      A0

// Variables
byte cpt_zeros = 0;
byte idx_trame = 1;
byte trame[43];
int horairesParis[3];
int horairesCergy[3];

void setup() {
  // Frequence de lecture pour le debug
  Serial.begin(9600); 
}

void loop() {
  // Detection ou non d'une trame
  delay(delaiDetection);
  int entree = analogRead(analog);

  // Si on detecte un signal on lance le processus
  if (entree > seuilUn){
    // On se deplace au milieu de la reception du signal
    delay(delaiEnvoiBit/2);
    // Recuperation de la trame
    for (byte idx = 0; idx < 43; idx = idx+1){
      int entree = analogRead(analog);
      if (entree > seuilUn){
        trame[idx] = 1;        
      }
      else {
        trame[idx] = 0;  
      }
      // DEBUG : affichage de la trame
      Serial.print(trame[idx]);
      // Attente du bit suivant
      delay(delaiEnvoiBit);
    }

    // Conversion donnees trame en valeurs numeriques
    horairesParis[0] = (((((trame[1]*2 + trame[2])*2 + trame[3])*2 + trame[4])*2 + trame[5])*2 + trame[6])*2 + trame[7];
    horairesParis[1] = (((((trame[8]*2 + trame[9])*2 + trame[10])*2+ trame[11])*2+ trame[12])*2 + trame[13])*2 + trame[14];
    horairesParis[2] = (((((trame[15]*2+ trame[16])*2 + trame[17])*2 + trame[18])*2+ trame[19])*2+ trame[20])*2 + trame[21];

    horairesCergy[0] = (((((trame[22]*2 + trame[23])*2 + trame[24])*2 + trame[25])*2+ trame[26])*2 + trame[27])*2+ trame[28];
    horairesCergy[1] = (((((trame[29]*2 + trame[30])*2 + trame[31])*2 + trame[32])*2 + trame[33])*2 + trame[34])*2 + trame[35];
    horairesCergy[2] = (((((trame[36]*2 + trame[37])*2 + trame[38])*2+ trame[39])*2 + trame[40])*2+ trame[41])*2 + trame[42];

    // DEBUG : affichage horaires
    Serial.print("-");
    Serial.print("Paris : ");
    for (byte idx = 0; idx < 3; idx = idx+1){
      Serial.print(horairesParis[idx]);
      Serial.print(" ");
    }

    Serial.print("Cergy : ");
    for (byte idx = 0; idx < 3; idx = idx+1){
      Serial.print(horairesCergy[idx]);
      Serial.print(" ");
    }

    // DEBUG : passage a la ligne
      Serial.println();


  }

}

