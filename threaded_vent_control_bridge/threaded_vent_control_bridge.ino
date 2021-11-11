int O2pin = 3; //PJN - set pins as needed
int N2pin = 4;
int HPpin = 5;
int MRtrigPin = 7;
int ExhalePin = 6;
int HPmodePin = 28; //I don't think I understand this one... Will have to examine
int PTreadPin = 3;


unsigned long currentMillis = 0;    // stores the value of millis() in each iteration of loop()
unsigned long previousInhaleMillis = 0;   // will store last time the LED was updated
unsigned long previousExhaleMillis = 0;
unsigned long previousTriggerMillis = 0;
unsigned long previousCycleMillis = 0;
unsigned long inhaleStart = 0;
unsigned long breathholdStart = 0;

unsigned long lastCycle = 1;

int inDur = 150;
int holdDur = 100;
int bpm = 80;
int HPyes = 0;
int TriggerStart = 65;
int TriggerDur = 10;

unsigned long cycleDur;
int cycleCount = 0;

void setup() {
  Serial.begin(9600);
  pinMode(O2pin, OUTPUT);
  pinMode(N2pin, OUTPUT);
  pinMode(HPpin, OUTPUT);
  pinMode(MRtrigPin, OUTPUT);
  pinMode(ExhalePin, OUTPUT);
  
  while (!Serial.available());
  Serial.println("Receiving values from python");
  String str1 = Serial.readString();
  //Need to pass 6 pieces of data - use 5 commas
  int ind1 = str1.indexOf(',');
  int ind2 = str1.indexOf(',',ind1+1);
  int ind3 = str1.indexOf(',',ind2+1);
  int ind4 = str1.indexOf(',',ind3+1);
  int ind5 = str1.indexOf(',',ind4+1);
  inDur = str1.substring(0,ind1).toInt();
  holdDur = str1.substring(ind1+1,ind2).toInt();
  bpm = str1.substring(ind2+1,ind3).toInt();
  HPyes = str1.substring(ind3+1,ind4).toInt();
  TriggerStart = str1.substring(ind4+1,ind5).toInt();
  TriggerDur = str1.substring(ind5+1).toInt();
  Serial.println("Values from Serial");
  Serial.println(String(inDur));
  Serial.println(String(holdDur));
  Serial.println(String(bpm));
  Serial.println(String(HPyes));
  Serial.println(String(TriggerStart));
  Serial.println(String(TriggerDur));
  Serial.println("End Values from Serial");
  cycleDur = (unsigned long) 60000/bpm;
}

void loop() {
  // put your main code here, to run repeatedly:
  currentMillis = millis(); // Read clock

  readADC(); // Read ADC every cycle. Takes 112 us.
  //I want the ability to read the ADC without actuating valves - Just pass inDur = 0 to do so
  if(inDur !=0)
  {
    updateCycle(); //Check what cycle we're on
    updateInhale();
    updateBreathhold();
    updateExhale();
    updateTrigger();
  }
}

void readADC()
{
  float data = analogRead(A0);
  data = (data/1024.00) * 5;
  String dataToSend = String(data);
  Serial.println(dataToSend);
}

// Work by cycles - makes it easy to time inhale
void updateCycle()
{
  if (currentMillis - previousCycleMillis >= cycleDur)
  {
    previousCycleMillis = currentMillis;
    cycleCount += 1;
  }
}

// Function to initiate inhale - if starting a new cycle, turn on inhale
// Everything will be timed from inhaleStart
void updateInhale()
{
  //simple method to get started
  if(cycleCount == 0)
  {
    cycleCount = 1;
    inhaleStart = currentMillis;
    if(HPyes)
    {
      HPInhale();
    }
    else
    {
      N2Inhale();
    }
  }
  else if(cycleCount > lastCycle)
  {
    lastCycle = cycleCount;
    inhaleStart = currentMillis;
    if(HPyes)
    {
      HPInhale();
    }
    else
    {
      N2Inhale();
    }
  }
}

void updateBreathhold()
{
  if((currentMillis - inhaleStart) >= inDur)
  {
    Breathhold();
  }
}

void updateExhale()
{
  if((currentMillis - inhaleStart) >= (inDur + holdDur))
  {
    Exhale();
  }
}

void updateTrigger()
{
  if((currentMillis - inhaleStart) >= TriggerStart)
  {
    TriggerOn();
  }
  if((currentMillis - inhaleStart) >= (TriggerStart + TriggerDur))
  {
    TriggerOff();
  }
}

// Functions to control inhale, breathhold, exhale, and trigger
void N2Inhale()
{
  digitalWrite(O2pin, HIGH);  
  digitalWrite(N2pin, HIGH);
  digitalWrite(HPpin, LOW);  
  digitalWrite(ExhalePin, LOW);
}

void HPInhale()
{
  digitalWrite(O2pin, HIGH);  
  digitalWrite(N2pin, LOW);
  digitalWrite(HPpin, HIGH);  
  digitalWrite(ExhalePin, LOW);
}

void Breathhold()
{
  digitalWrite(O2pin, LOW);  
  digitalWrite(N2pin, LOW);
  digitalWrite(HPpin, LOW);  
  digitalWrite(ExhalePin, LOW);
}

void Exhale()
{
  digitalWrite(O2pin, LOW);  
  digitalWrite(N2pin, LOW);
  digitalWrite(HPpin, LOW);  
  digitalWrite(ExhalePin, HIGH);
}

void TriggerOn()
{
  digitalWrite(MRtrigPin, LOW);
}

void TriggerOff()
{
  digitalWrite(MRtrigPin, HIGH);
}
