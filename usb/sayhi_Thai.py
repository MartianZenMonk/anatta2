import os
import sys
import time

from aiy.board import Board, Led

with Board() as board:
	board.led.state = Led.ON
	# board.button.wait_for_press()
	os.system("amixer -D pulse sset Master 70%")
	time.sleep(5)
	board.led.state = Led.OFF
	os.system('mpg123 -q -f 1000 ../thaivoices/hello.mp3')

'''	
How to
$ crontab -e
select nano editor (if not)
type
@reboot sleep 60 && python3 sayhi.py

Check if crontab is properly configured
$ crontab -l 
