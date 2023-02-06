"""!
@file main.py
This file sets up the motor driver, controller, and encoder, causing them to run step response tests when prompted.

TODO: Create a function that runs a closed-loop step response test to rotate the motor about one revolution
      and stop it at the final position. The controller runs every 10ms.
      
TODO: Run a loop that waits for a user inputted Kp value then runs the step response test.

@author Miloh Padgett, Tristan Cavarno, Jon Abraham
@date 30-Jan-2023 Original File
"""

import utime
import pyb
from ClosedLoopContoller import PController
from EncoderReader import EncoderReader
from MotorDriver import MotorDriver

def rotation_test(motor: MotorDriver, encoder: EncoderReader):
    """!
    Runs a test for a predetermined Kp and setpoint
    @param motor	MotorDriver object
    @param encoder	EncoderReader object
    """
    #Create controller object with set Kp and setpoint
    controller = PController(0.03, 5000.0)
    while(1):
        #Read encoder 
        encoder.read()
        actual = encoder.ticks
        #Calculate new duty cycle
        speeeed = controller.run(actual)
        #Set duty cycle
        motor.set_duty_cycle(speeeed)
        #print(f"Actual: {actual}")
        utime.sleep_ms(10)

def get_kp_input():
    """!
    Polls user to get input Kp value.
    """
    Kp = input("Please input a value Kp (float): ")
    try:
        return float(Kp)
    except:
        print("ERROR: Bad input")
        return get_kp_input()

def control_test(motor: MotorDriver, encoder: EncoderReader):
    """!
    Runs closed-loop step response test for a predetermined setpoint by taking in a Kp and getting the controller response
    @param motor	MotorDriver object
    @param encoder	EncoderReader object
    """
    #Poll for Kp input
    Kp = get_kp_input()
    #Create controller with predetermined setpoint and input Kp
    controller = PController(Kp,1050.0)
    #Initialize start time, current time, duty cycle, and encoder ticks 
    start_t = utime.ticks_ms()
    t = start_t
    output = 100
    actual = 0
    encoder.zero()
    #Run motor loop for 5 seconds
    while(t-start_t < 5000):
        #Read encoder value
        encoder.read()
        actual = encoder.ticks
        #print(f"encoder ticks {encoder.ticks}")
        #Calculate new duty cycle
        output = controller.run(actual)
        #print(f"{output}")
        #Set new duty cyctle
        motor.set_duty_cycle(output)
        #Delay for 10ms
        utime.sleep_ms(10)
        #Read new time
        t = utime.ticks_ms()
    #Stop motor after step response test
    motor.set_duty_cycle(0);
    u2 = pyb.UART(2, baudrate=115200)
    
    #Print controller output and reset
    controller.get_response()
    controller.reset_response()


def main():
    """!
    Set up pins and timer channels for motor and encoder, then run control_test().
    """
    #Set up pins and timer channel.
    in1 = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    in2 = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
    en = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    timer = pyb.Timer(3,freq=20000)
    
    #Create motor driver object
    motorA = MotorDriver(en,in1,in2,timer,False)

    #Set the GPIO pins and timer channel to pass into the encoder class
    ch1 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.IN)
    ch2 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.IN)
    tim8 = pyb.Timer(8,period=0xffff,prescaler = 0)
    
    #Create encoder driver object
    encoder = EncoderReader(ch1,ch2,tim8)
    while(1):
        control_test(motorA, encoder)
        encoder.zero()
        utime.sleep_ms(7000)
        #print(f"encoder ticks loop {encoder.ticks}")
        
        
# The following code only runs if this file is run as the main script;
# it does not run if this file is imported as a module
if __name__ == "__main__":
    # Call the main function
    main()