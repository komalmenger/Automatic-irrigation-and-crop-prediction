#include <SoftwareSerial.h>
#include <dht.h>
#define SensorPin A0          // the pH meter Analog output is connected with the Arduino’s Analog
#define sensorPin A1
#define RX 2
#define TX 3
#define DHT11_PIN 7
dht DHT;
String AP = "komal1";// AP NAME
String PASS = "komal@15";//Password
String API = "BX7XSI7NGW3M65GY";   // Write API KEY
String HOST = "api.thingspeak.com";
String PORT = "80";
int countTrueCommand;
int countTimeCommand;
boolean found = false;
int sensorValue = 0;  
int percent = 0;
int ACWATERPUMP = 12;
unsigned long int avgValue;  //Store the average value of the sensor feedback
float b;
int buf[10],temp;

SoftwareSerial esp8266(RX,TX);
 
void setup() {
  Serial.begin(9600);
  Serial.println("Ready");    //Test the serial monitor
  pinMode(12,OUTPUT); //Set pin 12 OUTPUT pin, to send signal to relay
  esp8266.begin(115200);
  sendCommand("AT",5,"OK");
  sendCommand("AT+CWMODE=1",5,"OK");
  sendCommand("AT+CWJAP=\""+ AP +"\",\""+ PASS +"\"",20,"OK");
}

void loop() {
 
 String getData = "GET /update?api_key="+ API +"&field1="+getTemperatureValue()+"&field2="+getHumidityValue()+"&field3="+getPHValue()+"&field4="+getmoistureValue();
 sendCommand("AT+CIPMUX=1",5,"OK");
 sendCommand("AT+CIPSTART=0,\"TCP\",\""+ HOST +"\","+ PORT,15,"OK");
 sendCommand("AT+CIPSEND=0," +String(getData.length()+4),4,"OK");
 esp8266.println(getData);
 delay(1500);countTrueCommand++;
 sendCommand("AT+CIPCLOSE=0",5,"OK");
}

String getTemperatureValue(){
  int t = DHT.read11(DHT11_PIN);
  Serial.print("\nTemperature = ");
  int tem = DHT.temperature;
  Serial.println(tem);
  delay(1500);
  return String(tem);
}

String getHumidityValue(){

  int h = DHT.read11(DHT11_PIN);   
   Serial.print("\n Humidity= ");
   int humidity =DHT.humidity;
   Serial.println(humidity);
   delay(1500);
   return String(humidity);
 
}

String getPHValue(){
for(int i=0;i<10;i++)       //Get 10 sample value from the sensor for smooth the value
  { 
    buf[i]=analogRead(SensorPin);
    delay(10);
  }
  for(int i=0;i<9;i++)        //sort the analog from small to large
  {
    for(int j=i+1;j<10;j++)
    {
      if(buf[i]>buf[j])
      {
        temp=buf[i];
        buf[i]=buf[j];
        buf[j]=temp;
      }
    }
  }
  avgValue=0;
  for(int i=2;i<8;i++)                      //take the average value of 6 center sample prior(int i=2;i<8;i++)
    avgValue+=buf[i];
  float milliValue=(float)avgValue*3.0/1024/6; //convert the analog into millivolt (avgValue*5.0/1024/6)
  float phValue=3*milliValue;                      //convert the millivolt into pH value (3.5 prior)
  Serial.print("pH Value = ");  
  Serial.print(phValue,2);
  //Serial.println(" ");
  digitalWrite(13, HIGH);       
  delay(800);
  digitalWrite(13, LOW);
  return String(phValue);
}


String getmoistureValue(){
  sensorValue = analogRead(sensorPin);
  percent = convertToPercent(sensorValue);
  printValuesToSerial();
  delay(1000);

  if(percent < 100) 
  {
  digitalWrite(12,LOW); //if soil moisture sensor provides LOW value send LOW value to relay
  Serial.print("\nRelay low\n");
  }
  else
  {
  digitalWrite(12,HIGH); //if soil moisture sensor provides HIGH value send HIGH value to relay
  Serial.print("\nRelay high\n");
  }
  delay(400); //Wait for few second and then continue the loop.
  return String(percent);
}

int convertToPercent(int value)
{
  int percentValue = 0;
  percentValue = map(value, 1023, 465, 0, 100);
  return percentValue;
}

void printValuesToSerial()
{
  //Serial.print("\n\nAnalog Value: ");
  //Serial.print(sensorValue);
  Serial.print("\nMoisture Percent: ");
  Serial.print(percent);
  Serial.print("%");
}


void sendCommand(String command, int maxTime, char readReplay[]) {
  Serial.print(countTrueCommand);
  Serial.print(". at command => ");
  Serial.print(command);
  Serial.print(" ");
  while(countTimeCommand < (maxTime*1))
  {
    esp8266.println(command);//at+cipsend
    if(esp8266.find(readReplay))//ok
    {
      found = true;
      break;
    }
 
    countTimeCommand++;
  }
 
  if(found == true)
  {
    Serial.println("OYI");
    countTrueCommand++;
    countTimeCommand = 0;
  }
 
  if(found == false)
  {
    Serial.println("Fail");
    countTrueCommand = 0;
    countTimeCommand = 0;
  }
 
  found = false;
 }
