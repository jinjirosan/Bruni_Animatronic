
#    ___                  _ 
#   / __\_ __ _   _ _ __ (_)
#  /__\// '__| | | | '_ \| |
# / \/  \ |  | |_| | | | | |
# \_____/_|   \__,_|_| |_|_|
#
# Bruni shoulder pluche - animatronic
#
# hardware platform  : Pimoroni Pico LiPo
# Animatronic driver : Tower Pro SG92R
# LEDs               : Flora Neopixel V2
# Power              : Galleon 3.7v - 400 mAh LiPo (hardcase)
# Codebase           : MicroPython v1.19.1
#
# (2023) JinjiroSan
#
# bruni_code.py : v4-1.1 (pre-release) - refactor C2.0.7

import machine
import utime
import random
import neopixel
import _thread 

# Variables
MID = 1500000       # pulse duration for the servo's middle position
MIN = 1000000       # pulse duration for the servo's minimum position
MAX = 2000000       # pulse duration for the servo's maximum position

neutral_angle = 2      # the angle for the servo's neutral position
angle_change = 95.0     # the angle difference for each wag direction

wag_count = 5       # the number of tail wags to perform
wait_range = (4, 20)       # the range of time to wait between tail wags

LED_PIN = 19        # the pin used for the Neopixel LED
NUM_PIXELS = 1      # the number of pixels in the LED strip
COLORS = [(0, 0, 0), (0x40, 0x00, 0xff), (0x80, 0x00, 0xff), (0xc0, 0x00, 0xff), (0xff, 0x00, 0xff)] # black, blue, purple, pink, magenta
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

debounce_time = 400     # the debounce time in milliseconds for button presses
last_press_time = 0     # the timestamp of the last button press

# Reset the neopixel LED to off at the start of the script
led[0] = (0, 0, 0)
led.write()

class ButtonState:   # class to store the state of a button
    def __init__(self):   # The __init__ method is the constructor for the ButtonState class
        self.last_press_time = 0   # Initialize the last_press_time attribute to store the timestamp of the last button press event

button_state = ButtonState()   # Create a new instance of ButtonState and assign it to the variable button_state

def tail_wag():
    # First left wag
    angle1 = neutral_angle - angle_change  # Calculate the angle for the first left wag
    pwm.duty_ns(int(angle1 / 180 * (MAX - MIN) / 2 + MID))  # Set the servo position to the first left wag angle
    print(f"First left wag angle: {angle1}")  # Display the calculated angle for the first left wag
    utime.sleep(0.5)  # Wait for 0.5 seconds

    # First right wag
    angle2 = neutral_angle + angle_change  # Calculate the angle for the first right wag
    pwm.duty_ns(int(angle2 / 180 * (MAX - MIN) / 2 + MID))  # Set the servo position to the first right wag angle
    print(f"First right wag angle: {angle2}")  # Display the calculated angle for the first right wag
    utime.sleep(0.5)  # Wait for 0.5 seconds

    # Second left wag with a random angle in the opposite direction
    random_angle_change2 = random.uniform(angle_change * 0.5, angle_change * 1.5)  # Calculate a random angle change for the second wag
    angle3 = neutral_angle + random_angle_change2  # Calculate the angle for the second left wag in the opposite direction
    pwm.duty_ns(int(angle3 / 180 * (MAX - MIN) / 2 + MID))  # Set the servo position to the second left wag angle
    print(f"Second left wag angle: {angle3}")  # Display the calculated angle for the second left wag
    utime.sleep(0.5)  # Wait for 0.5 seconds

    # Second right wag with a random angle in the opposite direction, maintaining the same angle difference
    angle4 = neutral_angle - random_angle_change2  # Calculate the angle for the second right wag in the opposite direction, maintaining the same angle difference
    pwm.duty_ns(int(angle4 / 180 * (MAX - MIN) / 2 + MID))  # Set the servo position to the second right wag angle
    print(f"Second right wag angle: {angle4}")  # Display the calculated angle for the second right wag
    utime.sleep(0.5)  # Wait for 0.5 seconds

    # Back to center
    pwm.duty_ns(MID)  # Set the servo position to the center
    print("Back to center")  # Display that the servo is back to the center position
    utime.sleep(0.2)  # Wait for 0.2 seconds

def tail_wag_random():
    global tail_wagging
    tail_wagging = True    # Set the tail_wagging flag to True to indicate that the tail is currently wagging
    count = 0              # Initialize the count of tail wags to 0
    while count < wag_count:   # Repeat the following block of code until wag_count tail wags have been performed
        count += 1              # Increment the count of tail wags
        print("Tail wagging {}/{}".format(count, wag_count))    # Print a message to indicate which tail wag is currently being performed
        tail_wag()           # Call the tail_wag() function to perform a single tail wag
        if count == wag_count:   # If all tail wags have been performed, break out of the while loop
            break
        else:
            wait_duration = random.randint(*wait_range)     # Generate a random wait duration between the specified range of values
            print("Waiting for {} seconds until next tail wag...".format(wait_duration))    # Print a message to indicate how long the wait will be
            utime.sleep(wait_duration)    # Wait for the specified duration before performing the next tail wag

    pwm.duty_ns(MID)    # Set the servo to the neutral position
    print("Tail in neutral position, waiting for next button press...")   # Print a message to indicate that the tail is now in the neutral position and waiting for the next button press
    tail_wagging = False  # Set the tail_wagging flag back to False to indicate that the tail is no longer wagging

def button_wag(pressed_button_pin):
    last_press_time = 0     # Initialize the timestamp of the last button press to 0
    wag_count = 0           # Initialize the count of tail wags to 0

    while True:             # Repeat the following block of code indefinitely
        if not pressed_button_pin.value():  # If the button is pressed (i.e., its value is False)
            current_time = utime.time()     # Get the current timestamp
            if current_time - last_press_time < 60 and wag_count < 1:  # If less than 60 seconds have elapsed since the last button press and fewer than 1 tail wags have been performed
                tail_wag()                    # Call the tail_wag() function to perform a single tail wag
                wag_count += 1                # Increment the count of tail wags performed
                print("Tail wagging 1/{}".format(wag_count))  # Print a message to indicate which tail wag is currently being performed
                tail_wag_random()             # Call the tail_wag_random() function to perform the remaining tail wags
                last_press_time = current_time    # Update the timestamp of the last button press to the current time
                wag_count = 0                 # Reset the count of tail wags to 0

            elif current_time - last_press_time >= 60:    # If 60 seconds or more have elapsed since the last button press
                wag_count = 0                  # Reset the count of tail wags to 0
                last_press_time = current_time  # Update the timestamp of the last button press to the current time

def flame_effect():
    global led_on           # Access the global variable led_on
    if led_on:              # If the LED is on
        color = random.choice(COLORS)                # Choose a random color from the list of available colors
        brightness = random.randint(MIN_BRIGHTNESS, MAX_BRIGHTNESS)   # Choose a random brightness level within the specified range
        led[0] = tuple(map(lambda x: int(x * brightness / 255), color))   # Set the brightness level for the chosen color and write it to the LED strip
        led.write()
        return random.uniform(0.05, 0.2)    # Return a random wait time between 0.05 and 0.2 seconds
    else:                   # If the LED is off
        led[0] = (0, 0, 0)  # Set the LED strip to be completely off
        led.write()
        return 0.1          # Return a wait time of 0.1 seconds

def button_pressed(pin):
    global led_on          # Access the global variable led_on
    current_time = utime.ticks_ms()    # Get the current timestamp in milliseconds
    if utime.ticks_diff(current_time, button_state.last_press_time) > debounce_time:   # If the time difference between the current and last button presses is greater than the debounce time
        print("Flame effect button pressed")     # Print a message to indicate that the button has been pressed
        button_state.last_press_time = current_time   # Update the timestamp of the last button press to the current time
        if led_on:              # If the LED is on
            led_on = False      # Turn it off
        else:                   # If the LED is off
            led_on = True       # Turn it on
        flame_effect()          # Call the flame_effect() function to update the LED strip accordingly

def button_wag_handler(pin):
    global wag_event        # Access the global variable wag_event
    wag_event = True        # Set the wag_event flag to True to indicate that the button has been pressed
    if not tail_wagging:    # If the tail is not already wagging
        _thread.start_new_thread(tail_wag_random, ())  # Start the tail_wag_random function in a new thread to wag the tail

button_led_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_pressed)   # Register the button_pressed function to handle the falling edge interrupt on the button LED pin
button_wag_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=button_wag_handler)    # Register the button_wag_handler function to handle the falling edge interrupt on the button wag pin

while True:
    if wag_event:       # If the wag button has been pressed
        wag_event = False   # Reset the wag_event flag
        if not tail_wagging:    # If the tail is not already wagging
            tail_wagging = True     # Set the tail_wagging flag to True to indicate that the tail is wagging
            tail_wag_random()       # Call the tail_wag_random function to wag the tail randomly
            tail_wagging = False    # Set the tail_wagging flag back to False to indicate that the tail is not wagging anymore

    if flame_event:     # If the flame button has been pressed
        flame_event = False     # Reset the flame_event flag
        if led_on:              # If the LED is currently on
            led_on = False      # Turn it off
        else:                   # If the LED is currently off
            led_on = True       # Turn it on

    wait_time = flame_effect()  # Call the flame_effect function to update the LED strip and get the wait time
    utime.sleep(wait_time)      # Wait for the specified amount of time
    utime.sleep(0.1)            # Add a small delay between iterations to avoid busy waiting

