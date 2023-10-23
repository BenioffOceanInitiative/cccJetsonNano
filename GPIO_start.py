import RPi.GPIO as GPIO
import time
import subprocess as sp

# Pin Definitions
input_pin = 17  # BCM pin 17, BOARD pin 11

def main():
    
    """
    This monitors the GPIO pin that the pump signal is attached to, and when it goes high, it starts the tracking program (start.sh),
    if the pin goes low, it stops the tracking program (stop.sh) after the set cooldown period
    """
    prev_value = None

    # Pin Setup:
    GPIO.setmode(GPIO.BCM)  # BCM pin-numbering scheme from Raspberry Pi
    GPIO.setup(input_pin, GPIO.IN)  # set pin as an input pin
    print("Starting demo now! Press CTRL+C to exit")
    try:
        while True:
            value = GPIO.input(input_pin)
            if value != prev_value:
                if value == GPIO.HIGH:
                    print("Starting tracking program")
                    sp.call("./start.sh")
                else:
                    print("Entering cooldown loop")
                    cooldown()
                prev_value = value
            time.sleep(1)
    finally:
        GPIO.cleanup()
def cooldown():
    """
    This is the cooldown period after the pump has been turned off, it waits for the set amount of time,then checks the pin state again,
      before turning off the tracking program. this is to prevent the tracking program from turning off if the pump is turned on again quickly
    """
    time.sleep(10)
    value = GPIO.input(input_pin)
    if value == GPIO.LOW:
        print("Stopping tracking program")
        sp.call("./stop.sh")
    else:
        cooldown()
    print("cooldown complete")

if __name__ == '__main__':
    main()