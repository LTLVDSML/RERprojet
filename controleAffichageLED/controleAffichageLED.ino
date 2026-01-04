// Variables fonctionnement
int delaiEntreAcquisition = 100;  //ms
byte seuilUn              = 200;

// Definition du pin de reception donnees
#define analog      A0


void setup() {
  // Frequence de lecture pour le debug
  Serial.begin(9600);

}

void loop() {
  // Intervalle de temps entre chaque acquisition
  delay(delaiEntreAcquisition);
  // Reception signal
  byte entree = analogRead(analog);

  // Traitements ////////////////////////////////////
  // Detection debut de trame
  if (entree > seuilUn){

    
  }

}
