from machine import Pin, I2C
from time import sleep
import time 

# AS5600 specific
AS5600_ADDRESS = const(0x36)   # AS5600 has a fixed address (so can only use one per I2C bus?)
ANGLE_H	= const(0x0E)          # Angle register (high byte)
ANGLE_L	= const(0x0F)          # Angle register (low byte)

def getnReg(reg, n):
    i2c.writeto(AS5600_ADDRESS, bytearray([reg]))
    t =	i2c.readfrom(AS5600_ADDRESS, n)
    return t    


def get_angle():
    buf = getnReg(ANGLE_H, 2)
    return ((buf[0]<<8) | buf[1])/ (2**12)*360

i2c = I2C(1,scl=Pin(15), sda=Pin(14))
time.sleep(0.1)  # delay 1ms
last = get_angle()
cur = get_angle()
jitter_tol = .15
while True:
    cur = get_angle()
    if abs(cur - last) > jitter_tol:
        print(cur)
        last = cur
