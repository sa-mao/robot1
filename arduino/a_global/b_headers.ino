#include <Wire.h>

// Setup data structures:

enum command_id{START, SPEED_UPDATE, STOP, DATA_REQUEST};
enum command_type{EMERGENCY, NORMAL};

typedef struct Command {
  enum command_id command;
  enum command_type type;
  float args[MAX_COMMAND_ARGS_NUMBER];
} Command;

typedef struct ExecutionQueue {
  int queue_size;
  Command queue[COMMANDS_EXECUTION_QUEUE_SIZE];  
} ExecutionQueue;

// Setup functions
void setup();
void setup_i2c();
void setup_motors();
void setup_sensors();

void loop();

// Sensors functions:
void ISR_encoderR();
void ISR_encoderL();
short send_sensors_data();
float read_motors_speed(int motor);

void stop_motors();
void command_motors(int l_pmw_cmd, int r_pmw_cmd);
void move_motors(int args[]);

// Communication protocol:
int execution_queue_add(struct ExecutionQueue *exec_queue, struct Command command);
Command execution_queue_dequeue(ExecutionQueue *exec_queue);
void receiveEvent(int howMany);
