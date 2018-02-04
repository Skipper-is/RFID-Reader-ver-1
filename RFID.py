import serial
import re
from tkinter import *
import threading
import winsound

# variables list
window = Tk()
threads = []
shutdown = False
#
seen = set()
serialPort = serial.Serial()


# functions list
def now():
    import datetime
    now = datetime.datetime.now()
    time = now.strftime("%d-%m-%y %H:%M:%S")
    return time


def remove_duplicates(inputlist):
    output = []

    for value in inputlist:
        if value not in seen and len(value) > 4:
            output.append("UK" + value)
            seen.add(value)
            write_toCSV(value)
            frequency = 2000
            duration = 300
            winsound.Beep(frequency, duration)
        elif value in seen and len(value) > 4:
            frequency = 1000
            duration = 500
            winsound.Beep(frequency, duration)
    return output


def write_toCSV(value):
    with open("list.csv", "a") as f:
        if len(value) > 4:
            f.write("UK" + value + "," + now() + "\n")


def split_string(i):
    if i != "":
        splitlist = re.split(r"[|_|\r]", i)
        for items in splitlist:
            if len(items) < 4:
                splitlist.remove(items)
                return splitlist
    else:
        return "error"


def serial_ports():
    if sys.platform.startswith('win'):
        # Windows based OS, we're happy!
        ports = ['COM%s' % (i + 1) for i in range(256)]
    else:
        raise EnvironmentError('Unsupported platform!')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass

    return result


def connectcomport(event):
    with serial.Serial(port=drop1_vars.get(), timeout=1) as ser:
        print("success!")
        ser.close()
        t = threading.Thread(target=read_data, args=(drop1_vars.get(),))
        threads.append(t)
        t.start()


def read_data(serial_port):
    with serial.Serial(port=serial_port, timeout=1) as ser:
        SerialPort = ser
        while True:
            response = ser.readline()
            response = response.decode("utf-8")

            if response != "":
                splitlist = split_string(response)
                splitlist = remove_duplicates(splitlist)
                if len(splitlist) > 0:
                    ewes.insert(END, splitlist[-1])

            if shutdown:
                break


def submit():
    pass

def clear():
    pass

window.title("RFID Reader ver 1")

# Lets make some items!

drop1_vars = StringVar()
comslist = serial_ports()
print(comslist)
if len(comslist) > 0:
    drop1_vars.set(comslist[0])
    drop1 = OptionMenu(window, drop1_vars, *comslist, command=connectcomport)
    drop1.grid(row=0, column=0)

if len(comslist) == 0:
    w = Label(window, text="No connections found")
    w.grid(row=0, column=0)

ewes = Listbox(window, height=5, width=40, selectmode = "SINGLE")
ewes.grid(row=1, column=1)

lambs = Listbox(window, height=5, width=40)
lambs.grid(row=1, column=4)

ewe_lable = Label(window, text="Ewes")
ewe_lable.grid(row=1, column=0)

lamb_lable = Label(window, text="Lambs")
lamb_lable.grid(row=1, column=3)

savebtn = Button(window, text="Save", command=submit)
savebtn.grid(row=2, column=0)

clearbtn = Button(window, text="Clear", command=clear)
clearbtn.grid(row=2, column=1, sticky=W)
print(serial_ports())
# Main script/body


window.mainloop()
shutdown = True
