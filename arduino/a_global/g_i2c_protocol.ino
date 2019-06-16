#include <stdio.h>

int execution_queue_add(struct ExecutionQueue *exec_queue, struct Command command) {
  Command cmd = command;
  if (exec_queue->queue_size >= COMMANDS_EXECUTION_QUEUE_SIZE) {
    // We cannot add further to the queue
    return -1;
  }
  exec_queue->queue[exec_queue->queue_size] = cmd;
  exec_queue->queue_size++;
  return 0;
}

Command execution_queue_dequeue(ExecutionQueue *exec_queue) {
  Command result;
  if (exec_queue->queue_size > 0) {
    //Queue is not empty
    exec_queue->queue_size--;
    result = exec_queue->queue[exec_queue->queue_size];
  }
  return result;
}

void receiveEvent(int howMany) {
  int sizeReceived = Wire.available();
  // Receive at least two byes or do nothing
  
  if (sizeReceived < 2) {
     return;
  }
  
  int argSize = (sizeReceived - 2)/ 4;

  // Command Structure
  byte command;
  byte type;
  float args[argSize];

  int i = 0; 

  while (0 < Wire.available()) {
    switch (i) {
      case 0:
        type = Wire.read();
        i+=1;
        break;
      case 1:
        command = Wire.read();
        i+=1;
        break;
      case 2:
        break;
        
    }
  }
  
  
  while (1 < Wire.available()) { // loop through all but the last
    char c = Wire.read(); // receive byte as a character
    Serial.print(c);         // print the character
  }
  int x = Wire.read();    // receive byte as an integer
  Serial.println(x);         // print the integer
}
