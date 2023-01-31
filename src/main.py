

import pyb
from ClosedLoopContoller import PController
from EncoderReader import EncoderReader
from MotorDriver import MotorDriver

def rotation_test(motor: MotorDriver, encoder: EncoderReader):
    controller = PController(0.05, 5000)
    while(1):
        actual = encoder.read()
        speeeed = controller.run(actual)
        motor.set_duty_cycle(speeeed)
        utime.sleep_ms(10)

def main():
    in1 = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    in2 = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
    en = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    timer = pyb.Timer(3,freq=20000)
    
    #Create motor driver object
    motorA = MotorDriver(en,in1,in2,timer)

    #Set the GPIO pins and timer channel to pass into the encoder class
    ch1 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.IN)
    ch2 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.IN)
    tim8 = pyb.Timer(8,period=0xffff,prescaler = 0)
    
    #Create encoder driver object
    encoder = EncoderReader(ch1,ch2,tim8)

    rotation_test(motorA, encoder)

if __name__ == "__main__":
    main()