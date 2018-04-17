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

    # Normal movements

    def forward(self):
        self.write_single_byte(RESET_BYTE)
        self.write_single_byte(FORWARD_BYTE)

    def reverse(self):
        self.write_single_byte(RESET_BYTE)
        self.write_single_byte(REVERSE_BYTE)

    def right(self):
        self.write_single_byte(RESET_BYTE)
        self.write_single_byte(RIGHT_BYTE)

    def left(self):
        self.write_single_byte(RESET_BYTE)
        self.write_single_byte(LEFT_BYTE)

    # Complex movements

    def forward_right(self):
        self.write_single_byte(RESET_BYTE)
        self.write_single_byte(FORWARD_RIGHT_BYTE)

    def forward_left(self):
        self.write_single_byte(RESET_BYTE)
        self.write_single_byte(FORWARD_LEFT_BYTE)

    def reverse_right(self):
        self.write_single_byte(RESET_BYTE)
        self.write_single_byte(REVERSE_RIGHT_BYTE)

    def reverse_left(self):
        self.write_single_byte(RESET_BYTE)
        self.write_single_byte(REVERSE_LEFT_BYTE)

    # Reset

    def reset_car(self):
        self.write_single_byte(RESET_BYTE)

    # Util

    def write_single_byte(self, byte):
        self.write(bytes([byte]))


def select_car():
    usb_device = select_usbmodem()
    return CarControl(usb_device, 115200, timeout=1)


def select_usbmodem():
    usb_devices = glob.glob('/dev/tty.usbmodem*')
    if len(usb_devices) == 0:
        print('Only one usbdevie found: %s. Using that one.' % usb_devices[0])
        return usb_devices[0]
    print("Choose an USB port for the serial")
    for i, usb_device in enumerate(usb_devices):
        print(i, usb_device)
    selection = -1
    while not 0 <= selection < len(usb_devices):
        try:
            selection = int(input())
        except ValueError:
            pass

    return usb_devices[selection]
