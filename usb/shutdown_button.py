import os
import sys
import time
import pyttsx3

from aiy.board import Board, Led

def main():
        button_press = 0
        ts1 = time.time()
        print('LED is ON while button is pressed (Ctrl-C for exit).')
        with Board() as board:
                while True:
                        board.button.wait_for_press()
                        board.led.state = Led.ON
                        button_press += 1
                        board.button.wait_for_release()
                        # board.led.state = Led.OFF
                        ts2 = time.time()
                        if ts2-ts1 > 10 :
                                button_press = 0
                                ts1 = time.time()
                        if button_press > 5 :
                                os.system("sudo pkill -f anatta_")
                                os.system("sudo killall mpg123")
                                board.led.state = Led.OFF
                                engine = pyttsx3.init() # object creation
                                engine.setProperty('voice','english-us') 
                                engine.setProperty('rate', 150)
                                engine.setProperty('volume',0.2)
                                engine.say("The system is shutting down, please wait until the green light in the box turn off, have a nice day")
                                engine.runAndWait()
                                engine.stop()
                                os.system("sudo shutdown now")
if __name__ == '__main__':
        main()
        
# How stop
# $ crontab -e
# select nano editor (if not)
# type
# @reboot python3 shutdown_button.py
#$ crontab -l Check if crontab is properly configured
