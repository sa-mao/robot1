// Define global Constants:
#define SLAVE_ADDRESS 0x08

// Define ports mappings:
// Left Motor pins:
#define L_CTRL_1  5
#define L_CTRL_2 4
#define L_PWM 9
#define L_ENCODER 2

// Right Motor pins:
#define R_CTRL_1 6
#define R_CTRL_2 7
#define R_PWM 10
#define R_ENCODER 3

// Comm protocl constants:
#define MAX_COMMAND_ARGS_NUMBER  4
#define COMMANDS_EXECUTION_QUEUE_SIZE 10

// Encoders and wheels constants:
const float ENCODER_DISK_SLOTS = 20;
const float R_WHEEK_DIAMETER = 66.10; // @TODO: get the correct value.
const float L_WHEEK_DIAMETER = 66.10;

// Pid control constants:
const float TS = 100; // x millisecs.  // @TODO: PID Constol research. 

// Define global variables and counters:
// Define encoders pulse counters
volatile int encoders_counterR = 0;
volatile int encoders_counterL = 0;
