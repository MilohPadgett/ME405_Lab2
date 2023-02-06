"""!
@file stepresponse.py


@author Miloh Padgett, Tristan Cavarno, Jon Abraham
@date 30-Jan-2023 Original File
"""

import serial
from matplotlib import pyplot


#Send characters through USB and read output
def steptest(Kp: str):
    data = []
    with serial.Serial ('/dev/ttyACM0', 115200) as s_port:
           print(f"Sending kp {Kp}")
           s_port.write(Kp.encode())                             #send characters
           while(s_port.readline()):
                 data = s_port.readline()
                 print(data.decode())
                 line = data.split (b',')   #read data
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
    pyplot.ylabel('Position')

def main():
    Kp = .035
    data = steptest(str(Kp))
    plotresponse(data)

if __name__ == "__main__":
    main()