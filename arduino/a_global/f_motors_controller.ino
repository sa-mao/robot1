// Motors helper and control functions.


void stop_motors() {
  digitalWrite(L_CTRL_1, HIGH);
  digitalWrite(L_CTRL_2, LOW);
  // Set forwoard
  digitalWrite(R_CTRL_1, HIGH);
  digitalWrite(R_CTRL_2, LOW);

  analogWrite(L_PWM, 0);
  analogWrite(R_PWM, 0);
}

void command_motors(int l_pmw_cmd, int r_pmw_cmd) {
  if (l_pmw_cmd < 0) {
    l_pmw_cmd = -1 * l_pmw_cmd;
    digitalWrite(L_CTRL_1, LOW);
    digitalWrite(L_CTRL_2, HIGH);
  } else {
    digitalWrite(L_CTRL_1, HIGH);
    digitalWrite(L_CTRL_2, LOW);
  }

  if (r_pmw_cmd < 0) {
    r_pmw_cmd = -1 * r_pmw_cmd;
    digitalWrite(R_CTRL_1, LOW);
    digitalWrite(R_CTRL_2, HIGH);
  } else {
    digitalWrite(R_CTRL_1, HIGH);
    digitalWrite(R_CTRL_2, LOW);
  }
  analogWrite(L_PWM, l_pmw_cmd);
  analogWrite(R_PWM, r_pmw_cmd);
}

void move_motors(int args[]) {
  int desired_speed_l = args[0];
  int desired_speed_r = args[1];
  int duration = args[2];
  float current_speed_l;
  float current_speed_r;
 
  int cycles = (int) duration / TS;
   
  while (cycles > 0) {
    cycles--;
    short is_hard_stop = send_sensors_data();
    if (is_hard_stop) {
      stop_motors();
    } else {
       Serial.print("L Motor Desired Speed: ");
       Serial.print(desired_speed_l);
       Serial.print(", L Motor Speed: "); 
       current_speed_l = read_motors_speed(L_ENCODER);
       Serial.print(current_speed_l);
       Serial.print("\n");
       
       Serial.print("R Motor Desired Speed: ");
       Serial.print(desired_speed_r);
       Serial.print(", R Motor Speed: "); 
       current_speed_r = read_motors_speed(R_ENCODER);
       Serial.print(current_speed_r); 
       Serial.print("\n");
       command_motors(desired_speed_l, desired_speed_r);
       delay(TS);   
    }
  }  
}
