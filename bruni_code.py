# Bruni shoulder pluche - animatronic
#
# hardware platform  : Pimoroni Pico LiPo
# Animatronic driver : Tower Pro SG92R
# LEDs               : Flora Neopixel + kitelight bright EL-Wire
# Codebase           : MicroPython v1.19.1
#
# (2023) JinjiroSan
#
# bruni_code.py : v4-1.0 (pre-release) - refactor C2.0.2

import machine
import utime
import random
import neopixel
import _thread 

# Variables
MID = 1500000       # pulse duration for the servo's middle position
MIN = 1000000       # pulse duration for the servo's minimum position
MAX = 2000000       # pulse duration for the servo's maximum position

neutral_angle = 90      # the angle for the servo's neutral position
angle_change = 70.0     # the angle difference for each wag direction

wag_count = 4       # the number of tail wags to perform
wait_range = (10, 50)       # the range of time to wait between tail wags

LED_PIN = 19        # the pin used for the Neopixel LED
NUM_PIXELS = 1      # the number of pixels in the LED strip
COLORS = [(0, 0, 0), (0x40, 0x00, 0xff), (0x80, 0x00, 0xff), (0xc0, 0x00, 0xff), (0xff, 0x00, 0xff)]
MIN_BRIGHTNESS = 50     # the minimum brightness level for the LED
MAX_BRIGHTNESS = 255        # the minimum brightness level for the LED

pwm = machine.PWM(machine.Pin(15))      # create a Pulse Width Modulation object for the servo control pin
pwm.freq(50)        # set the PWM frequency to 50Hz
pwm.duty_ns(MID)        # set the initial duty cycle to the middle position

led = neopixel.NeoPixel(machine.Pin(LED_PIN), NUM_PIXELS)       # create a NeoPixel object for the LED strip

button_wag_pin = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)       # create a Pin object for the wag button
button_led_pin = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP)       # create a Pin object for the LED button

led_on = False      # a flag to indicate if the LED is currently on or off
flame_effect_running = False        # a flag to indicate if the flame effect is currently running

tail_wagging = False  # global variable to track tail wagging status

wag_event = False       # a flag to indicate if the wag button has been pressed
flame_event = False     # a flag to indicate if the LED button has been pressed

debounce_time = 200     # the debounce time in milliseconds for button presses
last_press_time = 0     # the timestamp of the last button press

# Reset the neopixel LED to off at the start of the script
led[0] = (0, 0, 0)
led.write()

class ButtonState:
    def __init__(self):
        self.last_press_time = 0

button_state = ButtonState()

def tail_wag():
    print("Starting tail wagging")
    for angle in [neutral_angle - angle_change, neutral_angle + angle_change, neutral_angle]:
        pwm.duty_ns(int(angle / 180 * (MAX - MIN) / 2 + MID))
        utime.sleep(0.5 if angle in [neutral_angle - angle_change, neutral_angle + angle_change, neutral_angle] else 0.2)

def tail_wag_random():
    global tail_wagging
    tail_wagging = True
    count = 0
    while count < wag_count:
        count += 1
        print("Tail wagging {}/{}".format(count, wag_count))
        tail_wag()
        if count == wag_count:
            break
        else:
            wait_duration = random.randint(*wait_range) 
            print("Waiting for {} seconds until next tail wag...".format(wait_duration))
            utime.sleep(wait_duration)

    pwm.duty_ns(MID)
    print("Tail in neutral position, waiting for next button press...")
    tail_wagging = False  # set tail_wagging flag back to False



def button_wag(pressed_button_pin):
    last_press_time = 0
    wag_count = 0

    while True:
        if not pressed_button_pin.value():
            current_time = utime.time()
            if current_time - last_press_time < 60 and wag_count < 1:
                tail_wag()
                wag_count += 1
                print("Tail wagging 1/{}".format(wag_count))
                tail_wag_random()
                last_press_time = current_time
                wag_count = 0

            elif current_time - last_press_time >= 60:
                wag_count = 0
                last_press_time = current_time

def flame_effect():
    global led_on
    if led_on:
        color = random.choice(COLORS)
        brightness = random.randint(MIN_BRIGHTNESS, MAX_BRIGHTNESS)
        led[0] = tuple(map(lambda x: int(x * brightness / 255), color))
        led.write()
        return random.uniform(0.05, 0.2)
    else:
        led[0] = (0, 0, 0)
        led.write()
        return 0.1


def button_pressed(pin):
    global led_on  # Add led_on to the global variables
    current_time = utime.ticks_ms()
    if utime.ticks_diff(current_time, button_state.last_press_time) > debounce_time:
        print("Flame effect button pressed")
        button_state.last_press_time = current_time
        if led_on:
            led_on = False
        else:
            led_on = True
        flame_effect()  # Add this line to call the flame_effect function


led_on = False
flame_thread = None

def button_wag_handler(pin):
    global wag_event
    wag_event = True
    if not tail_wagging:
        _thread.start_new_thread(tail_wag_random, ())  # Start the tail_wag_random in a new thread


button_led_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_pressed)

button_wag_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_wag_handler)

while True:
    if wag_event:
        wag_event = False
        if not tail_wagging:
            tail_wagging = True
            tail_wag_random()
            tail_wagging = False

    if flame_event:
        flame_event = False
        if led_on:
            led_on = False
        else:
            led_on = True

    wait_time = flame_effect()
    utime.sleep(wait_time)
    utime.sleep(0.1)
