"""!
@file stepresponse.py
This file runs step response tests by sending
characters through the USB serial port, reading the data sent back,
and plotting the output.

TODO: Create a function to set up serial communication with the board

TODO: Plot the step responses with properly labeled axes and a title

@author Miloh Padgett, Tristan Cavarno, Jon Abraham
@date 30-Jan-2023 Original File
"""

import serial
from matplotlib import pyplot


#Send characters through USB and read output
def steptest(Kp: str):
    """!
    Input a Kp value, send to the board through serial, and return the encoder data.
    @param Kp	String containing the desired Kp value and a carriage return
    @returns A list of lists for each encoder reading, each containing a Time and Position
    """
    data = []
    #Open serial port
    with serial.Serial ('/dev/ttyACM0', 115200,timeout=6) as s_port:
           print(f"Sending kp {Kp}")
           #Send Kp using UTF-8 encoding
           s_port.write(Kp.encode())
           byte_ = 1
           msg = ""
           
           # Read the data sent from the controller while valid data is buffered and split into lists
           while(byte_):
                 byte_ = s_port.readline()
                 #Decode data into a string and print
                 msg = byte_.decode()
                 print(msg)
                 #Split by comma delimiter and store if valid
                 line = msg.strip().split (',')   
                 if(len(line) == 2):
                    data.append(line)
    return data


def plotresponse(data):
    """!
    Convert the data to floats and plot on properly labeled axes.
    @param data		Input data 
    """
    #Convert binary array into separate float lists of Time and Position
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
    """!
    Sets a Kp value, runs the step response function, then prints and plots the data.
    """
    Kp = ".01\r"
    data = steptest(str(Kp))
    print(data)
    plotresponse(data)

if __name__ == "__main__":
    main()