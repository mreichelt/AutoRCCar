// assign pin num
int right_pin = 6;
int left_pin = 9;
int forward_pin = 5;
int reverse_pin = 3;
int ignition_pin = 10;
int horn_pin = 11;

// duration for output in milliseconds
const int time = 50;

void setup() {
  pinMode(right_pin, OUTPUT);
  pinMode(left_pin, OUTPUT);
  pinMode(forward_pin, OUTPUT);
  pinMode(reverse_pin, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  int command = 0;
  // receive command
  if (Serial.available() > 0){
    command = Serial.read();
  } else {
    reset();
  }
  send_command(command);
}

typedef enum {LEFT, STRAIGHT, RIGHT} Direction;
typedef enum {REVERSE, STOP, FORWARD} Throttle;

struct DriveCommand {
    Direction direction;
    Throttle throttle;
};

const DriveCommand C_LEFT = {.direction=LEFT, .throttle=STOP};
const DriveCommand C_RIGHT = {.direction=RIGHT, .throttle=STOP};
const DriveCommand C_FORWARD = {.direction=STRAIGHT, .throttle=FORWARD};
const DriveCommand C_REVERSE = {.direction=STRAIGHT, .throttle=REVERSE};
const DriveCommand C_FORWARD_LEFT = {.direction=LEFT, .throttle=FORWARD};
const DriveCommand C_FORWARD_RIGHT = {.direction=RIGHT, .throttle=FORWARD};
const DriveCommand C_REVERSE_LEFT = {.direction=LEFT, .throttle=REVERSE};
const DriveCommand C_REVERSE_RIGHT = {.direction=RIGHT, .throttle=REVERSE};

void sendDriveCommand(DriveCommand command);

void sendDriveCommand(DriveCommand command) {
  digitalWrite(right_pin, command.direction == RIGHT ? HIGH : LOW);
  digitalWrite(left_pin, command.direction == LEFT ? HIGH : LOW);
  digitalWrite(forward_pin, command.throttle == FORWARD ? HIGH : LOW);
  digitalWrite(reverse_pin, command.throttle == REVERSE ? HIGH : LOW);
  delay(time);
}

void ignition() {
  digitalWrite(ignition_pin, HIGH);
  delay(time);
  digitalWrite(ignition_pin, LOW);
  delay(time);
}

void horn() {
  digitalWrite(horn_pin, HIGH);
  delay(time);
  digitalWrite(horn_pin, LOW);
  delay(time);
}

void reset() {
  digitalWrite(right_pin, LOW);
  digitalWrite(left_pin, LOW);
  digitalWrite(forward_pin, LOW);
  digitalWrite(reverse_pin, LOW);
}

void send_command(int command){
  switch (command){

    // reset command
    case 0: reset(); break;

    // single command
    case 1: sendDriveCommand(C_FORWARD); break;
    case 2: sendDriveCommand(C_REVERSE); break;
    case 3: sendDriveCommand(C_RIGHT); break;
    case 4: sendDriveCommand(C_LEFT); break;

    // combination command
    case 6: sendDriveCommand(C_FORWARD_RIGHT); break;
    case 7: sendDriveCommand(C_FORWARD_LEFT); break;
    case 8: sendDriveCommand(C_REVERSE_RIGHT); break;
    case 9: sendDriveCommand(C_REVERSE_LEFT); break;

    // special commands
    case 11: ignition(); break;
    case 12: horn(); break;

    default: Serial.print("Invalid Command\n");
  }

}
