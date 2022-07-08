//----------------------------------------Include the NodeMCU ESP8266 Library
//----------------------------------------see here: https://www.youtube.com/watch?v=8jMr94B8iN0 to add NodeMCU ESP12E ESP8266 library and board (ESP8266 Core SDK)
#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>

//----------------------------------------SSID and Password of your WiFi router.
const char* ssid = "wifi"; //--> Your wifi name or SSID.
const char* password = "7363591972"; //--> Your wifi password.
//----------------------------------------

//----------------------------------------Host & httpsPort
const char* host = "script.google.com";
const int httpsPort = 443;
//----------------------------------------

WiFiClientSecure client; //--> Create a WiFiClientSecure object.
String GAS_ID = "AKfycbwoNM_Du1hFoJ9U_M0emr9WmcZSY-x4_HodhrPQDcPCmUSGXj4PYhkkQxUonvJ6RxDq"; //--> spreadsheet script ID

int smoke_pin = A0;/* MQ2 O/P pin */
int flame_pin = 12;/* IR flame sensor D6*/
int buzzer = 4; /*Connected to D2 pin of NodeMCU*/
int smokeThres =200;
int flameThres=1;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(500);
  
  WiFi.begin(ssid, password); //--> Connect to your WiFi router
  Serial.println("");

  //----------------------------------------Wait for connection
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    //----------------------------------------Make the On Board Flashing LED on the process of connecting to the wifi router.
  }
  Serial.println("");
  Serial.print("Successfully connected to : ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.println();
  //----------------------------------------
  
  pinMode(smoke_pin,INPUT);
  pinMode(flame_pin,INPUT);
  pinMode(buzzer,OUTPUT);
  digitalWrite(buzzer, LOW);

  
  client.setInsecure();
}
//==============================================================================
//============================================================================== void loop
void loop() {
  // Reading smoke or flame takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  /* Read from IR flame*/
  float flameRead = digitalRead(flame_pin);
  float flame_val = flameRead;
  Serial.print("Flame Level = ");
  Serial.print(flame_val);
  Serial.print(" Flame \n");

  /* Read from MQ2 smoke sensor*/
  float smokeRead = analogRead(smoke_pin);
  float smoke_val= smokeRead;
  Serial.print("Smoke = ");
  Serial.print(smoke_val);
  Serial.print(" Units\n");  

  
  
  // Check if any reads failed and exit early (to try again).
  if (isnan(flame_val) || isnan(smoke_val)) {
    Serial.println("Failed to read from DHT sensor !");
    delay(500);
    return;
  }
  if(smoke_val>smokeThres && flame_val>flameThres){
    digitalWrite(buzzer, HIGH);
    delay(500);
    digitalWrite(buzzer, LOW);  
  }
  String Smoke = "smoke : " + String(smoke_val) + " °C";
  String Flame = "flame : " + String(flame_val) + " %";
  Serial.println(Smoke);
  Serial.println(Flame);
  
  sendData((int)smoke_val,(int)flame_val); //--> Calls the sendData Subroutine
}
//==============================================================================
//============================================================================== void sendData
// Subroutine for sending data to Google Sheets
void sendData(float smo, int fla) {
  Serial.println("==========");
  Serial.print("connecting to ");
  Serial.println(host);
  
  //----------------------------------------Connect to Google host
  if (!client.connect(host, httpsPort)) {
    Serial.println("connection failed");
    return;
  }
  //----------------------------------------

  //----------------------------------------Processing data and sending data
  String string_smoke =  String(smo);
  // String string_smoke =  String(smo, DEC); 
  String string_flame =  String(fla, DEC); 
  String url = "/macros/s/" + GAS_ID + "/exec?smoke1=" + string_smoke + "&flame1=" + string_flame;
  Serial.print("requesting URL: ");
  Serial.println(url);

  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
         "Host: " + host + "\r\n" +
         "User-Agent: BuildFailureDetectorESP8266\r\n" +
         "Connection: close\r\n\r\n");

  Serial.println("request sent");
  //----------------------------------------

  //----------------------------------------Checking whether the data was sent successfully or not
  while (client.connected()) {
    String line = client.readStringUntil('\n');
    if (line == "\r") {
      Serial.println("headers received");
      break;
    }
  }
  String line = client.readStringUntil('\n');
  Serial.println(line);
  if (line.startsWith("{\"state\":\"success\"")) {
    Serial.println("esp8266/Arduino CI successfull!");
  } else {
    Serial.println("esp8266/Arduino CI has failed");
  }
  Serial.print("reply was : ");
  Serial.println(line);
  Serial.println("closing connection");
  Serial.println("==========");
  Serial.println();
  delay(3000);//new code
  //----------------------------------------
} 
//==============================================================================
