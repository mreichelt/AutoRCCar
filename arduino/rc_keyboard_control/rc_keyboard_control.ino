// assign pin num
int right_pin = 6;
int left_pin = 9;
int forward_pin = 5;
int reverse_pin = 3;
int ignition_pin = 10;
int horn_pin = 11;

// duration for output
const int time = 50;

// initial command
int command = 0;

void setup() {
  pinMode(right_pin, OUTPUT);
  pinMode(left_pin, OUTPUT);
  pinMode(forward_pin, OUTPUT);
  pinMode(reverse_pin, OUTPUT);
  Serial.begin(115200);
}

void loop() {
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

typedef struct {
    Direction direction;
    Throttle throttle;
} DriveCommand;

void sendDriveCommand(DriveCommand command) {
  digitalWrite(right_pin, command.direction == RIGHT ? HIGH : LOW);
  digitalWrite(left_pin, command.direction == LEFT ? HIGH : LOW);
  digitalWrite(forward_pin, command.throttle == FORWARD ? HIGH : LOW);
  digitalWrite(reverse_pin, command.throttle == REVERSE ? HIGH : LOW);
  delay(time);
}

void right() {
  sendDriveCommand((DriveCommand) {.direction=RIGHT, .throttle=STOP});
}

void left() {
  sendDriveCommand((DriveCommand) {.direction=LEFT, .throttle=STOP});
}

void forward() {
  sendDriveCommand((DriveCommand) {.direction=STRAIGHT, .throttle=FORWARD});
}

void reverse() {
  sendDriveCommand((DriveCommand) {.direction=STRAIGHT, .throttle=REVERSE});
}

void forward_right() {
  sendDriveCommand((DriveCommand) {.direction=RIGHT, .throttle=FORWARD});
}

void reverse_right() {
  sendDriveCommand((DriveCommand) {.direction=RIGHT, .throttle=REVERSE});
}

void forward_left() {
  sendDriveCommand((DriveCommand) {.direction=LEFT, .throttle=FORWARD});
}

void reverse_left() {
  sendDriveCommand((DriveCommand) {.direction=LEFT, .throttle=REVERSE});
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
    case 1: forward(); break;
    case 2: reverse(); break;
    case 3: right(); break;
    case 4: left(); break;

    // combination command
    case 6: forward_right(); break;
    case 7: forward_left(); break;
    case 8: reverse_right(); break;
    case 9: reverse_left(); break;

    // special commands
    case 11: ignition(); break;
    case 12: horn(); break;

    default: Serial.print("Invalid Command\n");
  }

}
