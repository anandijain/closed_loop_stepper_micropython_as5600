from machine import Pin, PWM, I2C
from time import sleep
import time 
import random



# AS5600 specific
AS5600_ADDRESS = const(0x36)   # AS5600 has a fixed address (so can only use one per I2C bus?)
ANGLE_H	= const(0x0E)          # Angle register (high byte)
ANGLE_L	= const(0x0F)          # Angle register (low byte)

ratio = 1/(2**12)*360

def getnReg(reg, n):
    i2c.writeto(AS5600_ADDRESS, bytearray([reg]))
    t =	i2c.readfrom(AS5600_ADDRESS, n)
    return t    


def get_raw_angle():
    buf = getnReg(ANGLE_H, 2)
    return ((buf[0]<<8) | buf[1])

def to_deg(a):
    return a * ratio

def get_angle():
    return to_deg(get_raw_angle())

# Initialize drivers to known states
def initialize_driver(dir_pin, sleep_pin, reset_pin, ms1_pin, ms2_pin, ms3_pin, enable_pin):
    dir_pin.value(0)       # Set direction to 0
    sleep_pin.value(1)     # Keep awake
    reset_pin.value(1)     # Keep reset inactive
    ms1_pin.value(0)       # Set microstep setting
    ms2_pin.value(0)
    ms3_pin.value(0)
    enable_pin.value(0)    # Enable the driver


i2c = I2C(1,scl=Pin(15), sda=Pin(14))
time.sleep(0.1)  # delay 1ms

# Yaw driver pin definitions
yaw_dir = Pin(26, Pin.OUT)
yaw_step = Pin(22, Pin.OUT)
yaw_sleep = Pin(21, Pin.OUT)
yaw_reset = Pin(20, Pin.OUT)
yaw_ms3 = Pin(19, Pin.OUT)
yaw_ms2 = Pin(18, Pin.OUT)
yaw_ms1 = Pin(17, Pin.OUT)
yaw_enable = Pin(16, Pin.OUT)


initialize_driver(yaw_dir, yaw_sleep, yaw_reset, yaw_ms1, yaw_ms2, yaw_ms3, yaw_enable)

def take_step():
    yaw_step.value(1)
    sleep(0.005)
    yaw_step.value(0)
    sleep(0.005)

# arr = []
# n = 20
# for i in range(20):
#     a1 = get_angle()
#     take_step()
#     a2 = get_angle()
#     arr.append(a1-a2)

# print(arr)
num_turns = 0
# corrected_angle = 0
start_angle = 0
total_angle = 0
prev_total_angle = 0
quad = 0
prev_quad = 0

take_step() # just in case the reading is weird
start_angle = get_angle()

def correct_angle(a): 
    c = a - start_angle
    if c<0:
        c += 360
    return c

def check_quadrant(c): 
    global quad, prev_quad, num_turns, total_angle
    if (c >= 0) & (c <= 90):
        quad = 1
    elif (c > 90) & (c <= 180):
        quad = 2
    elif (c>180) & (c <= 270):
        quad = 3
    elif (c>270) & (c < 360):
        quad = 4
    
    if (quad != prev_quad):
        if (quad == 1) & (prev_quad == 4):
            num_turns += 1
    
        if (quad == 4) & (prev_quad == 1): 
            num_turns -= 1
    
    prev_quad = quad
    total_angle = (num_turns*360) + c
    return total_angle

set_point = random.uniform(-1000, 1000)
while True:
    c = correct_angle(get_angle())
    t = check_quadrant(c)
    err = t - set_point
    sleep(.01)
    if abs(err) < 1: # jitter 
        time.sleep(0.01)
        print("AAAA: t: ", t, "err: ", err, "set: ", set_point, "p: ", p)

        continue
    if err < 0: 
        yaw_dir.value(0)
    if err > 0: 
        yaw_dir.value(1)
    kp = 1
    step_err = err/1.8
    p = int(abs(kp*step_err))
    p = min(int((90/1.8)-1.8), p)
    print("t: ", t, "err: ", err, "set: ", set_point, "p: ", p)
    for i in range(p):
        take_step()
