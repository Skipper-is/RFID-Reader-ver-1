import serial
import re
from tkinter import *

#variables list
window = Tk()
fulllist = []
ser = serial.Serial( port = input("Enter comm number:"), timeout=1)
seen = set()

#functions list
def now():
    import datetime
    now = datetime.datetime.now()
    time = now.strftime("%d-%m-%y %H:%M:%S")
    return time

def remove_duplicates(inputlist):
    output = []

    for value in inputlist:
        if (value not in seen and len(value)>4):
            output.append(value)
            seen.add(value)
            write_toCSV(value)
    return output

def write_toCSV(value):
    with open("list.csv", "a") as f:
        if len(value)>4:
            f.write("UK"+value+","+now()+"\n")

def add_to_list(item):
	if item not in fulllist:
		fulllist.append(item)

	return fulllist

def split_string(i):
    if i != "":
        splitlist = re.split(r"[|_|\r]", i)
        for items in splitlist:
            if len(items) < 4:
                splitlist.remove(items)
                return splitlist
    else:
        return "error"

window.title("RFID Reader ver 1")

#Main script/body
while True:
    response = ser.readline()
    response=response.decode("utf-8")

    if response != "":
        splitlist = split_string(response)
        splitlist = remove_duplicates(splitlist)
        print(seen)


ser.close()
window.mainloop()
