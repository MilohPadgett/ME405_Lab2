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
    with serial.Serial ('/dev/ttyACM0', 115200,timeout=6) as s_port:
           print(f"Sending kp {Kp}")
           s_port.write(Kp.encode())                             #send characters
           byte_ = 1
           msg = ""
           while(byte_):
                 byte_ = s_port.readline()
                 msg = byte_.decode()
                 print(msg)
                 line = msg.strip().split (',')   #read data
                 if(len(line) == 2):
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
    pyplot.xlabel('Time (ms)')
    pyplot.ylabel('Position (encoder pulses)')
    pyplot.title("Position vs Time")
    pyplot.show()

def main():
    Kp = ".01\r"
    data = steptest(str(Kp))
    print(data)
    plotresponse(data)

if __name__ == "__main__":
    main()