bool message[8] = {0,0,0,0,0,0,0,0};
// 2-bit ID, 3-bit speed, 1-bit dir up, 1-bit dir down, 1-bit menu

void setup() { 
  pinMode (LED_BUILTIN, OUTPUT);

  Serial.begin(115200);
}

void loop() {
  set_speed(3); 011
  send_message();
  delay(1000);

  set_speed(6); 110
  send_message();
  delay(1000);
}

void send_message(){
  for(int i = 0; i < 8; i++){
    Serial.print(message[i]);
  }
  Serial.println();
}

void set_speed(int spd){
  if (spd < 8){
    message[2] = 0;
    message[3] = 0;
    message[4] = 0;
    
    int spd_reszta = 0;
    int spd_dzielone = 0;

    if (spd != 0){
      spd_reszta = spd % 2;
      spd_dzielone = spd / 2;
      message[2] = spd_reszta;
    }

    if (spd_dzielone != 0){
      spd_reszta = spd_dzielone % 2;
      spd_dzielone = spd_dzielone / 2;
      message[3] = spd_reszta;
    }

    if (spd_dzielone != 0){
      spd_reszta = spd_dzielone % 2;
      spd_dzielone = spd_dzielone / 2;
      message[4] = spd_reszta;
    }
  
    send_message();
  }
  else{
    //Spd too big!!!
  }
}

void set_dir_up(bool engage){
    message[5] = engage;
    send_message();
}

void set_dir_down(bool engage){
    message[6] = engage;
    send_message();
}

void set_menu(bool engage){
    message[7] = engage;
    send_message();
}
