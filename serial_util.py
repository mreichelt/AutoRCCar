import glob


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
