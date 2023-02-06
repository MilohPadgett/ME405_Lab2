
import utime
import pyb
from ClosedLoopContoller import PController
from EncoderReader import EncoderReader
from MotorDriver import MotorDriver

def rotation_test(motor: MotorDriver, encoder: EncoderReader):
    controller = PController(0.03, 5000.0)
    while(1):
        encoder.read()
        actual = encoder.ticks
        speeeed = controller.run(actual)
        motor.set_duty_cycle(speeeed)
        #print(f"Actual: {actual}")
        utime.sleep_ms(10)

def get_kp_input():
    Kp = input("Please input a value Kp (float): ")
    try:
        return float(Kp)
    except:
        print("ERROR: Bad input")
        return get_kp_input()

def control_test(motor: MotorDriver, encoder: EncoderReader):
    Kp = get_kp_input()
    controller = PController(Kp,1050.0)
    start_t = utime.ticks_ms()
    t= start_t
    output = 100
    actual = 0
    encoder.zero()
    while(t-start_t < 15000 and abs(output) > 1):
        encoder.read()
        actual = encoder.ticks
        print(f"encoder ticks {encoder.ticks}")
        output = controller.run(actual)
        print(f"{output}")
        motor.set_duty_cycle(output)
        utime.sleep_ms(10)
        t = utime.ticks_ms()
    motor.set_duty_cycle(0);
    u2 = pyb.UART(2, baudrate=115200)
    
    controller.get_response()
    controller.reset_response()


def main():
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
        print(f"encoder ticks loop {encoder.ticks}")
        
        

if __name__ == "__main__":
    main()