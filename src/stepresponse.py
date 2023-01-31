"""!
@file stepresponse.py


@author Miloh Padgett, Tristan Cavarno, Jon Abraham
@date 30-Jan-2023 Original File
"""

import serial
from matplotlib import pyplot


#Send characters through USB and read output
def steptest(Kp):
    kp = bytes(Kp, 'utf-8')
    data = []
    with serial.Serial ('COMx', 115200) as s_port:
           s_port.write (kp)                             #send characters
           while(s_port.readline()):
                 line = s_port.readline().split (b',')   #read data
                 data.append(line)
    return data

#Plot response data
def plotresponse(data):
    Time = []
    Position = []
    for row in data:
        try:
            Time.append(float(row[0]))
            try:
                Position.append(float(row[1]))
            except:             
                Time.pop()
        except:
            continue
    
    #Plot step response
    pyplot.plot(Time, Position)
    pyplot.xlabel('Time')
    pyplot.ylabel('Position)

def main():
    steptest(Kp)
    plotresponse()

if __name__ == "__main__":
    main()