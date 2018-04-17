import time

import serial_util
from serial_util import *


def main():
    car = select_car()

    seq = [getattr(serial_util, name.strip().upper().replace(" ", "_") + "_BYTE") for name in
           input("Pattern: ").split(",")]
    send_sequence(car, seq, -1)


def send_sequence(car, seq, count=-1):
    ind = 0
    while True:
        ind = (ind + 1) % len(seq)
        car.write_single_byte(seq[ind])
        print(ind)
        time.sleep(.1)
        if ind > count > 0:
            return


if __name__ == '__main__':
    send_sequence(select_car(),
                  [FORWARD_BYTE, FORWARD_BYTE, RESET_BYTE, RESET_BYTE, ])
    main()
