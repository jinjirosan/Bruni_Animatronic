# Bruni shoulder pluche - animatronic
#
# hardware platform : Pimoroni Pico LiPo
# Animatronic driver : Tower Pro SG92R
# LEDs : Flora Neopixel + kitelight bright EL-Wire
#
# (2023) JinjiroSan
#
# bruni_code.py : v4-0.2 (Alpha release!)


import board
import pwmio
import time
import random
import digitalio
import neopixel
import _thread

def setup_digital_io(pin):
    io = digitalio.DigitalInOut(pin)
    io.direction = digitalio.Direction.INPUT
    io.pull = digitalio.Pull.UP
    return io

def wag_tail(pwm):
    neutral_angle = 90
    angle_change = 53.13
    for angle in [neutral_angle - angle_change, neutral_angle + angle_change, neutral_angle] + [random.uniform(neutral_angle - angle_change / 2, neutral_angle + angle_change / 2) for _ in range(5)]:
        pwm.duty_cycle = int(angle / 180 * 65535 / 20)
        time.sleep(0.5 if angle in [neutral_angle - angle_change, neutral_angle + angle_change, neutral_angle] else 0.2)

pwm = pwmio.PWMOut(board.GP18, frequency=50)
button_wag = setup_digital_io(board.GP16)
led = digitalio.DigitalInOut(board.GP21)
led.direction = digitalio.Direction.OUTPUT
button_led = setup_digital_io(board.GP20)

# Set up the Flora NeoPixel v2
num_pixels = 1
neo_pixel_pin = board.GP19
pixels = neopixel.NeoPixel(neo_pixel_pin, num_pixels, auto_write=False)

# Set up the button to activate the Flora NeoPixel v2
button_neopixel = setup_digital_io(board.GP17)

# Function to animate the NeoPixel with a blue-purple flame effect
def animate_neopixel():
    start_time = time.monotonic()
    while time.monotonic() - start_time < 14:
        color = (random.randint(0, 30), 0, random.randint(100, 255))
        pixels.fill(color)
        pixels.show()
        time.sleep(random.uniform(0.05, 0.15))

# Function to handle NeoPixel animation in a separate thread
def neopixel_thread():
    while True:
        if not button_neopixel.value:
            _thread.start_new_thread(animate_neopixel, ())
            time.sleep(0.2)

# Start the NeoPixel animation thread
_thread.start_new_thread(neopixel_thread, ())

while True:
    if not button_wag.value:
        wag_tail(pwm)
        time.sleep(0.5)
    if not button_led.value:
        led.value = not led.value
        while not button_led.value:
            time.sleep(0.1)
        time.sleep(0.2)
