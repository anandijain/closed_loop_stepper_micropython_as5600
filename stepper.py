from machine import Pin, PWM, I2C
from time import sleep
import time 

# Yaw driver pin definitions
yaw_dir = Pin(26, Pin.OUT)
yaw_step = Pin(22, Pin.OUT)
yaw_sleep = Pin(21, Pin.OUT)
yaw_reset = Pin(20, Pin.OUT)
yaw_ms3 = Pin(19, Pin.OUT)
yaw_ms2 = Pin(18, Pin.OUT)
yaw_ms1 = Pin(17, Pin.OUT)
yaw_enable = Pin(16, Pin.OUT)

# Initialize drivers to known states
def initialize_driver(dir_pin, sleep_pin, reset_pin, ms1_pin, ms2_pin, ms3_pin, enable_pin):
    dir_pin.value(0)       # Set direction to 0
    sleep_pin.value(1)     # Keep awake
    reset_pin.value(1)     # Keep reset inactive
    ms1_pin.value(0)       # Set microstep setting
    ms2_pin.value(0)
    ms3_pin.value(0)
    enable_pin.value(0)    # Enable the driver

initialize_driver(yaw_dir, yaw_sleep, yaw_reset, yaw_ms1, yaw_ms2, yaw_ms3, yaw_enable)

# Test the stepper motors back and forth
def test_stepper(step_pin, dir_pin, steps, delay):
    # Move forward
    dir_pin.value(1)  # Set direction to forward
    for _ in range(steps):
        step_pin.value(1)
        time.sleep(delay)
        step_pin.value(0)
        time.sleep(delay)
    
    time.sleep(0.5)  # Small pause before changing direction
    
    # Move backward
    dir_pin.value(0)  # Set direction to backward
    for _ in range(steps):
        step_pin.value(1)
        time.sleep(delay)
        step_pin.value(0)
        time.sleep(delay)

# Test sequence
try:
    while True:
        print("Testing yaw motor back and forth")
        test_stepper(yaw_step, yaw_dir, 800, 0.005)  # 100 steps for yaw motor
        time.sleep(1)                              # Pause before the next motor

except KeyboardInterrupt:
    print("Test interrupted, disabling motors")
        # Stop the motor when the loop ends

# Disable motors when the test is stopped
yaw_enable.value(1)
