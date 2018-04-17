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
  //receive command
  if (Serial.available() > 0){
    command = Serial.read();
  } else {
    reset();
  }
  send_command(command);
}

void right(){
  digitalWrite(right_pin, HIGH);
  digitalWrite(left_pin, LOW);
  digitalWrite(forward_pin, LOW);
  digitalWrite(reverse_pin, LOW);
  delay(time);
}

void left(){
  digitalWrite(right_pin, LOW);
  digitalWrite(left_pin, HIGH);
  digitalWrite(forward_pin, LOW);
  digitalWrite(reverse_pin, LOW);
  delay(time);
}

void forward(){
  digitalWrite(right_pin, LOW);
  digitalWrite(left_pin, LOW);
  digitalWrite(forward_pin, HIGH);
  digitalWrite(reverse_pin, LOW);
  delay(time);
}

void reverse(){
  digitalWrite(right_pin, LOW);
  digitalWrite(left_pin, LOW);
  digitalWrite(forward_pin, LOW);
  digitalWrite(reverse_pin, HIGH);
  delay(time);
}

void forward_right(){
  digitalWrite(right_pin, HIGH);
  digitalWrite(left_pin, LOW);
  digitalWrite(forward_pin, HIGH);
  digitalWrite(reverse_pin, LOW);
  delay(time);
}

void reverse_right(){
  digitalWrite(right_pin, HIGH);
  digitalWrite(left_pin, LOW);
  digitalWrite(forward_pin, LOW);
  digitalWrite(reverse_pin, HIGH);
  delay(time);
}

void forward_left(){
  digitalWrite(right_pin, LOW);
  digitalWrite(left_pin, HIGH);
  digitalWrite(forward_pin, HIGH);
  digitalWrite(reverse_pin, LOW);
  delay(time);
}

void reverse_left(){
  digitalWrite(right_pin, LOW);
  digitalWrite(left_pin, HIGH);
  digitalWrite(forward_pin, LOW);
  digitalWrite(reverse_pin, HIGH);
  delay(time);
}

void ignition() {
  digitalWrite(ignition_pin, HIGH);
  delay(time);
  digitalWrite(ignition_pin, LOW);
}

void horn() {
  digitalWrite(horn_pin, HIGH);
  delay(time);
  digitalWrite(horn_pin, LOW);
}

void reset(){
  digitalWrite(right_pin, LOW);
  digitalWrite(left_pin, LOW);
  digitalWrite(forward_pin, LOW);
  digitalWrite(reverse_pin, LOW);
}

void send_command(int command){
  switch (command){

    //reset command
    case 0: reset(); break;

    // single command
    case 1: forward(); break;
    case 2: reverse(); break;
    case 3: right(); break;
    case 4: left(); break;

    //combination command
    case 6: forward_right(); break;
    case 7: forward_left(); break;
    case 8: reverse_right(); break;
    case 9: reverse_left(); break;

    // special commands
    case 11:ignition(); break;
    case 12:horn(); break;

    default: Serial.print("Invalid Command\n");
  }

}
