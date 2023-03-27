# Bruni shoulder pluche - animatronic
#
# hardware platform  : Pimoroni Pico LiPo
# Animatronic driver : Tower Pro SG92R
# LEDs               : Flora Neopixel + kitelight bright EL-Wire
# Codebase           : MicroPython v1.19.1
#
# (2023) JinjiroSan
#
# bruni_code.py : v4-0.5 (Beta) - refactor C1.2.8

import machine
import utime
import random
import neopixel

# Version A1 variables and setup
MID = 1500000
MIN = 1000000
MAX = 2000000

neutral_angle = 90
angle_change = 70.0

wag_count = 4
wait_range = (10, 50)

# Version B1 variables and setup
LED_PIN = 19
NUM_PIXELS = 1
COLORS = [(0, 0, 0), (0x40, 0x00, 0xff), (0x80, 0x00, 0xff), (0xc0, 0x00, 0xff), (0xff, 0x00, 0xff)]
MIN_BRIGHTNESS = 50
MAX_BRIGHTNESS = 255

pwm = machine.PWM(machine.Pin(15))
pwm.freq(50)
pwm.duty_ns(MID)

led = neopixel.NeoPixel(machine.Pin(LED_PIN), NUM_PIXELS)

button_wag_pin = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
button_led_pin = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP)

led_on = False
flame_effect_running = False

tail_wagging = False  # global variable to track tail wagging status

wag_event = False
flame_event = False

debounce_time = 200
last_press_time = 0

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
    global flame_event
    current_time = utime.ticks_ms()
    if utime.ticks_diff(current_time, button_state.last_press_time) > debounce_time:
        print("Flame effect button pressed")
        flame_event = True
        button_state.last_press_time = current_time

led_on = False
flame_thread = None

def button_wag_handler(pin):
    global wag_event
    wag_event = True

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