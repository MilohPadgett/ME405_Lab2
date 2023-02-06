"""!
@file ClosedLoopController.py
This file contains a class to implement a Closed Loop P Controller

TODO: Create a constructor which sets the proportional gain, initial setpoint, and other necessary parameters.

TODO: Create a method run() which is called repeatedly to run the control algorithm.
      This method should accept as parameters the setpoint and measured output.
      It should return an actuation value which is sent to a motor in this lab but might be sent to another device in another instance, as this is a generic controller.

TODO: The run() method should not contain a loop and should not print the results of its running; those things go in your main code.

TODO: A method set_setpoint() to set the setpoint.

TODO: A method set_Kp() to set the control gain.

@author Miloh Padgett, Tristan Cavarno, Jon Abraham
@date 30-Jan-2023 Original File
"""

import pyb 
import utime
class PController:
    '''!
    @param gain 
    @param setpoint
    '''
    def __init__(self, gain, target):
        self.gain = gain
        self.target = target
        self.times = []
        self.ticks = []
        self.time_start = None

    def run(self, actual):
        if self.time_start == None:
            self.time_start = utime.ticks_ms()
            self.times.append(0)
            self.ticks.append(actual)
        else:
            self.times.append(utime.ticks_ms()-self.time_start)
            self.ticks.append(actual)
        err = self.target - actual
        return max(min(self.gain*err,100),-100)

    def set_setpoint(self, new_target):
        self.target = new_target

    def set_Kp(self, new_gain):
        self.gain = new_gain

    def get_response(self):
        for i in range(len(self.times)):
            print(f"{self.times[i]},{self.ticks[i]}")


    def reset_response(self):
        self.times = []
        self.ticks = []
        self.time_start = None