void setup_i2c() {
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveEvent);
  //Wire.onRequest(requestEvent);
}
void setup_encoders() {
  pinMode(R_ENCODER, INPUT_PULLUP); 
  pinMode(L_ENCODER, INPUT_PULLUP); 
  attachInterrupt(digitalPinToInterrupt(R_ENCODER), ISR_encoderR, RISING);
  attachInterrupt(digitalPinToInterrupt(L_ENCODER), ISR_encoderL, RISING);
}

void setup_motors() {
  pinMode(L_PWM, OUTPUT);
  pinMode(R_PWM, OUTPUT);
  
  pinMode(L_CTRL_1, OUTPUT);
  pinMode(L_CTRL_2, OUTPUT);

  pinMode(R_CTRL_1, OUTPUT);
  pinMode(R_CTRL_2, OUTPUT);
 
  //stop_motors();  
}

void setup_sensors() {
  // Blank so far. 
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  setup_encoders();
  setup_motors();
  setup_sensors();
  setup_i2c();
}
