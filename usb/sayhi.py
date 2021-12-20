import os
import sys
import time
import pyttsx3

from aiy.board import Board, Led

with Board() as board:
	board.led.state = Led.ON
	# board.button.wait_for_press()
	os.system("amixer -D pulse sset Master 70%")
	time.sleep(5)
	board.led.state = Led.OFF
	# os.system('espeak -v "english-us" "Nothing is worth insisting on, Sawaddee krub"')
	engine = pyttsx3.init() # object creation
	engine.setProperty('voice','english-us') 
	engine.setProperty('rate', 130)
	engine.setProperty('volume',0.1)
	engine.say('Nothing is worth insisting on, sawaddee krub')
	engine.runAndWait()
	engine.stop()

# How to
# $ crontab -e
# select nano editor (if not)
# type
# @reboot sleep 60 && python3 sayhi.py
#$ crontab -l Check if crontab is properly configured
