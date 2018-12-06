# Project : SANGUIS
# This code extracts the dyed patch from the image and then finds the mean of V in the HSV range
import RPi.GPIO as GPIO
import time
import sanguis_main

def main():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_UP)

    while True:
        input_state = GPIO.input(18)
        if input_state == False:
            print ("Button Pressed")
            sanguis_main.start_process()
            time.sleep(0.2)
    
if __name__=="__main__":
    main()