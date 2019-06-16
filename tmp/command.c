#include <stdio.h>
#define MAX_COMMAND_ARGS_NUMBER  4
#define COMMANDS_EXECUTION_QUEUE_SIZE 10

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

int execution_queue_add(ExecutionQueue *exec_queue, Command command) {
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

void execution_queue_print(ExecutionQueue *exec_queue) {
  printf("start print queue: queue size %d\n", exec_queue->queue_size);
  for (int i = 0; i < exec_queue->queue_size; i++) {
    Command cmd = exec_queue->queue[i];
    printf("print queue: command %d, type: %d, first arg %f\n", cmd.command, cmd.type, cmd.args[0]);
  }
}


int main() {
  ExecutionQueue queue;
  

  Command cmd1 = {
    .command = STOP,
    .type = EMERGENCY 
  };
  cmd1.args[0] = 1;
  
  Command cmd2 = {
    .command = DATA_REQUEST,
    .type = NORMAL 
  };
  cmd2.args[0] = 2;
  
  Command cmd3 = {
    .command = SPEED_UPDATE,
    .type = NORMAL 
  };
  cmd3.args[0] = 3;
  execution_queue_add(&queue, cmd1);
  execution_queue_add(&queue, cmd2);
  execution_queue_add(&queue, cmd3);

  
  cmd3 = execution_queue_dequeue(&queue);
  cmd2 = execution_queue_dequeue(&queue);
  
  Command cmd4 = {
    .command = START,
    .type = NORMAL 
  };

  cmd4.args[0] = 4; 
  execution_queue_add(&queue, cmd4);

  printf("command1: command %d, type: %d, first arg %f\n", cmd1.command, cmd1.type, cmd1.args[0]);
  printf("command2: command %d, type: %d, first arg %f\n", cmd2.command, cmd2.type, cmd2.args[0]);
  printf("command3: command %d, type: %d, first arg %f\n", cmd3.command, cmd3.type, cmd3.args[0]);
  printf("command4: command %d, type: %d, first arg %f\n", cmd4.command, cmd4.type, cmd4.args[0]);
}


