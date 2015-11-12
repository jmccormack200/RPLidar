#include <SPI.h>
#include <WiFi.h>
#include <WiFiUdp.h>

int status = WL_IDLE_STATUS;
char ssid[] = "";     //  your network SSID (name) 
char pass[] = "";    // your network password

unsigned int localPort = 2390;      // local port to listen on

char packetBuffer[255]; //buffer to hold incoming packet
char ReplyBuffer[] = "acknowledged";       // a string to send back
int  arrayAsInt = 0;

//For dimming/Buzzing
int led = 6;
int brightness = 0;
int fadeAmount = 3;
int count = 0;
int dimSpeed = 100;


WiFiUDP Udp;


void setup() {
  int count = 0;
  pinMode(led, OUTPUT);
  analogWrite(led, 0);
  
  //Initialize serial and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }

  // check for the presence of the shield:
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    // don't continue:
    while (true);
  }

  String fv = WiFi.firmwareVersion();
  if ( fv != "1.1.0" )
    Serial.println("Please upgrade the firmware");

  // attempt to connect to Wifi network:
  while ( status != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    status = WiFi.begin(ssid, pass);

    // wait 10 seconds for connection:
    delay(5000);
  }
  Serial.println("Connected to wifi");
  printWifiStatus();

  Serial.println("\nStarting connection to server...");
  // if you get a connection, report back via serial:
  Udp.begin(localPort);
}

void loop() {
  //Serial.print("Timer = ");
  //Serial.println(count);
  //Serial.print("Brightness = ");
  //Serial.println(brightness);
  count = count + 1;
  analogWrite(led, brightness);
  if (count >= dimSpeed and brightness > 5){
   brightness = brightness - fadeAmount;
   count = 0;
  } else if (count >= dimSpeed and brightness <=5) {
    brightness = 0;
    count = 0; 
  }
  
  // if there's data available, read a packet
  int packetSize = Udp.parsePacket();
  if (packetSize)
  {
    count = 0;
   
    IPAddress remoteIp = Udp.remoteIP();

    // read the packet into packetBufffer
    int len = Udp.read(packetBuffer, 255);
    if (len > 0) packetBuffer[len] = 0;
    arrayAsInt = atoi(packetBuffer);
    Serial.print("Array as Int = ");
    Serial.println(arrayAsInt);
    brightness = 255 - arrayAsInt / fadeAmount; 
  }
  
}


void printWifiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}
