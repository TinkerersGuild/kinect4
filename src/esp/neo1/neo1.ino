// NeoPixel Ring simple sketch (c) 2013 Shae Erisson
// released under the GPLv3 license to match the rest of the AdaFruit NeoPixel library

#include <Adafruit_NeoPixel.h>
#include <ESP8266WiFi.h>

const char* ssid = "lynx";
const char* password = "FishFish";
const char* gameserver = "192.168.1.112";
int gameport = 5000;
// Create an instance of the server
// specify the port to listen on as an argument
WiFiServer server(80);

// Which pin on the Arduino is connected to the NeoPixels?
// On a Trinket or Gemma we suggest changing this to 1
#define PIN            2

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS      16

// When we setup the NeoPixel library, we tell it how many pixels, and which pin to use to send signals.
// Note that for older NeoPixel strips you might need to change the third parameter--see the strandtest
// example for more information on possible values.
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

 
int RED = pixels.Color(150,0,0);
int GREEN = pixels.Color(0,150,0);
int BLUE = pixels.Color(0, 0, 150);
int YELLOW = pixels.Color(150, 150, 0);

int myColors[4] = {RED, GREEN, BLUE, YELLOW};

int delayval = 500; // delay for half a second
int colchange = 0;
int col = RED;


int reg_client(){
  WiFiClient client;


  if (client.connect(gameserver, gameport)) {
    

    String s = "GET /register?ID=";
    s += WiFi.macAddress();
    client.println(s);
    
    return 1;
   
   }
  return 0;


}

void setup() {

  pixels.begin(); // This initializes the NeoPixel library.
  pixels.setPixelColor(0, RED); // Moderately bright red color.
  pixels.setPixelColor(1, RED);
  pixels.show(); // This sends the updated pixel color to the hardware.


  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    
  }
  
  if (reg_client()){
    pixels.setPixelColor(1, GREEN); // Moderately bright green color.
    pixels.show(); // This sends the updated pixel color to the hardware.
  }
  server.begin();
}

void loop() {

 WiFiClient client = server.available();
  if (!client) {
    return;
  }
  
  
  // Wait until the client sends some data
  while(!client.available()){
    delay(1);
  }
  
  // Read the first line of the request
  String req = client.readStringUntil('\r');

  String s = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE HTML>\r\n<html>\r\nOk, set ";
  s += req;
  client.flush();


// Request is formatted for a URL, but it's "telnet compatible"
  int colpos = req.indexOf("/col/");
  if ( colpos != -1){
    s += "<br/> New color at ";
    s += colpos;
    int newcol = req.charAt(colpos + 5) - 48;
    s += newcol;
    s += "<br/>";
    col = myColors[newcol];
    colchange = 1;


  }else{
    colchange = 0;
  }
  
  if (colchange == 1){
  for(int i=0;i<NUMPIXELS;i++){

    // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
    pixels.setPixelColor(i, col); // Moderately bright green color.
    }
  pixels.show(); // This sends the updated pixel color to the hardware.


  }

    
  
 
  s += "</html>\n";

  // Send the response to the client
  client.print(s);
  delay(1);
}



