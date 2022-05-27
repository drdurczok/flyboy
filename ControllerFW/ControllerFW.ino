bool message[6] = {0,0,0,0,0,0};
// 2-bit ID, 4-bit button states
#define Pin_Sens_RB 12
#define Pin_Sens_RT 13
#define Pin_Sens_LB 4
#define Pin_Sens_LT 5

bool Sens_RB_active = false;
bool Sens_RT_active = false;
bool Sens_LB_active = false;
bool Sens_LT_active = false;

void setup() { 
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(Pin_Sens_RB, INPUT);
  pinMode(Pin_Sens_RT, INPUT);
  pinMode(Pin_Sens_LB, INPUT);
  pinMode(Pin_Sens_LT, INPUT);

  Serial.begin(115200);
  Serial.println("Begin");
}

void loop() {
  check_sensor(Pin_Sens_RB, &Sens_RB_active);
  check_sensor(Pin_Sens_RT, &Sens_RT_active);
  check_sensor(Pin_Sens_LB, &Sens_LB_active);
  check_sensor(Pin_Sens_LT, &Sens_LT_active);

  delay(50);
}

void check_sensor(int pin, bool* state){
  int value = analogRead(pin);
  if (value > 500 && *state == false){
    *state = true;
    set_button(pin, true);
  }
  else if (value <= 500 && *state == true){
    *state = false;
    set_button(pin, false);
  }
}

void set_button(int pin, bool state){
  if (pin == Pin_Sens_RB){
    message[2] = state;
  }
  else if (pin == Pin_Sens_RT){
    message[3] = state;
  }
  else if (pin == Pin_Sens_LB){
    message[4] = state;
  }
  else if (pin == Pin_Sens_LT){
    message[5] = state;
  }
  send_message();
}

void send_message(){
  for(int i = 0; i < 6; i++){
    Serial.print(message[i]);
  }
  Serial.println();
}
