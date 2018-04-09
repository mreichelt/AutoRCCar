import glob
import serial

FORWARD_BYTE = 1
REVERSE_BYTE = 2
RIGHT_BYTE = 3
LEFT_BYTE = 4

FORWARD_RIGHT_BYTE = 6
FORWARD_LEFT_BYTE = 7
REVERSE_RIGHT_BYTE = 8
REVERSE_LEFT_BYTE = 9

RESET_BYTE = 0


class CarControl(serial.Serial):

    # Normal movement

    def forward(self):
        self.write_single_byte(FORWARD_BYTE)

    def reverse(self):
        self.write_single_byte(REVERSE_BYTE)

    def right(self):
        self.write_single_byte(RIGHT_BYTE)

    def left(self):
        self.write_single_byte(LEFT_BYTE)

    # Complex movements

    def forward_right(self):
        self.write_single_byte(FORWARD_RIGHT_BYTE)

    def forward_left(self):
        self.write_single_byte(FORWARD_LEFT_BYTE)

    def reverse_right(self):
        self.write_single_byte(REVERSE_RIGHT_BYTE)

    def reverse_left(self):
        self.write_single_byte(REVERSE_LEFT_BYTE)

    # Reset

    def reset_car(self):
        self.write_single_byte(RESET_BYTE)

    # Util

    def write_single_byte(self, byte):
        self.write(bytes([byte]))


def select_car():
    choice = select_usbmodem()
    return CarControl(choice, 115200, timeout=1)


def select_usbmodem():
    usbs = glob.glob('/dev/tty.usbmodem*')
    print("Choose an USB post for the serial")
    for i in range(len(usbs)):
        print(i, usbs[i])
    inp = -1
    while not (0 <= inp < len(usbs)):
        try:
            inp = int(input())
        except ValueError:
            pass

    return usbs[inp]
