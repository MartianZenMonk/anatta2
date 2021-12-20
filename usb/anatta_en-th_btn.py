import os
import sys
import time
import subprocess
import pyttsx3

from aiy.board import Board, Led

engine = pyttsx3.init()  # object creation
engine.setProperty('voice', 'english-us')
engine.setProperty('rate', 130)
engine.setProperty('volume', 0.1)

def speak(text):
        print(text)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
        return None


# voices = ["en-gb","en-us","en-gb-scotland","en-gb-x-gbclan","en-gb-x-gbcwmd","en-029"]

# def speakng(t,v='',*args):
#         if v == '':
#                 v = "en-us"
#         text = 'speak-ng -a 10 -s 130 -v ' + v + ' "' + t + '"'
#         print(text)
#         os.system(text)
#         return None


def main():
	with Board() as board:
		while True:
			board.led.state = Led.OFF
			text = "Hello Press button within 3 seconds For English Language"
			speak(text)
			t1 = time.time()
			board.led.state = Led.ON
			board.button.wait_for_press()
			t2 = time.time()
			if t2-t1 < 4:
				board.led.state = Led.OFF
				subprocess.run("python3 anatta_button.py",shell=True, check=True)

			board.led.state = Led.OFF
			text = "Hello Press button within 3 seconds For Thai Language"
			speak(text)
			t1 = time.time()
			board.led.state = Led.ON
			board.button.wait_for_press()
			t2 = time.time()
			if t2-t1 < 4:
				board.led.state = Led.OFF
				subprocess.run("python3 anatta_Thai_button.py",shell=True, check=True)

			board.led.state = Led.OFF
			text = "Well or press button within 3 seconds to play with voices control mode"
			speak(text)
			t1 = time.time()
			board.led.state = Led.ON
			board.button.wait_for_press()
			t2 = time.time()
			if t2-t1 < 4:
				board.led.state = Led.OFF
				text = "speak when see red light or press button and speak when see white light"
				speak(text)
				subprocess.run("python3 testq.py",shell=True, check=True)
				# subprocess.run("python3 test_words.py",shell=True, check=True)

			board.led.state = Led.OFF
			text = "Press button within 3 seconds For Shutdown"
			speak(text)
			t1 = time.time()
			board.led.state = Led.ON
			board.button.wait_for_press()
			t2 = time.time()
			if t2-t1 < 4:
				board.led.state = Led.OFF
				text = "The system is shutting down, please wait until the green light in the box turn off, have a nice day"
				speak(text)
				subprocess.run("sudo shutdown now",shell=True, check=True)
				break


if __name__ == '__main__':
        main()