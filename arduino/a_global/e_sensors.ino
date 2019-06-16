// Sensors helper and control functions.

void ISR_encoderR() {
  encoders_counterR++;
}

void ISR_encoderL() {
  encoders_counterL++;
}
short send_sensors_data() {
  // @TODO: Implement this function.
  // is this an emergency break?
  short is_hard_stop = 0;
  return is_hard_stop;
}

float read_motors_speed(int motor) {
  float speed;
  if (motor == L_ENCODER) {
    speed = encoders_counterL / (TS * ENCODER_DISK_SLOTS);
    encoders_counterL = 0;
  } else {
    speed = encoders_counterR / (TS * ENCODER_DISK_SLOTS);
    encoders_counterR = 0;
   // @TODO Speed calculation formulas for right motors.
  }
  return speed * 1000; 
}
