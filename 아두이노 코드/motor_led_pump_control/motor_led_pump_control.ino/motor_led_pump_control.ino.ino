#define RELAY_PIN1  9
#define RELAY_PIN2  10
#define RELAY_PIN3  11
#define RELAY_ON  LOW
#define RELAY_OFF HIGH
// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(RELAY_PIN1, OUTPUT);
  pinMode(RELAY_PIN2, OUTPUT);
  pinMode(RELAY_PIN3, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  // pwm 0~255
  activate_control(RELAY_ON,RELAY_OFF,RELAY_OFF);
  delay(1000);            
  activate_control(RELAY_OFF,RELAY_ON,RELAY_OFF);
  delay(1000);            
  activate_control(RELAY_OFF,RELAY_OFF,RELAY_ON);
  delay(1000);            
}

void activate_control(int LED, int water, int moter){
  digitalWrite(RELAY_PIN1, LED); 
  digitalWrite(RELAY_PIN2, water); 
  digitalWrite(RELAY_PIN3, moter);
}
