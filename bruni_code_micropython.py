# Bruni shoulder pluche - animatronic
#
# hardware platform : Pimoroni Pico LiPo
# Animatronic driver : Tower Pro SG92R
# LEDs : Flora Neopixel + kitelight bright EL-Wire
#
# (2023) JinjiroSan
#
# bruni_code.py : v4-0.3 (Alpha release!) - MicroPython refactor 0.1

import machine
import time
import random
import neopixel
import _thread  # Import the _thread module for multi-threading

def setup_digital_io(pin):
    io = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
    return io

def wag_tail(pwm):
    neutral_angle = 90
    angle_change = 53.13
    for angle in [neutral_angle - angle_change, neutral_angle + angle_change, neutral_angle] + [random.uniform(neutral_angle - angle_change / 2, neutral_angle + angle_change / 2) for _ in range(5)]:
        pwm.duty(int(angle / 180 * 1023))
        time.sleep_ms(500 if angle in [neutral_angle - angle_change, neutral_angle + angle_change, neutral_angle] else 200)

pwm = machine.PWM(machine.Pin(15))
button_wag = setup_digital_io(16)
led = machine.Pin(21, machine.Pin.OUT)
button_led = setup_digital_io(20)

# Set up the Flora NeoPixel v2
num_pixels = 1
neo_pixel_pin = 19
pixels = neopixel.NeoPixel(machine.Pin(neo_pixel_pin), num_pixels)

# Set up the button to activate the Flora NeoPixel v2
button_neopixel = setup_digital_io(17)

# Function to animate the NeoPixel with a blue-purple flame effect
def animate_neopixel():
    start_time = time.ticks_ms()
    while time.ticks_ms() - start_time < 14000:
        color = (random.randint(0, 30), 0, random.randint(100, 255))
        pixels[0] = color
        pixels.write()
        time.sleep_ms(random.randint(50, 150))

# Function to handle NeoPixel animation in a separate thread
def neopixel_thread():
    while True:
        if not button_neopixel.value():
            _thread.start_new_thread(animate_neopixel, ())
            time.sleep_ms(200)

# Start the NeoPixel animation thread
_thread.start_new_thread(neopixel_thread, ())

while True:
    if not button_wag.value():
        wag_tail(pwm)
        time.sleep_ms(500)
    if not button_led.value():
        led.value(not led.value())
        while not button_led.value():
            time.sleep_ms(100)
        time.sleep_ms(200)
