#!/usr/bin/env python3

import argparse
import os
import queue
import sounddevice as sd
import vosk
import sys
import json
import random
import pty
import gc
import time
import csv
import socket
import cv2
import psutil
import subprocess
from subprocess import call
import datetime as dt
from datetime import datetime
from aiy.board import Board, Led
from aiy.leds import (Leds, Pattern, PrivacyLed, RgbLeds, Color)
import threading
# import keyboard
from pynput. keyboard import Key, Controller
from pprint import pprint
from pymediainfo import MediaInfo

def media_info(mf=""):
	media_info = MediaInfo.parse(mf)
	for track in media_info.tracks:
		if track.track_type == "Video":
			print("Duration (raw value):", track.duration)
			return track.duration
		elif track.track_type == "Audio":
			print("Duration (raw value):", track.to_data()['duration'])
			return track.to_data()['duration']

def get_input(message, channel):
    response = input(message)
    channel.put(response)


def input_with_timeout(message, timeout):
    channel = queue.Queue()
    message = message + " [{} sec timeout] ".format(timeout)
    thread = threading.Thread(target=get_input, args=(message, channel))
    # by setting this as a daemon thread, python won't wait for it to complete
    thread.daemon = True
    thread.start()

    try:
        response = channel.get(True, timeout)
        return response
    except queue.Empty:
        pass
    return None

# sd._terminate()
# time.sleep(5)
# sd._initialize()
# sd.default.latency = 'low'

import pyttsx3
engine = pyttsx3.init() # object creation
engine.setProperty('voice','english-us') 
engine.setProperty('rate', 125)
engine.setProperty('volume',0.1)


def speak(text):
		print(text)
		engine.setProperty('volume',0.05)
		engine.say(text)
		engine.runAndWait()
		engine.stop()
		return None


from bs4 import BeautifulSoup
import requests

def listFD(url, ext=''):
    page = requests.get(url).text
    #print(page)
    soup = BeautifulSoup(page, 'html.parser')
    return [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]


freq = '../dataen/bell.mp3'#550 # Hz
freq2 = '../dataen/3bell.mp3'
dotLength  = 1 #60 # milliseconds
dashLength = 3 #dotLength * 3
pauseWords = 7 #dotLength * 7

alphaToMorse = {'a': ".-", 'b': "-...", 'c': "-.-.", 'd': "-..", 'e': ".",
				'f': "..-.", 'g': "--.", 'h': "....", 'i': "..", 'j': ".---", 'k': "-.-",
				'l': ".-..", 'm': "--", 'n': "-.", 'o': "---", 'p': ".--.", 'q': "--.-",
				'r': ".-.", 's': "...", 't': "-", 'u': "..-", 'v': "...-", 'w': ".--",
				'x': "-..-", 'y': "-.--", 'z': "--..",
				'1': ".----", '2': "..---", '3': "...--", '4': "....-", '5': ".....",
				'6': "-....", '7': "--...", '8': "---..", '9': "----.", '0': "-----",
				' ': "/", '.': ".-.-.-", ',': "--..--", '?': "..--..", "'": ".----.",
				'@': ".--.-.", '-': "-....-", '"': ".-..-.", ':': "---...", ';': "---...",
				'=': "-...-", '!': "-.-.--", '/': "-..-.", '(': "-.--.", ')': "-.--.-",
				'??': ".--.-", '??': "..-.."}


sutta = {
	"sutta":[
		{"title":"Cankama Sutta",
			"content":[
				{"voice":"1","text":"These are the five rewards for one who practices walking meditation. Which five?"},
				{"voice":"1","text":"He can endure traveling by foot"},
				{"voice":"1","text":"he can endure exertion"},
				{"voice":"1","text":"he becomes free from disease"},
				{"voice":"1","text":"whatever he has eaten & drunk, chewed & savored, becomes well-digested"},
				{"voice":"1","text":"the concentration he wins while doing walking meditation lasts for a long time"},
				{"voice":"1","text":"These are the five rewards for one who practices walking meditation"}
				]
		 },
		 {"title":"Moggallana Sutta",
			"content":[
				{"voice":"1","text":"the Blessed One said to Ven. Maha Moggallana,"},
				{"voice":"2","text":"Are you nodding, Moggallana? Are you nodding?"},
				{"voice":"3","text":"Yes, lord"},
				{"voice":"2","text":"Well then, Moggallana, whatever perception you have in mind when drowsiness descends on you, don't attend to that perception, don't pursue it. It's possible that by doing this you will shake off your drowsiness."},
				{"voice":"2","text":"But if by doing this you don't shake off your drowsiness, then recall to your awareness the Dhamma as you have heard & memorized it, re-examine it & ponder it over in your mind. It's possible that by doing this you will shake off your drowsiness."},
				{"voice":"2","text":"But if by doing this you don't shake off your drowsiness, then repeat aloud in detail the Dhamma as you have heard & memorized it. It's possible that by doing this you will shake off your drowsiness."},
				{"voice":"2","text":"But if by doing this you don't shake off your drowsiness, then pull both your earlobes and rub your limbs with your hands. It's possible that by doing this you will shake off your drowsiness."},
				{"voice":"2","text":"But if by doing this you don't shake off your drowsiness, then get up from your seat and, after washing your eyes out with water, look around in all directions and upward to the major stars & constellations. It's possible that by doing this you will shake off your drowsiness."},
				{"voice":"2","text":"But if by doing this you don't shake off your drowsiness, then attend to the perception of light, resolve on the perception of daytime, [dwelling] by night as by day, and by day as by night. By means of an awareness thus open & unhampered, develop a brightened mind. It's possible that by doing this you will shake off your drowsiness."},
				{"voice":"2","text":"But if by doing this you don't shake off your drowsiness, then ??? percipient of what lies in front & behind ??? set a distance to meditate walking back & forth, your senses inwardly immersed, your mind not straying outwards. It's possible that by doing this you will shake off your drowsiness."},
				{"voice":"2","text":"But if by doing this you don't shake off your drowsiness, then ??? reclining on your right side ??? take up the lion's posture, one foot placed on top of the other, mindful, alert, with your mind set on getting up. As soon as you wake up, get up quickly, with the thought, 'I won't stay indulging in the pleasure of lying down, the pleasure of reclining, the pleasure of drowsiness.' That is how you should train yourself."},
				{"voice":"2","text":"Furthermore, Moggallana, should you train yourself: 'I will not visit families with my pride lifted high.' That is how you should train yourself. Among families there are many jobs that have to be done, so that people don't pay attention to a visiting monk. If a monk visits them with his trunk lifted high, the thought will occur to him, 'Now who, I wonder, has caused a split between me and this family? The people seem to have no liking for me.' Getting nothing, he becomes abashed. Abashed, he becomes restless. Restless, he becomes unrestrained. Unrestrained, his mind is far from concentration."},
				{"voice":"2","text":"Furthermore, Moggallana, should you train yourself: 'I will speak no confrontational speech.' That is how you should train yourself. When there is confrontational speech, a lot of discussion can be expected. When there is a lot of discussion, there is restlessness. One who is restless becomes unrestrained. Unrestrained, his mind is far from concentration."},
				{"voice":"2","text":"It's not the case, Moggallana, that I praise association of every sort. But it's not the case that I dispraise association of every sort. I don't praise association with householders and renunciates. But as for dwelling places that are free from noise, free from sound, their atmosphere devoid of people, appropriately secluded for resting undisturbed by human beings: I praise association with dwelling places of this sort."},
				{"voice":"1","text":"When this was said, Ven. Moggallana said to the Blessed One"},
				{"voice":"3","text":"Briefly, lord, in what respect is a monk released through the ending of craving, utterly complete, utterly free from bonds, a follower of the utterly holy life, utterly consummate: foremost among human & heavenly beings?"},
				{"voice":"2","text":"There is the case, Moggallana, where a monk has heard, 'All phenomena are unworthy of attachment.' Having heard that all phenomena are unworthy of attachment, he fully knows all things. Fully knowing all things, he fully comprehends all things. Fully comprehending all things, then whatever feeling he experiences ??? pleasure, pain, neither pleasure nor pain ??? he remains focused on inconstancy, focused on dispassion, focused on cessation, focused on relinquishing with regard to that feeling. As he remains focused on inconstancy, focused on dispassion, focused on cessation, focused on relinquishing with regard to that feeling, he is unsustained by anything in the world. Unsustained, he is not agitated. Unagitated, he is unbound right within. He discerns: 'Birth is ended, the holy life fulfilled, the task done. There is nothing further for this world"},
				{"voice":"2","text":"It is in this respect, Moggallana, that a monk, in brief, is released through the ending of craving, utterly complete, utterly free from bonds, a follower of the utterly holy life, utterly consummate: foremost among human & heavenly beings."}
				]
		 }
		 ]
	}


def morsecode(message):
	
	if message == "":
		return

	# remembers characters that do not have standard morse code equivalent
	unabletoconvert = ""
	morse = ""
	for char in message.lower():
		if char in alphaToMorse:
			morse += alphaToMorse[char] + ' '
		else:
			unabletoconvert += char
	if len(unabletoconvert) != 0:
		print("These characters are unable to be converted:\n" + ' '.join(unabletoconvert))
	morse = morse[:-1]
	print(morse)
	morseaudio(morse)
		
def dot(dur):
	os.system("mpg123 -q -f 4000 " + freq)
	
def dash(dur):
	os.system("mpg123 -q -f 4000 " + freq2)

def beep(dur):
	"""
	makes noise for specific duration.
	:param dur: duration of beep in milliseconds
	"""
	#winsound.Beep(freq, dur)
	os.system("mpg123 --loop " + str(dur) + ' -f 2000 ' + freq)

def pause(dur):
	"""
	pauses audio for dur milliseconds
	:param dur: duration of pause in milliseconds
	"""
	time.sleep(dur*5)

def morseaudio(morse):
	"""
	plays audio conversion of morse string using inbuilt windows module.
	:param morse: morse code string.
	"""
	for char in morse:
		if char == ".":
			dot(dotLength) #beep(dotLength)
		elif char == "-":
			dash(dashLength) #beep(dashLength)
		elif char == "/":
			pause(pauseWords)
		else:
			# char is blank space
			pause(dashLength)


def find_name(name):
	for proc in psutil.process_iter():
		try:
			pinfo = proc.as_dict(attrs=['pid', 'name'])
			if pinfo['name'] == name:
				return True
			else:
				continue
		except psutil.NoSuchProcess:
			print("not found")
	return False


try:
	import httplib
except:
	import http.client as httplib

def have_internet():
	conn = httplib.HTTPConnection("www.google.com", timeout=5)
	try:
		conn.request("HEAD", "/")
		conn.close()
		return True
	except:
		conn.close()
		return False


es_voices = ["englisg+f1","english+f2","english+m1","english+m3","english+m2","english_rp+m2"]


def espeak(t,a='',v='',s='',*args):

		if v == '':
			v = es_voices[2]

		if a == '':
			a = '10'

		if s == '':
			s = '125'

		text = 'espeak -s ' + s + ' -a ' + a + ' -v ' + v + ' "' + str(t) + '"'
		print(t)
		os.system(text)
		return None


word  = ["zero","one","two","three","four","five","six","seven","eight","nine","ten"]
word += ["eleven","twelve","thirteen","forteen","fifteen","sixteen","seventeen","eighteen","nineteen"]
number = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]

def word2int(w):
	
	try:
		n = word.index(w)
		return number[n]
	except:
		return None


def int2word(i):
	
	try:
		n = number.index(i)
		return word[n]
	except:
		return None


# flite Voices available: kal awb_time kal16 awb rms slt  
def speakf(v,t,*args):
		os.system('flite -voice ' + v + ' -t "' + str(t) + '"')
		return None

voices = ["kal", "slt", "rms", "awb", "awb_time", "kal16"]


q = queue.Queue()
qlimit = 10
qf = 0

def int_or_str(text):
	"""Helper function for argument parsing."""
	try:
		return int(text)
	except ValueError:
		return text

def callback(indata, frames, time, status):
	"""This is called (from a separate thread) for each audio block."""
	global qlimit
	if status:
		print(status, file=sys.stderr)
	# for pi zero
	if q.qsize() > qlimit:
		pass
		# with q.mutex:
		# 	q.queue.clear()
	else:
		q.put(bytes(indata)) 
	# for others
	# q.put(bytes(indata))


def clear_q():
	time.sleep(1)
	with q.mutex:
		q.queue.clear()

# see leds_example.py

def ledc(c='', f='16hz'):
	global led_color

	Color.ORANGE = (100, 5, 0)
	Color.DRAKGREEN = (0, 1, 0)

	today = dt.datetime.now()
	hrs = int(today.strftime("%H"))
	if hrs < 6:
		led_color = 'd'
	elif hrs < 18:
		led_color = 'dg'
	else:
		led_color = 'off'

	# print('Set blink pattern: period=500ms (2Hz)')
	if f == 'alpha':
		leds.pattern = Pattern.blink(100) # Alpha 10 Hz
	elif f == 'delta':
		leds.pattern = Pattern.blink(500) # Delta 2 Hz
	elif f == 'theta':
		leds.pattern = Pattern.blink(250) # Theta 4 Hz
	else:
		leds.pattern = Pattern.blink(62.5) #  16 Hz

	if c == 'r':
		leds.update(Leds.rgb_on(Color.RED))
	elif c == 'rr':
		leds.update(Leds.rgb_pattern(Color.RED))

	elif c == 'g':
		leds.update(Leds.rgb_on(Color.GREEN))
	elif c == 'dg':
		leds.update(Leds.rgb_on(Color.DRAKGREEN))
	elif c == "gg":
		leds.update(Leds.rgb_pattern(Color.GREEN))

	elif c == 'b':
		leds.update(Leds.rgb_on(Color.BLUE))
	elif c == 'bb':
		leds.update(Leds.rgb_pattern(Color.BLUE))

	elif c == 'y':
		leds.update(Leds.rgb_on(Color.YELLOW))
	elif c == 'yy':
		leds.update(Leds.rgb_pattern(Color.YELLOW))

	elif c == 'p':
		leds.update(Leds.rgb_on(Color.PURPLE))     
	elif c == 'pp':
		leds.update(Leds.rgb_pattern(Color.PURPLE))

	elif c == 'c':
		leds.update(Leds.rgb_on(Color.CYAN))
	elif c == 'cc':
		leds.update(Leds.rgb_pattern(Color.CYAN))

	elif c == 'd':
		# dark or black = rgb(0,0,0)
		leds.update(Leds.rgb_on(Color.BLACK))
	elif c == 'dd':
		leds.update(Leds.rgb_pattern(Color.BLACK))
	elif c == 'o':
		leds.update(Leds.rgb_on(Color.ORANGE))
	elif c == 'oo':
		leds.update(Leds.rgb_pattern(Color.ORANGE))
	elif c == 'off':
		board.led.state = Led.OFF

	else:
		leds.update(Leds.rgb_on(Color.WHITE))

	return None

def with_opencv(filename):

	video = cv2.VideoCapture(filename)

	fps = video.get(cv2.CAP_PROP_FPS)
	frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
	sec = frame_count / fps

	return sec


def killPlayer():
	if find_name('mpg123'):
		os.system("killall mpg123")
	if find_name('vlc'):
		os.system("killall vlc")
	return None

def wait_for_vlc(proc=0,t=5):
	# print(proc)
	ledc('d')
	delay(1)
	vlc = True
	while vlc:
		if find_name('vlc'):
			board.button.wait_for_press(60*t)
		else:
			vlc = False
	proc.kill()
	# print("Done!")

def pkill_proc_name(name=''):
	global proc_name
	if name == '':
		pass
	else:
		proc_name = name

	if len(proc_name) > 0:
		os.system("pkill -f " + proc_name)
		proc_name = ''
		# espeak("kill " + proc_name,'4')
		
	return None


def delay(t,c='off'):
	ledc(c)
	board.button.wait_for_press(60*t)
	return None


def press_for_stop(c='off',proc=0,t=0):
	ledc(c)
	if t == 0 :
		board.button.wait_for_press()
	else:
		board.button.wait_for_press(t)
	proc.kill()
	killPlayer()
	with q.mutex:
		q.queue.clear()
	return None


def get_help():
	text =  '''
			Thai Chanting,
            Play Dhamma, 
            Play Sutra,
            Meditation One,
            Thai Walking, 
            Sitting Practice,
			daily dependent origination,
			buddha thinking,
			nature truth chanting,
			breathing chanting,
			dependent origination chanting,
			8 fold path Thai, 8 fold path English,
			English chanting,
			meditaion time, play radio, 
			mantra 1 2 3 4 5 6 or 10 15 20 30 40 50 minutes,
			play 1 3 6 stage,
			what time, what day, buddha day, zen story,
			red green blue yellow or sound and or alpha light on,
			pure or breathing alpha meditation,
			math meditation,
			walking practice,
			moring practice,
			wise one or alpha,
			goodbye or anat ta stop,
			'''
	speak(text)
	time.sleep(3)
	with q.mutex:
		q.queue.clear()
	return None


def shutdown():
	os.system("mpg123 -f 1000 ../voices/dead.mp3")
	espeak("The system is shutting down, wait until the green light in the box turn off, bye bye",'10')
	board.led.state = Led.OFF
	os.system("sudo shutdown now")
	return None


def get_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		# doesn't even have to be reachable
		s.connect(('10.255.255.255', 1))
		IP = s.getsockname()[0]
	except Exception:
		IP = '127.0.0.1'
	finally:
		s.close()
	return IP

#TEST
def motion_detect(proc,t=0):
	bk = False
	# timeout = time.time() + t*60
	# Assigning our static_back to None
	static_back = None
	# List when any moving object appear
	# motion_list = [ None, None ]
	video = cv2.VideoCapture(0)
	while True:
		# Reading frame(image) from video
		check, frame = video.read()
		# Initializing motion = 0(no motion)
		# motion = 0

		# Converting color image to gray_scale image
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		# Converting gray scale image to GaussianBlur
		# so that change can be find easily
		gray = cv2.GaussianBlur(gray, (21, 21), 0)

		# In first iteration we assign the value
		# of static_back to our first frame
		if static_back is None:
			static_back = gray
			continue

		# Difference between static background
		# and current frame(which is GaussianBlur)
		diff_frame = cv2.absdiff(static_back, gray)

		# If change in between static background and
		# current frame is greater than 30 it will show white color(255)
		thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
		thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)

		# Finding contour of moving object
		_,cnts,_ = cv2.findContours(thresh_frame.copy(),
						cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		for contour in cnts:
			if cv2.contourArea(contour) < 10000:
				continue
			# motion = 1

			(x, y, w, h) = cv2.boundingRect(contour)
			# print(str(w*h))
			# making green rectangle arround the moving object
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
			if w*h > 220000:
				bk = True

		# if t > 0:
		# 	if time.time() > timeout:
		# 		break

		# Appending status of motion
		# motion_list.append(motion)
		if bk:
			break

		#cv2.imshow("Gray Frame", gray)
		#cv2.imshow("Difference Frame", diff_frame)
		#cv2.imshow("Threshold Frame", thresh_frame)
		# cv2.imshow("Color Frame", frame)
		# key = cv2.waitKey(1)
		# if q entered whole process will stop
		# if key == ord('q'):
		#     break

	proc.kill()
	video.release()
	# Destroying all the windows
	# cv2.destroyAllWindows()
		
	return None

from pydub import AudioSegment
from pydub.playback import play

def speakThai(texts,dB=20):
	thsound = AudioSegment.empty()
	stext = ""
	for tx in texts:
		stext = "../voices/thai/" + tx + ".mp3"
		thsound += AudioSegment.from_mp3(stext)
	play(thsound-dB)

def speakThai_mp3(texts,vol='1000'):
	stext = ""
	for tx in texts:
		stext += "../voices/thai/" + tx + ".mp3 "	
	os.system('mpg123 -f ' + vol + ' ' + stext)

def enwords(text):
	stext = ""
	for i in range(len(text)):
		stext += " ../dataen/" + text[i] + ".mp3"
	return stext


def thwords(text):
	stext = ""
	for i in range(len(text)):
		stext += " ../voices/th/" + text[i] + ".mp3"
	return stext

def mythaiwords(text):
	stext = ""
	for i in range(len(text)):
		stext += " voices/mp3/th/" + text[i] + ".mp3"
	return stext

def mythaiwordswav(text):
	stext = ""
	for i in range(len(text)):
		stext += " voices/wav/th/" + text[i] + ".wav"
	return stext


def thaiwords(text):
	stext = ""
	for i in range(len(text)):
		stext += " ../voices/th/" + text[i] + ".mp3"
	return stext

def thaiwordswav(text):
	stext = ""
	for i in range(len(text)):
		stext += " ../voices/th/" + text[i] + ".wav"
	return stext


def zhwords(text):
	stext = ""
	for i in range(len(text)):
		stext += " ../voices/zh/" + text[i] + ".mp3"
	return stext


def jawords(text):
	stext = ""
	for i in range(len(text)):
		stext += " ../voices/ja/" + text[i] + ".mp3"
	return stext

def kowords(text):
	stext = ""
	for i in range(len(text)):
		stext += " ../voices/ko/" + text[i] + ".mp3"
	return stext


def engwords(text):
	stext = ""
	for i in range(len(text)):
		stext += " ../voices/en/" + text[i] + ".mp3"
	return stext

def mp3_words(text,lg='th'):
	stext = ""
	for i in range(len(text)):
		stext += " ../mp3voices/" + lg + "/" + text[i] + ".mp3"
	return stext


def runtime_vocabulary():
	with open('../csv/vocabulary.csv', newline='') as f:
		reader = csv.reader(f)
		data = list(reader)

	new_vocab = " ".join(str(x[0]) for x in data) 
	new_vocab += ' '
	del data
	gc.collect()
	return new_vocab


def save_vocabulary(w):
	wlist = []
	wlist.append(w)
	writer = csv.writer(open("../csv/vocabulary.csv", "a"))
	writer.writerow(wlist)
	# writer.close()


def buddha_day():
	if have_internet():
		today = dt.datetime.now()
		year  = today.strftime("%Y")
		with open('../csv/'+ year + '.csv', newline='') as f:
			reader = csv.reader(f)
			data = list(reader)

		day = datetime.today().strftime('%Y%m%d')
		holyday = []
		thholyday = []
		todayholyday = []
		for i in range(len(data)):
			if i > 0:
				if(int(data[i][1]) > int(day)):
					holyday.append(data[i][1])
					thholyday.append(data[i][0])
				elif (int(data[i][1]) == int(day)):
					todayholyday = list(str(data[i][0]))

		t = thholyday[0].replace("(", " ")
		x = t.split()
		
		bdaytext = ""
		for i in range(len(x)-1):
		  bdaytext += " ../voices/th/" + x[i] + ".mp3"

		

		today = dt.datetime.now()
		z = today.strftime("%B %A %d %H %M")
		speak("Today is " + z)

		t = "??????????????????,?????????,weekday/%w,?????????,59/%d,???????????????,month/%m,????????????,59/%H,??????????????????,59/%M,????????????"
		t = t.replace("%w",today.strftime('%w'))
		t = t.replace("%d",today.strftime('%d'))
		t = t.replace("%m",today.strftime('%m'))
		t = t.replace("%H",today.strftime('%H'))
		t = t.replace("%M",today.strftime('%M'))
		text = t.split(',')

		stext = ""
		for i in range(len(text)):
				stext += " ../voices/th/" + text[i] + ".mp3"
		os.system("mpg123 -q -f 2100 "+stext)

		y = list(str(holyday))
		yy = y[2]+y[3]+y[4]+y[5]
		mm = y[6]+y[7]
		dd = y[8]+y[9]
		x = dt.datetime(int(yy), int(mm), int(dd))

		z = x.strftime("%B %A %d")
		speak("next Buddha holy day is " + z)

		t = "??????????????????,????????????,?????????,?????????,weekday/%w,?????????,59/%d,???????????????,month/%m"
		t = t.replace("%w",x.strftime('%w'))
		t = t.replace("%d",x.strftime('%d'))
		t = t.replace("%m",x.strftime('%m'))
		text = t.split(',')

		stext = ""
		for i in range(len(text)):
				stext += " ../voices/th/" + text[i] + ".mp3" 
		os.system("mpg123 -q -f 2100 "+stext) 
		os.system("mpg123 -q -f 2100 "+bdaytext) 

		del data
		del stext
		del bdaytext
		del t
		del text
		gc.collect()

		if len(todayholyday) >0:
			if '8' in todayholyday:
				speak("One nee one phra Lek, today is Buddha day")
				speakThai_mp3(['?????????','?????????','????????????'])
				clear_q()
				return 8
			else:
				speak("One nee one patimok, today is Big Buddha day")
				speakThai_mp3(['?????????','?????????','????????????'])
				clear_q()
				return 15
		else:
			clear_q()
			return 0
	else:
		speak("sorry no internet connection")
		return 0


def fast_buddho(c='off', t=30, vol='2000'):

	ledc(c)

	if t==0:
		proc = subprocess.Popen(["mpg123","-d","3","-f",vol,"-q","--loop","-1","../voices/buddho.mp3"])
		press_for_stop(c,proc)
	else:
		proc = subprocess.Popen(["mpg123","-d","3","-f",vol,"-q","--loop","-1","../voices/buddho.mp3"])
		delay(t)
		proc.kill()
		clear_q()
   
	return None

def fast_buddho_hiphop(c='off', t=30, vol='2000'):

	ledc(c)

	if t==0:
		proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../sound/buddho-hiphop.mp3"])
		press_for_stop(c,proc)
	else:
		proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../sound/buddho-hiphop.mp3"])
		delay(t)
		proc.kill()
		clear_q()
   
	return None

def buddhodeekwa(c='off', t=30, vol='2000'):

	ledc(c)

	if t==0:
		proc = subprocess.Popen(["mpg123","-d","1","-f",vol,"-q","--loop","-1","../voices/buddhodeekwa-15.mp3"])
		press_for_stop(c,proc)
	else:
		proc = subprocess.Popen(["mpg123","-d","1","-f",vol,"-q","--loop","-1","../voices/buddhodeekwa-15.mp3"])
		delay(t)
		proc.kill()
		clear_q()
   
	return None

def breathing1(c='off', t=30, vol='2000'):

	ledc(c)

	if t==0:
		proc = subprocess.Popen(["mpg123","-d","1","-f",vol,"-q","--loop","-1","../voices/breathing1.mp3"])
		press_for_stop(c,proc)
	else:
		proc = subprocess.Popen(["mpg123","-d","1","-f",vol,"-q","--loop","-1","../voices/breathing1.mp3"])
		delay(t)
		proc.kill()
		clear_q()
   
	return None

def kidnor(c='off', t=30, vol='2000'):

	ledc(c)

	if t==0:
		proc = subprocess.Popen(["mpg123","-d","1","-f",vol,"-q","--loop","-1","../voices/kidnor30min.mp3"])
		press_for_stop(c,proc)
	else:
		proc = subprocess.Popen(["mpg123","-d","1","-f",vol,"-q","--loop","-1","../voices/kidnor30min.mp3"])
		delay(t)
		proc.kill()
		clear_q()
   
	return None


def bell(l='3',vol='500'):
	subprocess.run(["mpg123","-q","-f",vol,"--loop",l,"../dataen/bell.mp3"])
	return None

def bell_5minutes(l='1',vol='500'):
	subprocess.run(["mpg123","-q","-f",vol,"--loop",l,"../sound/bell5min.mp3"])
	return None

def adjust_volume():
	now = int(datetime.today().strftime('%H'))		
	if now > 17 or now < 6:
		call(["amixer","-q","-M","sset","Master","75%"])
	else:
		call(["amixer","-q","-M","sset","Master","95%"])


def relax_thai(vol="600"):

	text  = ["??????","?????????","????????????","????????????","?????????","??????","?????????","?????????","????????????","????????????","???????????????","????????????","?????????","????????????","?????????","??????","?????????","??????"]
	text += ["????????????","?????????","????????????","?????????","????????????","?????????????????????","????????????","?????????","?????????","??????????????????","?????????"]
	# text += ["??????","?????????","??????","???????????????","?????????","??????","?????????","??????","?????????","????????????","?????????","?????????","????????????","????????????????????????","???????????????????????????","???????????????","?????????????????????","????????????","??????","????????????"]
	stext = thwords(text)
	# print(stext)
	os.system("mpg123 -q -f " + vol + " " + stext)
	del stext
	gc.collect()
	return None


def relax_walk(t=5,vol='1000'):
	call(["amixer","-q","-M","sset","Master","40%"])
	text  = ["?????????","??????","?????????","??????","??????????????????","??????????????????","?????????","??????","?????????","??????","?????????","?????????","?????????????????????","?????????","?????????","??????","?????????","?????????","??????","?????????","????????????","?????????"]
	text += ["?????????","??????","?????????","??????","??????????????????","??????????????????","?????????","????????????","??????","??????","?????????","????????????","?????????","??????","??????","??????","??????","?????????","????????????","?????????"]
	text += ["?????????","??????","?????????","??????","??????????????????","??????????????????","?????????","????????????","?????????","?????????","??????","????????????","?????????","????????????","?????????","?????????","??????","?????????"]
	text += ["?????????","??????","?????????","??????","??????????????????","??????????????????","?????????","??????","?????????","?????????","??????","????????????","?????????","?????????","????????????","?????????","??????","?????????","??????","?????????","?????????","?????????"]
	tx   = thaiwords(text)
	tx_list = tx.split(' ')
	# print(tx_list)
	i = 1
	n = len(tx_list) - 1
	timeout = time.time() + 60*t   
	while True:
		if time.time() > timeout and i == n:
			break
		else:
			# os.system("cvlc --play-and-exit --gain 1 " + tx_list[i])
			os.system("aplay " + tx_list[i] + ".wav")
		time.sleep(0.25)
		if i < n:
			i += 1
		else:
			i = 1
	# os.system("cvlc --play-and-exit --gain 1 " + tx_list[i])
	# os.system("mpg123 -q -f "+ vol + " " + tx_list[i])
	os.system("aplay " + tx_list[i] + ".wav")
	time.sleep(1)
	del text
	del tx
	del tx_list
	gc.collect()
	clear_q()
	call(["amixer","-q","-M","sset","Master","90%"])
	return None


def anapanasati_walk(ts=5,vol="40%"):
	call(["amixer","-q","-M","sset","Master",vol])
	t  = '????????? ?????? ????????? ?????? ?????????????????? ?????????????????? ????????? ?????? ????????? ????????? ?????? ???????????? ????????? ????????? ???????????? ????????? ????????? ????????? ?????? ????????? ????????? ????????? '
	t += '????????? ?????? ????????? ?????? ?????????????????? ?????????????????? ????????? ?????? ?????? ????????? ????????? ????????? ?????? ?????? ?????? ????????? ?????? ?????? ?????? ????????? ?????? ????????? '
	t += '????????? ?????? ????????? ?????? ?????????????????? ?????????????????? ????????? ??????????????? ???????????? ????????? ????????? ????????? ????????? ????????? ???????????? ????????? ????????? ????????? ???????????? ???????????? ????????? ????????? ????????? ??????????????? ' 
	t += '????????? ?????? ????????? ?????? ?????????????????? ?????????????????? ????????? ???????????? ???????????? ????????? ?????????????????? ????????? ???????????? ???????????? ???????????? ????????? ???????????? ????????? ???????????? ???????????? ????????? ????????? ??????????????? ????????? ???????????? ???????????? ???????????? ?????????'
	text = t.split(' ')
	tx   = thaiwords(text)
	tx_list = tx.split(' ')
	# print(tx_list)
	i = 1
	n = len(tx_list) - 1
	timeout = time.time() + 60*ts  
	while True:
		if time.time() > timeout and i == n:
			break
		else:
			os.system("aplay " + tx_list[i] + ".wav")
		time.sleep(0.25)
		if i < n:
			i += 1
		else:
			i = 1
	os.system("aplay " + tx_list[i] + ".wav")
	time.sleep(1)
	del t
	del text
	del tx
	del tx_list
	gc.collect()
	clear_q()
	call(["amixer","-q","-M","sset","Master","80%"])
	return None


def musk_walk(ts=5):
	call(["amixer","-q","-M","sset","Master","40%"])
	t  = '????????? ?????? ????????? ?????? ?????????????????? ?????????????????? ???????????? ???????????? ????????? ????????? ?????? ????????? ?????? ???????????? ????????? ?????? ??????????????? ???????????? ????????? ?????? ???????????? ????????? ???????????? ??????????????? ???????????? ????????? ?????? ???????????? ????????? ???????????? ??????????????? ???????????? ????????? ?????? ????????? ?????? ???????????? ????????? ????????? ???????????? ????????? ???????????? ??????????????? '
	t += '????????? ?????? ????????? ?????? ?????????????????? ?????????????????? ???????????? ???????????? ????????? ????????? ?????? ????????? ????????? ?????? ???????????? ?????? ????????? ????????? ????????? ????????? ???????????? ?????? ????????? ????????? ???????????? ???????????? ???????????? ?????? ????????? ????????? ??????????????? ??????????????? '
	t += '????????? ?????? ????????? ?????? ?????????????????? ?????????????????? ????????? ????????? ?????? ????????? ????????? ?????? ?????? ?????? ???????????? ????????? ????????? ????????? ????????? ???????????? ???????????? ????????? ????????? ????????? ????????? ??????????????? ???????????? ????????? ????????? ????????? ???????????? ???????????? ????????? ????????? ????????? ???????????? ???????????? '
	t += '????????? ?????? ????????? ?????? ?????????????????? ?????????????????? ????????? ?????? ????????? ????????? ????????? ????????? ?????? ????????? ????????? ?????? ???????????? ????????? ????????? ????????? ???????????? ????????? ????????? ????????? ????????? ???????????? ????????? ????????? ???????????? ????????? ????????? ????????? ????????? ???????????? ????????? ????????? ????????????????????? ????????? ?????? ????????? '
	t += '????????? ?????? ????????? ?????? ?????????????????? ?????????????????? ????????? ?????????????????? ?????? ????????? ????????? ????????? ?????? ?????? ?????? ?????? ????????? ?????? ?????? ????????? ?????? ???????????? ?????? ?????? ????????? ?????? ???????????? '
	t += '????????? ?????? ????????? ?????? ?????????????????? ?????????????????? ???????????? ??????????????? ????????? ????????? ?????? ?????? ?????? ?????? ????????? ?????? ???????????? ???????????? ???????????? ?????? ???????????? ????????? ????????? ?????? ???????????? ?????? ???????????? ?????? ??????????????? ????????? ?????? ???????????? ?????? ????????? ?????? ????????? '
	t += '????????? ?????? ????????? ?????? ?????????????????? ?????????????????? ???????????? ?????? ????????? ????????? ????????? ?????? ????????? ?????? ????????? ?????? ????????? ?????? ????????? ?????? ?????? ?????? ?????? ?????? ????????? ?????? ????????? ?????? ????????? ?????? ???????????? ?????? ???????????? ??????????????? ????????? ??????????????? ?????? ???????????? ????????? ????????? ????????? ?????? ????????? ????????? ???????????? ?????? ?????? ????????? ???????????? ????????? ?????? ?????? ?????? ?????? ????????? ???????????? ????????? '
	t += '????????? ?????? ????????? ?????? ?????????????????? ?????????????????? ???????????? ???????????? ?????? ???????????? ????????? ????????? ?????? ????????? ?????? ???????????? ????????? ????????? ????????? ?????? ???????????? ??????????????? ???????????? ????????? ???????????????????????? ???????????? ????????? ??????????????? ????????? ????????? ?????? ???????????? ??????????????? ?????? ????????? ???????????? ????????? ???????????????????????? '
	t += '???????????? ????????? ???????????? ????????? ????????? ?????? ???????????? ?????? ???????????? ????????? ???????????? ?????????????????? ???????????? ????????? ???????????? ?????? ????????? ?????? ?????? ????????? ???????????? ???????????? ???????????? ????????? ???????????? ????????? ??????????????? ????????? ????????? ?????? ??????????????? ????????? ?????? ????????? ?????? ????????? ???????????? ????????? ????????? ???????????? ???????????????????????? ???????????????????????? ??????????????? ?????? ????????? ?????? ???????????? ?????? ????????????'

	text = t.split(' ')
	tx   = thaiwords(text)
	tx_list = tx.split(' ')
	# print(tx_list)
	i = 1
	n = len(tx_list) - 1
	timeout = time.time() + 60*ts  
	while True:
		if time.time() > timeout and i == n:
			break
		else:
			os.system("aplay " + tx_list[i] + ".wav")
		time.sleep(0.25)
		if i < n:
			i += 1
		else:
			i = 1
	os.system("aplay " + tx_list[i] + ".wav")
	time.sleep(1)
	del t
	del text
	del tx
	del tx_list
	gc.collect()
	clear_q()
	call(["amixer","-q","-M","sset","Master","80%"])
	return None

def cheerful_mantra_th1(c='off', t=30, vol='2000'):

	ledc(c)

	if t==0:
		proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../sound/c_citta_alpha.mp3"])
		press_for_stop(c,proc)
	else:
		proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../sound/c_citta_alpha.mp3"])
		delay(t)
		proc.kill()
		clear_q()
   
	return None


def pure_alpha(c='yy'):
	ledc(c)
	call(["amixer","-q","-M","sset","Master","50%"])
	speak("pure alpha sound, push button for stop")
	os.system("mpg123 -f 1000 ../voices/right_concentation.mp3")
	proc = subprocess.Popen(["mpg123","-q","--loop","-1","../sound/pureAlpha2.mp3"])
	press_for_stop(c,proc)
	call(["amixer","-q","-M","sset","Master","90%"])
	return None

def alpha_wave(t):
	call(["amixer","-q","-M","sset","Master","50%"])
	proc = subprocess.Popen(["mpg123","-q","--loop","-1","../sound/pureAlpha2.mp3"])
	delay(t)
	proc.kill()
	clear_q()
	call(["amixer","-q","-M","sset","Master","90%"])
	return None

def singing_bowl(t=15):
	m = random.randint(0,1) 
	if m == 0:
		play_mp3('../sound/528Hz.mp3',t*60)
	elif m == 1:
		play_mp3('../sound/432Hz.mp3',t*60)
	return None
	
	
def mars_wind(t):
	proc = subprocess.Popen(["mpg123","-q","-f","2000","--loop","-1","../sound/wind-on-mars.mp3"])
	delay(t)
	proc.kill()
	clear_q()
	return None

#BHAVANA
def remind_breathing(t=30,vol='600',l='th',ts=0):
	bell('1',vol)
	if l == 'zh':
		text = ['???????????????','?????????????????????']
		tx   = zhwords(text)
	elif l == 'ja':
		text = ['????????????_????????????','????????????_????????????']
		tx   = jawords(text)
	elif l == 'en':
		text = ['cheerful_breathing_in','relieved_breathing_out']
		tx   = engwords(text)
	elif l == 'th1':
		text = ["?????????05","??????05","?????????05","??????05","?????????","??????","????????????","?????????05","?????????","??????","?????????","??????05"]
		tx   = thaiwords(text)
	elif l == 'th2':
		text = ["?????????","??????","????????????05","?????????","??????","?????????05","?????????05","??????05"]
		tx   = thaiwords(text)
	elif l == 'th3':
		text = ["?????????","??????","????????????05","?????????","??????","?????????05"]
		tx   = thaiwords(text)
	elif l == 'th4':
		text = ["?????????05","??????05"]
		tx   = thaiwords(text)
	elif l == 'th5':
		text = ['????????????????????????','????????????','??????????????????????????????','??????????????????','??????????????????','??????????????????']
		tx   = thaiwords(text)
	else:
		text = ["?????????","????????????","?????????","?????????","??????","????????????","?????????","????????????","?????????","?????????","??????","?????????","??????","?????????","?????????","?????????","?????????"]
		tx   = thwords(text)

	timeout = time.time() + 60*t   
	while True:
		if time.time() > timeout:
			break
		else:
			os.system("mpg123 -q -f "+ vol + " " + tx)
			time.sleep(ts)
	bell('1',vol)
	clear_q()
	return None
 
 
def remind_breathing2(t=30,vol='500'):
	#bell('3',vol)
	text  = ["?????????","??????","?????????","??????","????????????","?????????","??????","?????????","?????????","?????????","????????????","????????????"]
	tx   = thaiwords(text)
	timeout = time.time() + 60*t   
	while True:
		if time.time() > timeout:
			break
		else:
			os.system("mpg123 -f "+ vol + " " + tx)
	bell('1',vol)
	clear_q()
	return None


def remind_b4walking(vol='500',lg=''):
	bell('1',vol)
	if lg == 'th':
		text  = ["?????????","????????????","?????????????????????","?????????","?????????","??????","?????????","?????????","??????","?????????","????????????","?????????","????????????","?????????","?????????","??????","?????????"]
		tx   = thaiwords(text)
		os.system("mpg123 -f "+ vol + " " + tx)
	else:
		speak("mind your step")
	bell('1',vol)
	clear_q()
	return None


def remind_walking(t=30,vol='600',n=0):
	#bell('3',vol)
	if n == 1:
		text = ['????????????????????????','????????????','??????????????????????????????','??????????????????','??????????????????','??????????????????']
		tx   = thaiwords(text)
	elif n == 2:
		text = ["??????","?????????","?????????","????????????","??????????????????","?????????"]
		tx   = thaiwords(text)
	else:
		text  = ["?????????","????????????","?????????????????????","?????????","?????????","??????","?????????","?????????","??????","?????????","????????????","?????????","????????????","?????????","?????????","??????","?????????"]
		tx   = thaiwords(text)
	timeout = time.time() + 60*t   
	while True:
		if time.time() > timeout:
			break
		else:
			os.system("mpg123 -f "+ vol + " " + tx)
	# bell('1',vol)
	clear_q()
	return None


def remind_walking2(t=30,vol='600',n=0):
	tt = 0.5
	if n == 1:
		text  = [["?????????"],["????????????"],["?????????"],["?????????"],["?????????"],["??????"],["?????????"],["??????"]]
	elif n == 2:
		text =  [["?????????"],["????????????"],["?????????????????????"],["?????????"],["?????????"],["??????"],["?????????"],["?????????"],["??????"],["?????????"],["????????????"],["?????????"],["????????????"],["?????????"],["?????????"],["??????"],["?????????"]]
	elif n == 3:
		text = [["?????????"],["??????"],["?????????"],["??????"],["?????????"],["????????????"],["?????????????????????"],["?????????"]]
	elif n == 4:
		text  = [["??????"],["?????????"],["?????????"],["?????????"],["?????????"],["?????????"],["?????????"],["?????????"],["?????????"],["??????"],["?????????"],["??????"]]
	elif n == 5:
		text  = [["????????????????????????????????????1"],["????????????????????????????????????1"]]
		tt = 0
	elif n == 6:
		text  = [["?????????"],["????????????"],["?????????????????????"],["?????????"],["?????????"],["?????????"],["??????"],["?????????"],["?????????"]]
	elif n == 7:
		text = [['????????????????????????'],['????????????'],['??????????????????????????????'],['??????????????????'],['??????????????????'],['??????????????????']]
		tt = 0
	elif n == 8:
		text = [["??????"],["?????????"],["?????????"],["?????????"],["?????????"],["?????????"],["?????????"],["?????????"],["?????????"],["??????"],["?????????"],["??????"]]
	else:
		text =  [["?????????"],["?????????"],["?????????????????????"],["?????????"],["?????????"],["??????"],["?????????"],["?????????"],["??????"],["?????????"],["????????????"],["?????????"],["????????????"],["?????????"],["?????????"],["??????"],["?????????"]]
	
	timeout = time.time() + 60*t   
	while True:
		if time.time() > timeout:
			break
		else:
			for t in text:
				tx   = thaiwords(t)
				os.system("mpg123 -f "+ vol + " " + tx)
				time.sleep(tt)
	# bell('1',vol)
	clear_q()
	return None


def remind_walking_en(t=30,vol='10',n=0):
	if n == 1:
		text  = ["mind","your","step","unanxious","no desire","Ah happiness!","Ah happiness!"]
	elif n == 2:
		text = ["mind right step","mind left step"]
	elif n == 2:
		text = ["stepping right","stepping left"]
	else:
		text =  ["right go thus","left go thus","mind","your","breath","mind","your","movements","mind","the","mind","be","cheerful","be","here","and","now","left go thus","right go thus","left go thus"]
	
	timeout = time.time() + 60*t   
	while True:
		if time.time() > timeout:
			break
		else:
			for tx in text:
				speak(tx)
				time.sleep(0.5)
	# bell('1',vol)
	clear_q()
	return None


def remind_relax(t=30,vol='500'):
	bell('3',vol)
	text  = ["??????","?????????","????????????","????????????","?????????","??????","?????????","?????????","????????????","????????????","???????????????","????????????","?????????","????????????","?????????","??????","?????????","??????"]
	text += ["????????????","?????????","????????????","?????????","????????????","?????????????????????","????????????","?????????","?????????","??????????????????","?????????"]
	tx   = thwords(text)
	timeout = time.time() + 60*t   
	while True:
		if time.time() > timeout:
			break
		else:
			os.system("mpg123 -f "+ vol + " " + tx)
	bell('1',vol)
	clear_q()
	return None


def loop_sati(t=30,vol='500'):
	bell('3',vol)
	os.system('mpg123 -f ' + vol + ' -loop -1 ')
	proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../voices/sati-cut.mp3"])
	delay(t)
	proc.kill()
	bell('1',vol)
	clear_q()
	return None


def wise_one(c='off',vol="500"):
	proc = subprocess.Popen(["mpg123","-d","3","-f",vol,"-q","--loop","-1","../voices/buddho.mp3"])
	press_for_stop(c,proc)
	return None


def breathing_alpha_meditation(c='g',t=30):

	vol = "500"
	speak(str(t) + " minutes alpha sound")

	
	relax_thai()

	bell('3',vol)

	if len(c) == 1:
		ledc(c+c)
	else:
		ledc(c)

	alpha_wave(t)

	bell('1',vol)
	clear_q()
	return None


def alpha_meditation(m=60,t=15,c='off',vol="500"):


	speak(str(m) + " minutes alpha sound")
	if t > 0:
		speak("and "+ str(t) + " minutes bell sound")

	bell('3',vol)

	if len(c) == 1:
		ledc(c+c)
	else:
		ledc(c)

	if t == 0:
		alpha_wave(m)
		bell('1',vol)
	else:
		timeout = time.time() + 60*m
		while True:
		
			if time.time() > timeout:
				break
			else:
				alpha_wave(t)
				bell('1',vol)

	bell('1',vol)
	clear_q()
	return None


def slow_buddho(c='',t=30,vol='1000',alpha=True):
	ledc(c)
	th_stand = thwords(["?????????","?????????"])
	for i in range(3):
		os.system('mpg123 -f ' + vol + ' ' + th_stand)
		time.sleep(1)

	del th_stand
	gc.collect()

	if alpha:
		mp3 = "../sound/buddho0.mp3"
	else:
		mp3 = "../sound/buddho1.mp3"

	if t==0:
		proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1",mp3])
		press_for_stop(c,proc)
	else:
		proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1",mp3])
		delay(t)
		proc.kill()
	
	return None


def slow_buddho2(c='',t=30,vol='1000'):
	ledc(c)

	if t==0:
		proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../voices/buddho1.mp3"])
		press_for_stop(c,proc)
	else:
		proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../voices/buddho1.mp3"])
		delay(t)
		proc.kill()
	
	return None


def one_stage_en(c='',t=5):
	ledc(c)
	for i in range(3):
		speak("standing")
		time.sleep(1)
	proc = subprocess.Popen(["mpg123","-f","1000","-q","--loop","-1","../dataen/one_stage.mp3"])
	delay(t)
	proc.kill()
	return None

def one_stage_th_en(c='',t=5):

	th_right = thwords(['?????????','????????????','?????????'])
	th_left = thwords(['????????????','????????????','?????????'])
	th_stand = thwords(["?????????","?????????"])
	en_right = enwords(['right','goes','thus'])
	en_left = enwords(['left','goes','thus'])
	
	ledc(c)
	for i in range(3):
		os.system('mpg123 -f 1000 ' + th_stand)
		time.sleep(1)
		speak("standing")
		time.sleep(1)
	timeout = time.time() + 60*t
	while True:
		
		if time.time() > timeout:
			break
		else:
			os.system('mpg123 -f 1000 ' + th_right)
			time.sleep(1)
			os.system('mpg123 -f 1000 ' + th_left)
			time.sleep(1)

			os.system('mpg123 -f 1000 ' + en_right)
			time.sleep(1)
			os.system('mpg123 -f 1000 ' + en_left)
			time.sleep(1)

	del th_left
	del th_right
	del th_stand
	del en_left
	del en_right
	gc.collect()

	return None


def three_stages_th_en(c='',t=5,lg='th'):
	killPlayer()    
	speak(str(t) + " minutes 3 stages walking practice")
	if lg == 'th':
		stand = thwords(["?????????","?????????"])
		stage = thwords(["???????????????","?????????????????????","???????????????????????????"])
	elif lg == 'zh':
		stand = zhwords(["??????"])
		stage = zhwords(['??????','??????','??????'])
	elif lg == 'ja':
		stand = jawords(["???????????????"])
		stage = jawords(['??????????????????','??????','??????'])
	elif lg == 'ko':
		stand = kowords(["?????????"])
		stage = kowords(['?????????','????????????','??????'])
	else:
		stand = ""
		stage = enwords(['lifting','moving','treading'])

	en_stage = enwords(['lifting','moving','treading'])
	
	
	ledc(c)
	for i in range(3):
		os.system('mpg123 -f 1000 ' + stand)
		time.sleep(1)
		speak("standing")
		time.sleep(1)
	timeout = time.time() + 60*t
	while True:
		
		if time.time() > timeout:
			break
		else:
			os.system('mpg123 -f 1000 ' + stage)
			time.sleep(1)
			os.system('mpg123 -f 1000 ' + en_stage)
			time.sleep(1)

			os.system('mpg123 -f 1000 ' + stage)
			time.sleep(1)
			os.system('mpg123 -f 1000 ' + en_stage)
			time.sleep(1)

	del stage
	del stand
	del en_stage
	gc.collect() 

	return None


def six_stages_th_en(c='',t=5):

	killPlayer()   
	speak(str(t) + " minutes 6 stages walking practice")
	th_stand = thwords(["?????????","?????????"])
	th_stage = thwords(["????????????????????????","???????????????","?????????????????????","???????????????","??????????????????","???????????????"])
	en_stage = enwords(["heelup","lifting","moving","lowering","touching","pressing"])
	ledc(c)
	for i in range(3):
		os.system('mpg123 -f 1000 ' + th_stand)
		time.sleep(1)
		speak("standing")
		time.sleep(1)
	timeout = time.time() + 60*t
	
	while True:
		
		if time.time() > timeout:
			break
		else:
			os.system('mpg123 -f 1000 ' + th_stage)
			time.sleep(1)
			os.system('mpg123 -f 1000 ' + en_stage)
			time.sleep(1)

			os.system('mpg123 -f 1000 ' + th_stage)
			time.sleep(1)
			os.system('mpg123 -f 1000 ' + en_stage)
			time.sleep(1)

	del th_stage
	del th_stand
	del en_stage
	gc.collect() 

	return None

def read_sutta(d):
	speak(d["title"])
	lines = d["content"]
	# print(lines)
	for i in range(len(lines)):
		x = int(lines[i]["voice"])
		engine.setProperty('voice',es_voices[x]) 
		speak(lines[i]["text"])
	engine.setProperty('voice',es_voices[2])
	clear_q()
	return None

def meditation_goal(g=1,vol='2000'):
	if g == 1:
		text = " ../voices/dukkha.mp3 ../voices/goal.mp3"
	elif g == 2:
		text = " ../voices/howtopractice.mp3"
	elif g == 3:
		text = " ../voices/natureTruth3.mp3"
	elif g == 4:
		text = " ../voices/circle_of_dukkha_thai.mp3"
	elif g == 5:
		text = " ../voices/yoniso_thai.mp3"

	os.system("mpg123 -q -f " + vol + text)


def before_walk(l="th",vol="2000"):
	if l == "en":
		st = "percipient of what lies in front & behind, set a distance to meditate walking back & forth, your senses inwardly immersed, your mind not straying outwards"
		espeak(t,vol)
	else:
		st = " ../voices/before_walking.mp3"
		os.system("mpg123 -q -f "+ vol + st)       


def before_sit(l="th1",vol="2000"):
	if l == 'th1':
		st = " ../voices/at_the_present.mp3"
	else:
		st = " --loop 3 ../voices/cheerful_breathing.mp3"

	os.system("mpg123 -q -f "+ vol + st)
	relax_thai(vol)


def be_happy(vol='1000'):
	st = " --loop 3 ../voices/happy.mp3"
	os.system("mpg123 -q -f "+ vol + st)


def cheerful_payutto(t=5,vol='1000'):
	proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../sound/cheerful_payutto.mp3"])
	delay(t)
	proc.kill()
	return None

def cheerful_payutto2(t=5,vol='1000'):
	proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../sound/cheerful_citta.mp3"])
	delay(t)
	proc.kill()
	return None

def cheerful_payutto3(t=5,vol='1000'):
	proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../sound/cheerful_citta2.mp3"])
	delay(t)
	proc.kill()
	return None


def walking_reward():
	read_sutta(sutta["sutta"][0]) 
	return None


def remind_sati():
	speak("Do not forget to mind your breathing, mind your body movement and mind your mind.")
	text = " ../voices/sati.mp3"
	os.system("mpg123 -q -f 2000 "+text)


def remind_sati_bikkhu():
	entext = """
			Come you, monk, have mindfulness and situational awareness. Act with situational awareness 
			when going out and coming back; when looking ahead and aside; when bending and extending the limbs; 
			when bearing the outer robe, bowl and robes; when eating, drinking, chewing, and tasting; 
			when urinating and defecating; when walking, standing, sitting, sleeping, waking, speaking, and keeping silent.
			"""
	speak(entext)
	text = " ../voices/sati_bikkhu.mp3"
	os.system("mpg123 -q -f 2000 "+text)


def remind_right_sati():
	speak("Ardent, fully aware, and mindful, after removing avarice and sorrow regarding the world.")
	text = " ../voices/right_sati.mp3"
	os.system("mpg123 -q -f 2000 "+text)


def remind_dead():
	text = " ../voices/dead.mp3"
	os.system("mpg123 -q -f 2000 "+text)


def mixed_mode(c='',t=10,n=0,vol='1000'):
	if n == 14:
		pass
	else:
		# remind_b4walking(vol,'th')
		st = " ../voices/before_walking.mp3"
		os.system("mpg123 -q -f "+ vol + st) 

	if n == 1:
		one_stage_en(c,t)
	elif n == 2:
		lg = ['th','zh','ja','ko']
		random.shuffle(lg)
		three_stages_th_en(c,t,lg[0])
	elif n == 3:
		six_stages_th_en(c,t)
	elif n == 4:
		slow_buddho(c,t,'1000',True)
	elif n == 5:
		slow_buddho(c,t,'1000',False)
	elif n == 6:
		slow_buddho2(c,t)
	elif n == 7:
		anapanasati_walk(t)
	elif n == 8:
		remind_breathing(t,'1000','th5')
	elif n == 9:
		remind_walking2(t,vol,1)
	elif n == 10:
		remind_walking2(t,vol,2)
	elif n == 11:
		remind_walking_en(t,vol,1)
	elif n == 12:
		remind_walking_en(t,vol,0)
	elif n == 13:
		remind_walking2(t,vol,4)
	elif n == 14:
		remind_walking2(t,vol,5)
	elif n == 15:
		remind_walking2(t,vol,6)
	elif n == 16:
		remind_walking2(t,vol,3)
	elif n == 17:
		singing_bowl(t)
	elif n == 18:
		remind_walking_en(t,vol,2)
	else:
		one_stage_th_en(c,t)
	return None


def mixed_mode2(c='',t=10,n=0,vol='1000'):
	if n == 14:
		pass
	else:
		# remind_b4walking(vol,'th')
		st = " ../voices/before_walking.mp3"
		os.system("mpg123 -q -f "+ vol + st) 

# slow 1-4, fast 5-9, normal 10 -
	if n == 1:
		lg = ['th','zh','ja','ko']
		random.shuffle(lg)
		three_stages_th_en(c,t,lg[0])
	elif n == 2:
		six_stages_th_en(c,t)
	elif n == 5:
		slow_buddho2(c,t)
	elif n == 6:
		fast_buddho()
	elif n == 10:
		slow_buddho(c,t,'1000',True)
	elif n == 11:
		slow_buddho(c,t,'1000',False)
	elif n == 12:
		anapanasati_walk(t)
	elif n == 13:
		remind_breathing(t,'1000','th5')
	elif n == 14:
		remind_walking2(t,vol,1)
	elif n == 15:
		remind_walking2(t,vol,2)
	elif n == 16:
		remind_walking2(t,vol,3)
	elif n == 17:
		remind_walking2(t,vol,4)
	elif n == 18:
		remind_walking2(t,vol,5)
	elif n == 19:
		remind_walking2(t,vol,6)
	elif n == 20:
		singing_bowl(t)
	elif n == 90:
		remind_walking_en(t,vol,0)
	elif n == 91:
		remind_walking_en(t,vol,1)
	elif n == 92:
		remind_walking_en(t,vol,2)
	elif n == 93:
		one_stage_th_en(c,t)
	else:
		delay(t)
	return None


# log : timestamp data1 data2 
def lastlog(logpath='../mars/log/log.txt'):
	last_logs = []
	try:
		infile = open(logpath,'r')
		for line in infile :
			fx = line.strip().split()
			last_logs.append(fx)
		infile.close()
	except:
		pass
	return last_logs


def reclog(data,logpath='../mars/log/log.txt'):
	try:
		outfile = open(logpath,'a')
		outfile.write(str(data)+'\n')
		outfile.close()
		return 1
	except:
		return 0

#TEST
def vlc_one(t=0,fp='../mars/suttanta/',logpath="../mars/log/log_vlc1.txt",m=0,gain='0.1',rate='1.75'):
	files = get_files_list(fp,m)
	# print(files)
	timeout = 0
	if t > 0:
		tlimit = time.time() + t*60
		random.shuffle(files)
	b = lastlog(logpath)
	fn = len(files)
	if len(b) >= fn:
		infile = open(logpath,'w')
		infile.close()
		speak("end of playlist, clear log file")
		b = []
	n = 0
	for f in files:
		c = True
		if len(b) > 0:
			for a in b:
				if f == a[2]:
					c = False
				else:
					pass
		if t == 0 and n == fn:
			break
		elif c:
			n += 1
			fx = fp + f
			print(fx)
			try:
				tfx = media_info(fx)
				tx = tfx / (1000*float(rate))
				# print(tx)
				speak(str(round(tx/60))+" minutes")
				if t > 0:
					t = tlimit - time.time()
					if tx > t:
						tx = t
					print(t)
				cmd = "cvlc --play-and-exit --global-key-vol-up u --global-key-vol-down d" + " --gain " + gain + " --rate " + rate + " " + fx
				proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stdin=master)
				press_for_stop(led_color,proc,tx)
				data = str(time.time()) + " " + fp + " " + f
				reclog(data,logpath)
			except:
				speak('file not found')
				data = str(time.time()) + " " + fp + " " + f
				reclog(data,logpath)
			# speak('press button in 5 seconds for exit or wait to continue')
			ledc('r')
			t0 = time.time()
			board.button.wait_for_press(5) 
			if time.time() - t0 < 5:
				break
			elif  t > 0 and time.time() > tlimit:
				break
			ledc('d')


def dhamma_one(t=0,fp='../mars/',fpath='pyt.json',gain='0.1',rate='1.75',logpath="../mars/log/log1.txt"):
	files = json.load(open(fp+fpath,mode='r',newline='',encoding='UTF-8'))
	# print(files)
	timeout = 0
	if t > 0:
		tlimit = time.time() + t*60
		random.shuffle(files)
	b = lastlog(logpath)
	fn = len(files)
	if len(b) >= fn:
		infile = open(logpath,'w')
		infile.close()
		speak("end of playlist, clear log file")
		b = []
	n = 0
	for f in files:
		c = True
		f = f.split(',')
		if len(b) > 0:
			for a in b:
				if f[1] == a[2]:
					c = False
					n +=1
				else:
					pass
		if t == 0 and n == fn:
			infile = open(logpath,'w')
			infile.close()
			speak("end of playlist, just clear log file,please call again")
			break
		elif c:
			n += 1
			fx = fp + f[0] + '/' + f[1]
			print(fx)
			try:
				tfx = media_info(fx)
				tx = tfx / (1000*float(rate))
				# print(tx)
				speak(str(round(tx/60))+" minutes")
				if t > 0:
					t = tlimit - time.time()
					if tx > t:
						tx = t
					print(t)
				cmd = "cvlc --play-and-exit --global-key-vol-up u --global-key-vol-down d" + " --gain " + gain + " --rate " + rate + " " + fx
				proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stdin=master)
				press_for_stop(led_color,proc,tx)
				data = str(time.time()) + " " + f[0] + " " + f[1]
				reclog(data,logpath)
			except:
				speak('file not found')
				data = str(time.time()) + " " + f[0] + " " + f[1]
				reclog(data,logpath)
			# speak('press button in 5 seconds for exit or wait to continue')
			ledc('r')
			t0 = time.time()
			board.button.wait_for_press(5) 
			if time.time() - t0 < 5:
				break
			elif  t > 0 and time.time() > tlimit:
				break
			ledc('d')

def dhamma_two(t=0,fp='../mars/wisdom-en/',fpath='wisdom-en.json',gain='0.1',rate='1.25',logpath="../mars/log/log-en.txt"):
	files = json.load(open(fp+fpath,mode='r',newline='',encoding='UTF-8'))
	# print(files)
	timeout = 0
	if t > 0:
		tlimit = time.time() + t*60
		random.shuffle(files)
	b = lastlog(logpath)
	fn = len(files)
	if len(b) >= fn:
		infile = open(logpath,'w')
		infile.close()
		speak("end of playlist, clear log file")
		b = []
	n = 0
	for f in files:
		c = True
		f = f.split(',')
		if len(b) > 0:
			for a in b:
				if f[0] == a[2]:
					c = False
					n +=1
				else:
					pass
		if t == 0 and n == fn:
			infile = open(logpath,'w')
			infile.close()
			speak("end of playlist, just clear log file,please call again")
			break
		elif c:
			n += 1
			fx = fp + f[0]
			print(fx)
			try:
				tfx = media_info(fx)
				tx = tfx / (1000*float(rate))
				# print(tx)
				speak(f[1])
				speak(str(round(tx/60))+" minutes")
				if t > 0:
					t = tlimit - time.time()
					if tx > t:
						tx = t
					print(t)
				cmd = "cvlc --play-and-exit --global-key-vol-up u --global-key-vol-down d" + " --gain " + gain + " --rate " + rate + " " + fx
				proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stdin=master)
				press_for_stop(led_color,proc,tx)
				data = str(time.time()) + " " + f[0] 
				reclog(data,logpath)
			except:
				speak('file not found')
				data = str(time.time()) + " " + f[0]
				reclog(data,logpath)
			# speak('press button in 5 seconds for exit or wait to continue')
			ledc('r')
			t0 = time.time()
			board.button.wait_for_press(5) 
			if time.time() - t0 < 5:
				break
			elif  t > 0 and time.time() > tlimit:
				break
			ledc('d')


def dhamma_wisdom(t=0,gain='0.1',rate='1.50',log="../mars/log/log.txt"):
	dhamma_one(t,'../mars/','wisdom.json',gain,rate,log)


def dhamma_meditation(t=0,gain='0.1',rate='1.50',log="../mars/log/log-med.txt"):
	dhamma_one(t,'../mars/','pyt-med.json',gain,rate,log)
	

def dhamma_meditation2(t=0,fp='../mars/',logpath="../mars/log/log-med.txt",gain='0.1',rate='1.75'):
	files = [
	['payutto','05_31.wma'],
	['payutto','05_32.wma'],
	['payutto','05_33.wma'],
	['payutto','05_34.wma'],
	['payutto','05_35.wma'],
	['payutto','05_36.wma'],
	['payutto','05_37.wma'],
	['payutto','05_38.wma'],
	['payutto','05_39.wma'],
	['payutto','05_40.wma'],
	['payutto','05_41.wma'],
	['payutto','05_42.wma'],
	['payutto','05_43.wma'],
	['payutto','05_44.wma'],
	['payutto','05_45.wma'],
	['payutto','05_46.wma'],
	['payutto','05_47.wma'],
	['payutto','05_48.wma'],
	['payutto','05_49.wma'],
	['payutto','05_50.wma'],
	['payutto','05_51.wma']
	]

	timeout = 0
	if t > 0:
		tlimit = time.time() + t*60
		random.shuffle(files)
	b = lastlog()
	fn = len(files)
	if len(b) >= fn:
		infile = open(logpath,'w')
		infile.close()
		speak("end of playlist, clear log file")
		b = []
	n = 0
	for f in files:
		c = True
		if len(b) > 0:
			for a in b:
				if f[1] == a[2]:
					c = False
					n += 1
				else:
					pass
		if t == 0 and n == fn:
			infile = open(logpath,'w')
			infile.close()
			speak("end of playlist, just clear log file, please try again")
			break
		elif c:
			n += 1
			fx = fp + f[0] + '/' + f[1]
			print(fx)
			try:
				tfx = media_info(fx)
				tx = tfx / (1000*float(rate))
				# print(tx)
				speak(str(round(tx/60))+" minutes")
				what_time2()
				if t > 0:
					t = tlimit - time.time()
					if tx > t:
						tx = t
					print(t)
				cmd = "cvlc --play-and-exit --global-key-vol-up u --global-key-vol-down d" + " --gain " + gain + " --rate " + rate + " " + fx
				proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stdin=master)
				press_for_stop(led_color,proc,tx)
				data = str(time.time()) + " " + f[0] + " " + f[1]
				reclog(data)
			except:
				speak('file not found')
				data = str(time.time()) + " " + f[0] + " " + f[1]
				reclog(data)
			# speak('press button in 5 seconds for exit or wait to continue')
			ledc('r')
			t0 = time.time()
			board.button.wait_for_press(5) 
			if time.time() - t0 < 5:
				break
			elif  t > 0 and time.time() > tlimit:
				break
			ledc('d')


#return all files in series
def get_new_dhamma_files(fp="../datath/dhamma",m=0):
	new_files = []
	newfiles = ''
	for file in os.listdir(fp):
		if file.endswith(".mp3") or file.endswith(".m4a") or file.endswith(".wma"):
			new_files.append(os.path.join(fp, file))
	# print(new_files)
	if m == 0:
		new_files.sort()
	else:
		new_files = sorted(new_files)[::-1]
	random.shuffle(new_files)
	newfiles = " + ".join(str(x) for x in new_files) 
	# print(newfiles)
	del new_files
	gc.collect()
	return newfiles

# return limit files in series
def get_files_folder(fp="../mars/payutto",cmd='dhamma_four',limit=10,logpath='../mars/log/'):
	d1 = []
	old_files = set()
	new_files = set()

	for file in os.listdir(fp):
		if file.endswith(".mp3") or file.endswith(".m4a") or file.endswith(".wma"):
			new_files.add(file)

	upperlimit = len(new_files) - limit

	try:
		infile = open(logpath+cmd+'.txt','r')
		d = infile.readline()
		infile.close()
		# print(d)
		d=d.replace('[','')
		d=d.replace(']','')
		d=d.replace("'",'')
		d=d.replace(' ','')
		# print(d)
		d1 = d.split(',')
		print(len(d1))
		speak(str(len(d1)))
		if len(d1) > upperlimit:
			d1 = []
		# print(d1[cmd])
		for a in d1:
			old_files.add(a)
	except:
		old_files = set()

	# print(old_files)

	new_files = set()
	for file in os.listdir(fp):
		if file.endswith(".mp3") or file.endswith(".m4a") or file.endswith(".wma"):
			new_files.add(file)
	# print(new_files)
	new_files = new_files - old_files
	xfiles = []
	for x in new_files:
		xfiles.append(x)
	# random.shuffle(xfiles)
	xfiles.sort()
	outfile = open(logpath+cmd+'.txt','w')
	outfile.write(str(d1+xfiles[:limit]))
	outfile.close()
	
	if len(xfiles) > limit:
		# print(xfiles[:limit])
		newfiles = " + ".join(os.path.join(fp,x) for x in xfiles[:limit]) 
	else:
		newfiles = " + ".join(os.path.join(fp,x) for x in xfiles) 
	print(newfiles)
	del d1
	del old_files
	del new_files
	del xfiles
	gc.collect()
	return newfiles

# return limit files in list
def get_files_folder_list(fp="../mars/payutto",cmd='dhamma_four',limit=10,m=0,logpath='../mars/log/'):
	d1 = []
	old_files = set()
	new_files = set()

	for file in os.listdir(fp):
		if file.endswith(".mp3") or file.endswith(".m4a") or file.endswith(".wma"):
			new_files.add(file)

	upperlimit = len(new_files) - limit

	try:
		infile = open(logpath+cmd+'.txt','r')
		d = infile.readline()
		infile.close()
		# print(d)
		d=d.replace('[','')
		d=d.replace(']','')
		d=d.replace("'",'')
		d=d.replace(' ','')
		# print(d)
		d1 = d.split(',')
		print(len(d1))
		speak(str(len(d1)))
		if len(d1) > upperlimit:
			d1 = []
		# print(d1[cmd])
		for a in d1:
			old_files.add(a)
	except:
		old_files = set()

	# print(new_files)
	new_files = new_files - old_files
	xfiles = []
	for x in new_files:
		xfiles.append(x)
	# random.shuffle(xfiles)
	
	if m == 0:
		xfiles.sort()
	else:
		xfiles = sorted(xfiles)[::-1]

	outfile = open(logpath+cmd+'.txt','w')
	outfile.write(str(d1+xfiles[:limit]))
	outfile.close()
	
	if len(xfiles) > limit:
		xfiles = xfiles[:limit] 
	
	# print(newfiles)
	del d1
	del old_files
	del new_files
	gc.collect()
	return xfiles

#return files with path in list
def get_dhamma_list(fp="../datath/dhamma",m=0):
	new_files = []
	for file in os.listdir(fp):
		if file.endswith(".mp3") or file.endswith(".m4a") or file.endswith(".wma"):
			new_files.append(os.path.join(fp, file))
	# print(new_files)
	if m == 0:
		new_files.sort()
	else:
		random.shuffle(new_files)
	return new_files

#return files in list
def get_files_list(fp="../datath/dhamma",m=0):
	new_files = []
	for file in os.listdir(fp):
		if file.endswith(".mp3") or file.endswith(".m4a") or file.endswith(".wma"):
			new_files.append(file)
	# print(new_files)
	if m == 0:
		new_files.sort()
	else:
		random.shuffle(new_files)
	return new_files

# play vlc - files in folder
def play_dhamma_by_list(fp="../mars/payutto",cmd='dhamma_4',limit=4,gain='0.1',rate='1.75'):
	killPlayer()
	files= get_files_folder(fp,cmd,limit)
	cmd = "cvlc --play-and-exit --global-key-play-pause p --global-key-vol-up u --global-key-vol-down d --global-key-next f --global-key-jump+medium j  --global-key-stop s" + " --gain " + gain + " --rate " + rate + " " + files
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stdin=master)
	wait_for_vlc(proc)   
	del files
	gc.collect()

def play_vlc_by_list(fp="../mars/4nt2",cmd='dhamma_4nt2',limit=2,m=0,gain='0.1',rate='1.50'):
	killPlayer()
	files= get_files_folder_list(fp,cmd,limit,m)
	for fx in files:
		fx = fp + '/' + fx
		print(fx)
		try:
			tfx = media_info(fx)
			t = tfx / (1000*float(rate))
			speak(str(round(t/60))+" minutes")
			cmd = "cvlc --play-and-exit --global-key-play-pause p --global-key-vol-up u --global-key-vol-down d" + " --gain " + gain + " --rate " + rate + " " + fx
			proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stdin=master)
			press_for_stop(led_color,proc,t+5)
		except:
			speak("can not get duration")
		# speak('press button in 5 seconds for exit or wait to continue')
		ledc('r')
		t0 = time.time()
		board.button.wait_for_press(5) 
		if time.time() - t0 < 5:
			break
		ledc('d')
	del files
	gc.collect()

def play_vlc_inTime(fp="../mars/4nt2",cmd='dhamma_4nt2',t=60,rate='1.50',gain='0.1',n=0,logpath='../mars/log/'):
	killPlayer()

	tlimit = time.time() + t*60
	print(tlimit)
	
	files= get_files_list(fp,n)
	if len(files) < 5:
		speak("sorry, files less than 5")
	else:
		xfiles = []
		try:
			infile = open(logpath+cmd+'_inTime.txt','r')
			for line in infile :
				fx = line.strip().split()
				xfiles.append(fx[0])
			infile.close()
		except:
			pass
	    	
		zfiles = set(files) - set(xfiles)

		if len(zfiles) < 3:
			outfile = open(logpath+cmd+'_inTime.txt','w')
			outfile.close()
		else:
			files = []
			for z in zfiles:
				files.append(z)

		outfile = open(logpath+cmd+'_inTime.txt','a')
		
		for f in files:
			fx = fp + '/' + f
			print(fx)
			try:
				tfx = media_info(fx)
				tx = tfx / (1000*float(rate))
				print(tx)
				t = tlimit - time.time()
				if tx > t:
					tx = t
				print(t)
				cmd = "cvlc --play-and-exit --global-key-vol-up u --global-key-vol-down d" + " --gain " + gain + " --rate " + rate + " " + fx
				proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stdin=master)
				press_for_stop(led_color,proc,tx)
				outfile.write(str(f)+'\n')
			except:
				speak("can not get duration")
			# speak('press button in 5 seconds for exit or wait to continue')
			ledc('r')
			t0 = time.time()
			board.button.wait_for_press(5) 
			if time.time() - t0 < 5 or time.time() > tlimit:
				break
			ledc('d')
		outfile.close()
	del files
	gc.collect()
	return None


def play_vlc_all_inTime(fp="../mars/4nt2",t=60,rate='1.50',gain='0.1',n=0):
	killPlayer()
	if t == 0:
		t = 60
	tlimit = time.time() + t*60
	files= get_dhamma_list(fp,n)
	if len(files) < 1:
		speak('sorry, no file found')
	else:
		for fx in files:
			print(fx)
			tfx = media_info(fx)
			tx = tfx / (1000*float(rate))
			t = tlimit - time.time()
			if tx > t:
				tx = t
			cmd = "cvlc --play-and-exit --global-key-vol-up u --global-key-vol-down d" + " --gain " + gain + " --rate " + rate + " " + fx
			proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stdin=master)
			press_for_stop(led_color,proc,tx)
			# speak('press button in 5 seconds for exit or wait to continue')
			ledc('r')
			t0 = time.time()
			board.button.wait_for_press(5) 
			if time.time() - t0 < 5 or time.time() > tlimit:
				break
			ledc('d')
	del files
	gc.collect()
	return None
	
def play_dhamma_by_list_2(fp="../mars/payutto",cmd='dhamma_four',limit=10,uperlimit=300,gain='0.1',rate='1.75'):
	killPlayer()
	files= get_files_folder(fp,cmd,limit,uperlimit)
	cmd = "cvlc --play-and-exit --global-key-play-pause p --global-key-vol-up u --global-key-vol-down d --global-key-next f --global-key-jump+medium j  --global-key-stop s" + " --gain " + gain + " --rate " + rate + " " + files
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stdin=master)
	board.button.wait_for_press()
	try:
		keyboard = Controller()
		key = "f"
		keyboard. press(key)
		keyboard. release(key)
		# keyboard.press_and_release('f')
	except:
		pass
	press_for_stop('d',proc)   
	del files
	gc.collect()

def play_dhamma_by_list_3(fp="../mars/4nt2",gain='0.1',rate='1.50',n=1):
	killPlayer()
	files= get_dhamma_list(fp,n)
	for fx in files:
		print(fx)
		cmd = "cvlc --play-and-exit --global-key-play-pause p --global-key-vol-up u --global-key-vol-down d --global-key-jump+medium j  --global-key-stop s" + " --gain " + gain + " --rate " + rate + " " + fx
		subprocess.run(cmd, stdout=subprocess.PIPE, shell=True, stdin=master)
		# speak('press button in 5 seconds for exit or wait to continue')
		ledc('r')
		t0 = time.time()
		board.button.wait_for_press(5) 
		if time.time() - t0 < 5:
			break
		ledc('d')
	del files
	gc.collect()


def play_vlc_by_list_all(fp="../mars/4nt2",gain='0.1',rate='1.50',n=0):
	killPlayer()
	files= get_dhamma_list(fp,n)
	for fx in files:
		# print(fx)
		try:
			tfx = media_info(fx)
			t = tfx / (1000*float(rate))
			cmd = "cvlc --play-and-exit --global-key-play-pause p --global-key-vol-up u --global-key-vol-down d --global-key-jump+medium j" + " --gain " + gain + " --rate " + rate + " " + fx
			proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stdin=master)
			press_for_stop(led_color,proc,t+5)
		except:
			speak("can not get duration")
		# speak('press button in 5 seconds for exit or wait to continue')
		ledc('r')
		t0 = time.time()
		board.button.wait_for_press(5) 
		if time.time() - t0 < 5:
			break
		ledc('d')
	del files
	gc.collect()
	return None


# play vlc - a file
# press btn for stop
def play_vlc_file(fp="../mars/muttothai.m4a",rate='1.50',gain='0.10'):
	adjust_volume()
	tfx = media_info(fp)
	t = tfx / (1000*float(rate))
	cmd = "cvlc --play-and-exit --global-key-play-pause p --global-key-vol-up u --global-key-vol-down d --global-key-next f --gain " + gain + " --rate " + rate + " " + fp
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stdin=master)
	press_for_stop('d',proc,t)

# t minutes
def play_vlc_file2(fp="../mars/muttothai.m4a",t=0,st=0,rate='1.50',gain='0.1'):
	adjust_volume()
	cmd = "cvlc --loop --global-key-play-pause p --global-key-vol-up u --global-key-vol-down d --gain " + gain + " --rate " + rate + " --start-time " + str(st) + " " + fp
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stdin=master)
	press_for_stop('d',proc,t*60)  

# whole file
def play_vlc_file3(fp="../sound/bowl1.m4a",rate='1.00',gain='0.1',st=0):
	adjust_volume()
	cmd = "cvlc --play-and-exit --global-key-play-pause p --global-key-vol-up u --global-key-vol-down d --global-key-stop s --gain " + gain + " --rate " + rate + " --start-time " + str(st) + " " + fp
	subprocess.run(cmd, stdout=subprocess.PIPE, shell=True, stdin=master)

# TEST mp3

def play_my_dhamma(fp="../datath/dhamma",v='1',vol='2000'):
	files= get_new_dhamma_files(fp)
	cmd = "mpg123 -C -d " + v + " -f " + vol + " " + files
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stdin=master)
	ledc('o')
	board.button.wait_for_press()
	os.write(slave, b'f')
	ledc('d')
	board.button.wait_for_press()
	os.write(slave, b'f')
	ledc('o')
	board.button.wait_for_press()
	os.write(slave, b'f')
	ledc('d')
	board.button.wait_for_press()
	os.write(slave, b'f')
	ledc('o')
	board.button.wait_for_press()
	os.write(slave, b'f')
	press_for_stop(led_color,proc)
	killPlayer()    
	del files
	gc.collect() 
	return None
   
def play_dhamma_with_alarm(t=60,ts=15,fp="../datath/dhamma",vol='1000',b=True):
	files= get_new_dhamma_files(fp)
	cmd = "mpg123 -C -Z -f " + vol + " " + files
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stdin=master)
	color = ['o','d','b','g']
	n = t/ts
	i = 0
	timeout = time.time() + 60*t
	while True:
		random.shuffle(color)
		ledc(color[0])
		if time.time() > timeout or i == n:
			break
		delay(ts)
		os.write(slave, b's')
		if b:
			bell('1')
		else:
			what_time2()
		os.write(slave, b's')
		i = i + 1
	
	proc.kill()
	killPlayer()    
	del files
	gc.collect() 
	return None
	  
	
def play_mp3_with_alarm(t=60,ts=15,f="../datath/chanting/paticca.mp3",vol='1000',b=False):
	cmd = "mpg123 -C -Z -f " + vol + " " + f
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stdin=master)
	color = ['o','d','b','g']
	n = t/ts
	i = 0
	timeout = time.time() + 60*t
	while True:
		random.shuffle(color)
		ledc(color[0])
		if time.time() > timeout or i == n:
			break
		delay(ts)
		os.write(slave, b's')
		if b:
			bell('1')
		else:
			what_time2()
		os.write(slave, b's')
		i = i + 1
	
	proc.kill()
	killPlayer()    
	return None


def play_mp3_folder(fp="../datath/sutta",vol='1000',t=0):
	files= get_new_dhamma_files(fp)
	cmd = "mpg123 -C -Z -f " + vol + " " + files
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stdin=master)
	press_for_stop('off',proc,t*60) 
	killPlayer()    
	del files
	gc.collect() 
	return None
	
# Features
# hr 1 - 24
def x_minutes(hr=22):
	now = datetime.today().strftime('%H %M')
	tn = now.split()
	if hr > int(tn[0]):
		mn = (hr-int(tn[0]))*60 - int(tn[1])
	else:
		mn = 0
	return mn


def what_time():
	today = datetime.today().strftime('%H %M')
	speak("The time is " + today)
	clear_q()
	
	
def what_time2():
	today = datetime.today().strftime('%H %M')
	speak(today)
	clear_q()


def weekday():
	today = dt.datetime.now() 
	return int(today.strftime('%w'))


def what_day():
	today = datetime.today().strftime('%B %A %d')
	speak("Today is " + today)
	today = dt.datetime.now() 
	# text = ["??????????????????","?????????","weekday/%w","?????????","59/%d","???????????????","month/%m","????????????","59/%H","??????????????????","59/%M","????????????"]
	t = "??????????????????,?????????,weekday/%w,?????????,59/%d,???????????????,month/%m,????????????,59/%H,??????????????????,59/%M,????????????"
	t = t.replace("%w",today.strftime('%w'))
	t = t.replace("%d",today.strftime('%d'))
	t = t.replace("%m",today.strftime('%m'))
	t = t.replace("%H",today.strftime('%H'))
	t = t.replace("%M",today.strftime('%M'))
	text = t.split(',')
	stext = ""
	for i in range(len(text)):
		stext += " ../voices/thwords/" + text[i] + ".mp3"
	os.system("mpg123 -q -f 2100 "+stext)
	del t
	del text
	del stext
	gc.collect()
	clear_q()
	

def play_mp3(path,sec=0,vol='2000',c='off',d='1'):
	killPlayer()  
	proc = subprocess.Popen(["mpg123","-f",vol,"-d",d,"--loop","-1",path])
	press_for_stop(c,proc,sec)


def play_mp3_loop(path='',l='3',vol='2000',d='1'):
	killPlayer()  
	subprocess.run(["mpg123","-f",vol,"-d",d,"--loop",l,path])
	
	
	
def blessed_one(t=0,vol='1000'):
	play_mp3('../datath/chanting/paticca.mp3',t*60,vol)
	
	
def basic_chanting(t=0,vol='1000',c='off'):
	killPlayer() 
	command = "mpg123 -q -Z -f " + vol + " ../mars/basic_chanting/pahung.mp3 ../mars/basic_chanting/7tamnan.mp3 ../mars/basic_chanting/7kampee.mp3 ../mars/matika.mp3"
	proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	press_for_stop(c,proc,60*t) 


def basic_chanting2(t=0,vol="1500"):
	killPlayer()  
	ledc('off') 
	play_mp3_folder("../mars/sutta_chanting",vol,t)

	
def play_four_noble_truth_dhamma(t=0,r='1.75',g='0.1',c='o'):
	pass
	
	
def chinese_chanting(t=0,vol='1000',c='off'):
	killPlayer() 
	play_mp3_folder("../mars/chinese_chanting",vol,t) 
	

def play_daily_dependent_origination_thai():
	killPlayer()  
	speak("Dependent Origination Application in Everyday Life in Thai")
	proc = subprocess.Popen(["mpg123","-f","2000","../datath/buddhadham/paticcasamuppda.mp3"])
	press_for_stop(led_color,proc)


def play_buddha_thinking_thai():
	killPlayer()
	os.system("mpg123 -f 2000 -q ../voices/yoniso_thai.mp3")
	speak("Thai Buddhadham Yonisomanasikan")
	proc = subprocess.Popen(["mpg123","-f","2000","../datath/buddhadham/yoniso.mp3"])
	press_for_stop(led_color,proc)


def play_breathing_chanting_thai():
	killPlayer()
	if "loop" in words:
		speak("Thai Anapanasati chanting")
		proc = subprocess.Popen(["mpg123","-f","2000","-C","--loop","-1","../datath/chanting/anapanasati-cut.mp3"], stdin=master)
		press_for_stop(led_color,proc)
	else:
		subprocess.run(["mpg123","-f","2000","../datath/chanting/anapanasati-cut.mp3"])


def play_nature_truth_chanting_thai():
	killPlayer()
	speak("Thai Dhamma Ni yam chanting")
	proc = subprocess.Popen(["mpg123","-f","2000","-C","--loop","-1","../datath/chanting/dhammaniyam.mp3"], stdin=master)
	try:
		motion_detect(proc)
	except:
		press_for_stop(led_color,proc)


def play_dependent_origination_chanting_thai():
	killPlayer()  
	speak("Thai Itup paj ja ya ta Pa tij ja sa mup path chanting")
	proc = subprocess.Popen(["mpg123","-f","2000","-C","--loop","-1","../datath/chanting/ituppajjayata.mp3"], stdin=master)
	press_for_stop(led_color,proc)

def play_eight_fold_path_chanting_thai(vol="2000"):
	killPlayer()   
	# speak("Thai Noble 8 fold path chanting")
	proc = subprocess.Popen(["mpg123","-f",vol,"-C","--loop","-1","../datath/chanting/8.mp3"], stdin=master)
	press_for_stop('off',proc)


def play_eight_fold_path_chanting_english():
	killPlayer()   
	speak("English Noble 8 fold path chanting")
	proc = subprocess.Popen(["mpg123","-f","4000","-C","--loop","-1","../dataen/chanting/noble8fold.mp3"], stdin=master)
	press_for_stop(led_color,proc)


def play_8_fold_path_clip():
	killPlayer() 
	try:
		command = "export DISPLAY=:0.0; vlc -f --loop --video-on-top ../mp4/8.mp4"
		proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		press_for_stop('d',proc)      
	except:
		speak("sorry can not play video clip")


def play_dependent_origination_clip():
	killPlayer() 
	try:
		command = "export DISPLAY=:0.0; vlc -f --loop --video-on-top ../mp4/11.mp4"
		proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		press_for_stop('d',proc)      
	except:
		speak("sorry can not play video clip")


def english_chating(t=0,vol="1500"):
	killPlayer()  
	speak("English chanting")
	play_mp3_folder("../dataen/chanting",vol,t)


def thai_chanting(t=0,vol="1500"):
	killPlayer()   
	play_mp3_folder("../datath/chanting",vol,t)

def play_radio(vol='2000'):
	killPlayer()                                    
	if have_internet():
		# speak("Tibetan Buddhist internet radio")
		# proc = subprocess.Popen(["mpg123","-f","2000","-q","http://199.180.72.2:9097/lamrim"])
		proc = subprocess.Popen(["mpg123","-f",vol,"-q","http://202.142.203.28:8000/siangdham.mp3"])
		press_for_stop('d',proc)
	else:
		speak("sorry no internet connection")  


def play_radio_mp3(vol='8000'):
	killPlayer()                                    
	if have_internet():
		m = random.randint(1,6)
		if m == 1:
			url = 'http://www.thammapedia.com/listen/bdds/mp3'
		elif m == 2:
			url = 'http://www.thammapedia.com/listen/char/mp3'
		elif m == 3:
			url = 'http://www.thammapedia.com/listen/payutto/mp3'
		elif m == 4:
			url = 'http://www.thammapedia.com/listen/plean/mp3'
		elif m == 5:
			url = 'http://www.thammapedia.com/listen/bua/mp3'
		elif m == 6:
			url = 'http://www.thammapedia.com/listen/riean/mp3/'

		ext = 'mp3'

		mp3list = listFD(url, ext)
		random.shuffle(mp3list)

		for file in mp3list[:5]:
			print(file)
			proc = subprocess.Popen(["mpg123","-f",vol,file])
			press_for_stop('d',proc)
		
	else:
		speak("sorry no internet connection")  

# pip3 install --upgrade youtube-dl or
# python3 -m pip install -U yt-dlp
def play_youtube():
	m = random.randint(1,2)
	if m == 1:
		plist = 'https://www.youtube.com/playlist?list=PLWPh4CKxHuQ91lL9Nme_utg5qH4F4KTOg'
		#Buddhadasa
	elif m == 2:
		plist = 'https://www.youtube.com/playlist?list=PLFUPwJBonRX0CzKn3jRROtQDQ7UAQFRrK'
		#Payutto
	cmd = "yt-dlp -f 139 --playlist-random -o - " + plist + " | cvlc --rate 1.50 --gain 0.1 -"
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stdin=master)
	press_for_stop('d',proc) 

def play_my_playlist():
	adjust_volume()
	m = random.randint(1,4)
	if m == 1:
		speak("Dukkha, suffering, incapable of satisfying, painful")
		plist = 'https://www.youtube.com/playlist?list=PLamD6Dg8nlBT-ugSj7EMBvAY5TRP7P-kI'
		
	elif m == 2:
		speak("Samudaya, origin, arising of this dukkha")
		plist = 'https://www.youtube.com/playlist?list=PLamD6Dg8nlBR-RpzgZXSUlnM-s8KvwB8q'
		
	elif m == 3:
		speak("Nirodha, cessation, ending of this dukkha")
		plist = 'https://www.youtube.com/playlist?list=PLamD6Dg8nlBTKSF1s6Xp4l9tueaJ_UtNo'
		
	elif m == 4:
		speak("Marga, path, Noble Eightfold Path is the path leading to renouncement of tanha and cessation of dukkha")
		plist = 'https://www.youtube.com/playlist?list=PLamD6Dg8nlBSRuwJ2Y9kKqX6Vo6tc0QT_'
		
	cmd = "yt-dlp -f 139 --playlist-random -o - " + plist + " | cvlc --rate 1.50 --gain 0.1 -"
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stdin=master)
	press_for_stop('d',proc)  

def meditation_time():
	killPlayer()   
	text = """
			Meditation time will make 15 minutes bell sound, you may relax your self by walking then sitting. 
			For walking, set a distance to meditate walking back and forth, your senses inwardly immersed, your mind not straying outwards. 
			Lifting, Moving, Treading, slow moving and always mind your foot movement then you can increse your awakening sense, 
			or free walking, just focus on Treading, "
			For sitting, breathing in calm, breathing out down, always mind your breathing, your citta will not go around
			"""
	speak(text)
	del text
	gc.collect()
	proc = subprocess.Popen(["mpg123","-f","1500","-q","--loop","-1","../dataen/bell15min.mp3"])
	press_for_stop(led_color,proc)


def buddha_dhamma(n=1):
	killPlayer()    
	speak("Buddha dhamma")
	vlc_one(0,'../mars/buddhaDhamma/',"../mars/log/log_buddhadham.txt",0,'0.1','1.50')
	# play_vlc_by_list_all("../mars/buddhaDhamma",'0.1','1.50',n)


def dhamma_dhamma(t=60):
	dm = [['?????????????????????','bdd','2.00'],['???????????????','panya','1.75'],['??????','char','1.50'],['??????????????????','payutto','1.50']]	
	random.shuffle(dm)
	text = ['?????????','????????????','????????????',dm[0][0]]
	speakThai_mp3(text)
	play_vlc_inTime('../mars/'+dm[0][1],'dhamma_dhamma',t,dm[0][2],'0.1',1)
	# play_vlc_by_list('../mars/'+dm[0][1],'dhamma_dhamma')


def play_dhamma(vol='1000',fp='../datath/dhamma'):
	killPlayer()   
	speakThai_mp3(['?????????','????????????','?????????'])
	play_mp3("../voices/pay-attention.mp3",15)
	files= get_new_dhamma_files(fp)
	cmd = "mpg123 -C -z -f " + vol + " " + files
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stdin=master)
	leds.update(Leds.rgb_on(Color.YELLOW))
	board.button.wait_for_press()
	os.write(slave, b'f')
	leds.update(Leds.rgb_on(Color.RED))
	board.button.wait_for_press()
	os.write(slave, b'f')
	press_for_stop(led_color,proc)

#bdds + pyt
def play_dhamma2(t=0):
	dhamma_one(t,'../mars/','satipanya.json','0.1','1.75','../mars/log/log2.txt')
	# dhamma_one(t=0,fp='../mars/',fpath='pyt.json',gain='0.1',rate='1.75',logpath="../mars/log/log1.txt"):
	# play_vlc_by_list("../datath/dhamma","dhamma_2",4,0)

def play_dhamma3(t=0):
	dhamma_one(t,'../mars/','bddspanya.json','0.1','1.75','../mars/log/log3.txt')


def play_sutra(t=0,vol='1000',fp='../datath/sutta'):
	killPlayer()
	files= get_new_dhamma_files(fp)
	cmd = "mpg123 -C -Z -f " + vol + " " + files
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stdin=master)
	press_for_stop('off',proc,60*t)


def play_sutra2(t=0):
	killPlayer()
	i = random.choices([1,2,3,4],[7,5,3,1])[0]
	if i == 1:
		play_vlc_all_inTime("../datath/sutra",t,'1.50','0.1',0)
	elif i == 2:
		play_vlc_all_inTime("../mars/sutta",t,'1.50','0.1',0)
	else:
		play_vlc_all_inTime("../mars/sutta3",t,'1.50','0.1',0)


def play_buddha_story():
	speak("play buddha story")
	killPlayer()                
	try:
		command = "export DISPLAY=:0.0; vlc -f --stop-time 453 --play-and-exit ../mp4/buddha-story.mp4"
		proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		press_for_stop('d',proc,455)
		killPlayer() 
	except:
		speak("sorry can not play video clip")


def walking_meditation_count(c='oo'):
	
	speak("one stage walking practice, please count your step then you can verify it in the end")

	th_right = thwords(['?????????','????????????','?????????'])
	th_left = thwords(['????????????','????????????','?????????'])
	th_stand = thwords(["?????????","?????????"])
	en_right = enwords(['right','goes','thus'])
	en_left = enwords(['left','goes','thus'])
	
	ledc(c)
	for i in range(3):
		os.system('mpg123 -f 1000 ' + th_stand)
		time.sleep(1)
		speak("standing")
		time.sleep(1)

	bell()
	count = 0
	t = random.randint(5,10)
	timeout = time.time() + 60*t
	while True:
		
		if time.time() > timeout:
			break
		else:
			t1 = random.randint(1,2)
			t2 = random.randint(1,2)
			os.system('mpg123 -f 1000 ' + th_right)
			time.sleep(t1)
			os.system('mpg123 -f 1000 ' + th_left)
			time.sleep(t2)

			os.system('mpg123 -f 1000 ' + en_right)
			time.sleep(t2)
			os.system('mpg123 -f 1000 ' + en_left)
			time.sleep(t1)

			count +=1

	bell('1')
	speak("you walk for " + str(count*4) + "steps")

	del th_left
	del th_right
	del th_stand
	del en_left
	del en_right
	gc.collect()

	return None


def counting_walk(t=15,fast=False,l='th',vol='2000'):

	if l == 'en':
		tt = "Percipient of what lies in front & behind, set a distance to meditate walking back & forth, your senses inwardly immersed, your mind not straying outwards, mind your step"
		speak(tt)
		t1 = 0
		tx = engwords(['1','2','3','4','5','6','7','8','9','10'])
		tx_list = tx.split(' ')

	elif l == 'zh':
		os.system('mpg123 -q -f ' + vol + ' ../voices/zh/chinese_walk.mp3')
		t1 = 0
		tx = zhwords(['1','2','3','4','5','6','7','8','9','10'])
		tx_list = tx.split(' ')

	elif l == 'ja':
		os.system('mpg123 -q -f ' + vol + ' ../voices/ja/japanese_walk.mp3')
		t1 = 0
		tx = jawords(['1','2','3','4','5','6','7','8','9','10'])
		tx_list = tx.split(' ')

	elif l == 'ko':
		os.system('mpg123 -q -f ' + vol + ' ../voices/ko/b4walk.mp3')
		t1 = 0
		tx = kowords(['1','2','3','4','5','6','7','8','9','10'])
		tx_list = tx.split(' ')

	elif l == 'wav':
		os.system('mpg123 -q ../voices/before_walking.mp3')
		t1 = 0.5
		tx = thaiwordswav(['1','2','3','4','5','6','7','8','9','10'])
		tx_list = tx.split(' ')

	else:
		os.system('mpg123 -q -f ' + vol + ' ../voices/before_walking.mp3')
		t1 = 0.25
		tx = thaiwords(['1','2','3','4','5','6','7','8','9','10'])
		tx_list = tx.split(' ')
		
	if l == 'wav':
		# cmd = 'mplayer -volume 1 '
		cmd = 'aplay '
		# cmd = 'cvlc --play-and-exit --gain 1 '
	else:
		cmd = 'mpg123 -q -f ' + vol + ' '

	# cmd = 'cvlc --play-and-exit --gain 1 '
	i  = 1
	n = 5
	bell('1')
	timeout = time.time() + 60*t
	while True:
		print(n)        
		if time.time() > timeout and i < 11:
			break
		else:
			if fast:
				os.system(cmd + tx_list[i])
				time.sleep(t1)
				i += 1
			else:
				os.system(cmd + tx_list[i])
				time.sleep(t1)
				os.system(cmd + tx_list[i])
				time.sleep(t1)
				i += 1

		if i>n and n < 10:
			n += 1
			i = 1  
		elif i>10:
			n = 5
			i = 1  
	return None 


def kanaanub(t=15,fast=False,l='th',vol='10'):

	if l == 'en':
		tt = "percipient of what lies in front & behind, set a distance to meditate walking back & forth, your senses inwardly immersed, your mind not straying outwards."
		speak(tt)
		t1 = 0
		tx_list = ['0','1','2','3','4','5','6','7','8','9','10']
	elif l == 'zh':
		os.system('mpg123 -q -f 1000 ../voices/zh/chinese_walk.mp3')
		t1 = 0
		tx_list = ['Ling','Yi','Er','San','Si','Wu','Liu','Qi','Ba','Jiu','Shi']       
	else:
		os.system('mpg123 -q -f 1000 ../voices/before_walking.mp3')
		t1 = 0
		tx_list = ['soon','noong','song','sam','see','ha','hok','jed','pad','kao','sib']

	cmd = "espeak -s 150 -a " + vol + " "

	i  = 1
	n = 5
	bell('1')
	timeout = time.time() + 60*t
	while True:
		print(n)        
		if time.time() > timeout and i < 11:
			break
		else:
			if fast:
				os.system(cmd + tx_list[i])
				time.sleep(t1)
				i += 1
			else:
				os.system(cmd + tx_list[i])
				time.sleep(t1)
				os.system(cmd + tx_list[i])
				time.sleep(t1)
				i += 1

		if i>n and n < 10:
			n += 1
			i = 1  
		elif i>10:
			n = 5
			i = 1  
	return None 


def heart_sutra(t=0,c='d',vol="1000"):
	ledc(c)
	if t == 0:
		proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../dataen/chanting/heart-sutra.mp3"])
		press_for_stop(c,proc)
	else:
		proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../dataen/chanting/heart-sutra.mp3"])
		delay(t)
		proc.kill()
		clear_q()
	return None

def wooden_gong_sound(t=0,vol='2000',c='off'):
	ledc(c)
	if t == 0:
		proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../sound/pakhue.mp3"])
		press_for_stop(c,proc)
	else:
		proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../sound/pakhue.mp3"])
		delay(t)
		proc.kill()
		clear_q()
	return None



def raining_meditation(t=0,c='d',vol="2000"):
	ledc(c)
	if t == 0:
		proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../sound/rainymood.mp3"])
		press_for_stop(c,proc)
	else:
		proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../sound/rainymood.mp3"])
		delay(t)
		proc.kill()
		clear_q()
	return None


def thunder_meditation(t=0,c='d',vol="2000"):
	ledc(c)
	if t == 0:
		proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../sound/thunderstorm.mp3"])
		press_for_stop(c,proc)
	else:
		proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../sound/thunderstorm.mp3"])
		delay(t)
		proc.kill()
		clear_q()
	return None


def jungle_meditation(t=0,c='d',vol="2000"):
	ledc(c)
	if t == 0:
		proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../sound/jungle.mp3"])
		press_for_stop(c,proc)
	else:
		proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../sound/jungle.mp3"])
		delay(t)
		proc.kill()
		clear_q()
	return None


def tibetan_meditation(t=0,c='d',vol="2000"):
	ledc(c)
	if t == 0:
		proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../sound/tibetan.mp3"])
		press_for_stop(c,proc)
	else:
		proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../sound/tibetan.mp3"])
		delay(t)
		proc.kill()
		clear_q()
	return None


def om_meditation(t=0,c='d',vol="2000"):
	ledc(c)
	if t == 0:
		proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../sound/OM417Hz.mp3"])
		press_for_stop(c,proc)
	else:
		proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../sound/OM417Hz.mp3"])
		delay(t)
		proc.kill()
		clear_q()
	return None

# FOR MARTIAN MONK ONLY
def play_plants(w):
	plants = ['cells.mp4','light-sd.mp4','seed-sd.mp4','water-sd.mp4','co2.mp4','npk.mp4']
	plists = ['cell','light','seed','water','carbon','food']           
	try:
		i = plists.index(w)
		speak("Play Plants " + w)
		command = "export DISPLAY=:0.0; vlc -f --loop --video-on-top ../mars/plants/" + plants[i]
		proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		press_for_stop(led_color,proc)
	except:
		speak("sorry can not play video clip")

def play_tripataka_chapter(p):
	killPlayer()  
	speak("play Thai reading Tripitaka Chapter " + p)
	proc = subprocess.Popen(["mpg123","-d","2","-f","3000","../mars/tripitaka/Tripidok" + p + ".mp3"])
	press_for_stop('d',proc)

def pali_chanting():
	killPlayer()  
	speak("Pali grammar chanting")
	proc = subprocess.Popen(["mpg123","-f","3000","../mars/monk/pali.mp3"])
	press_for_stop('d',proc)

def morning_merit(vol="1000"):
	killPlayer()  
	proc = subprocess.Popen(["mpg123","-f",vol,"../datath/chanting/morning-merit.mp3"])
	press_for_stop('d',proc,192)
	
def tibetan_metta_chanting(vol="1000"):
	killPlayer()  
	proc = subprocess.Popen(["mpg123","-f",vol,"../mars/chinese_chanting/tibetanmetta.mp3"])
	press_for_stop('d',proc,545)
	
def metta_chanting(vol="1000"):
	killPlayer()  
	proc = subprocess.Popen(["mpg123","-f",vol,"--loop","-1","../mars/basic_chanting/metta-sutta-chanting.mp3"])
	press_for_stop('d',proc,1800)
	
def metta_chanting_thai(vol="1000",t=1800):
	killPlayer()  
	proc = subprocess.Popen(["mpg123","-f",vol,"-Z","../mars/basic_chanting/metta-sutta.mp3","../mars/basic_chanting/metta-sutta-chanting.mp3"])
	press_for_stop('d',proc,t)

def hdmi_display(s='on'):
	if s == 'off':
		os.system("/opt/vc/bin/tvservice -o")
	else:
		os.system("/opt/vc/bin/tvservice -p")
	espeak("turn display " + s, '5')
	return None	

# sitting 1 hr
def testing_mode2():
	killPlayer()
	bell('3') 
	cheerful  = [['../mp4/BloomingFlowers.mp4','154'],['../mp4/flowers-blooming.mp4','192'],['../mp4/flowers.mp4','120']]
	i = random.randint(0,2)              
	try:
		command = "cvlc -f --loop --stop-time " + cheerful[i][1] + " --video-on-top " + cheerful[i][0]
		proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		# delay(5)
		board.button.wait_for_press(2*int(cheerful[i][1]))
		proc.kill()
		killPlayer() 
	except:
		speak("sorry can not play video clip")
	my_sun()
	bell('1')
	before_sit('th')
	bell('1')   
	singing_bowl(30)
	bell('1')
	singing_bowl(15)
	bell('1')
	singing_bowl(15)
	bell('1')
	clear_q()
	return None

# walking 1 hr
def testing_mode1():
	meditation_goal(1)
	vol = '2000'
	lg = ['th','en','zh','ja','ko']
	lgx = random.choice(lg)
	walk = [0,1,2,4,5,7,8,9,10,12,13,15,18]
	i = random.randint(1,3)
	for x in range(i):
		random.shuffle(walk)

	#bell('3')
	#relax_walk(5,'1000')
	#sun = ['sun1.gif','sun2.gif','sun3.gif','sun4.gif']
	#i = random.randint(0,3) 
	#command = "export DISPLAY=:0.0; python3 testgif.py -f full -p ../images/" + sun[i]
	#proc1 = subprocess.Popen(command, shell=True)
	bell('1')
	speak("mind your step")
	counting_walk(10,False,lgx)
	bell('1')
	speak("mind your step")
	counting_walk(10,True,lgx)
	bell('1')
	
	for i in range(1,5):
		t = random.randint(2,6)
		n = random.randint(0,1)
		if n == 0:
			mixed_mode('off',t,walk[i],vol)
			mixed_mode('off',10-t,14,vol)
		else:
			mixed_mode('off',10,walk[i])

	#proc1.kill()
	#pkill_proc_name("testgif")
	bell('1')
	clear_q()
	return None


def sitting_meditation(n=0,t=60,vol='1000'):
	# a = buddha_day()
	play_mp3('../sound/namo.mp3',161,vol)
	relax_thai()
	if n == 0:
		play_vlc_file3("../datath/chanting/dhammajak.mp3")
		play_vlc_file3("../datath/chanting/8.mp3")
		now = datetime.today().strftime('%H %M')
		tn = now.split()
		t = (22-int(tn[0]))*60 - int(tn[1]) - 5 #bowls
	else:
		play_vlc_file3("../datath/chanting/dhammaniyam.mp3")
		play_vlc_file3("../datath/chanting/ituppajjayata.mp3")
		t = t - 20
	
	bowls = ["../sound/bowl1.m4a","../sound/bowl2.m4a","../sound/bowl3.m4a","../sound/bowl4.m4a","../sound/bowl5.m4a"]
	play_vlc_file3(random.choice(bowls))
	play_vlc_file("../sound/rattana.mp3",'1.00')
	killPlayer()
	dhamma_wisdom(t)
	# dhamma_dhamma(t)
	# if a == 8 or a == 15:
	# 	m = random.choices([8,6,7,9],[5,4,3,2])[0]
	# else:
	# 	m = random.choices([4,8,5],[5,3,1])[0]
	# print(m)
	# if m == 4:
	# 	play_mp3_folder("../datath/sutta",'1500',t)
	# elif m == 5:
	# 	play_vlc_all_inTime("../mars/12paticca",t,'1.50')
	# 	# play_mp3_folder("../mars/45pope",'2000',t)
	# elif m == 6:
	# 	play_vlc_all_inTime("../mars/char",t,'1.50')
	# elif m == 7:
	# 	play_vlc_all_inTime("../mars/gold",t,'1.50')
	# elif m == 8:
	# 	play_vlc_all_inTime("../mars/panya",t,'1.50')
	# else:
	# 	play_vlc_all_inTime("../mars/bdd",t,'1.50')
	bell('3')

def testing_mode3():
	meditation_goal(1)
	lg = ['th','en','zh','ja']
	lgx = random.choice(lg)

	bell('3')
	relax_walk(5,'1000')
	sun = ['sun1.gif','sun2.gif','sun3.gif','sun4.gif']
	i = random.randint(0,3) 
	
	command = "export DISPLAY=:0.0; python3 testgif.py -f full -p ../images/" + sun[i]
	proc1 = subprocess.Popen(command, shell=True)
	bell('1')
	counting_walk(5,False,lgx)
	bell('1')
	counting_walk(5,True,lgx)
	bell('1')
	slow_buddho('off',10)
	slow_buddho2('off',5)

	proc1.kill()
	pkill_proc_name("testgif")

	testing_mode2()
	
	return None

def umong_testing_4():
	speak("Testing 4, meditation practice at watumong")
	mm = True
	now = int(datetime.today().strftime('%H'))
	if now < 3:
		mn = x_minutes(3)
		wooden_gong_sound(mn,'500','off')
		bell('1')
		relax_thai()
		fast_buddho('off',60,'500')
		mm = False
	elif now < 5:
		mm = False

	elif now > 16 and now < 21:
		if now < 20:
			a = buddha_day()
			if a == 0:
				mn = x_minutes(20)
				dhamma_wisdom(mn)
			else:
				mn = x_minutes(19)
				dhamma_wisdom(mn)
				play_vlc_file("../mars/bdd/7005.mp3",'2.00')
				play_vlc_file("../mars/bdd/7007.mp3",'2.00')
		# efp = ["../datath/chanting/anapanasati.mp3","../datath/chanting/8.mp3"]
		# play_vlc_file(random.choice(efp),'1.00')
		adjust_volume()
		i = weekday()%2
		mn = x_minutes(22) 
		if i == 0:
			i = random.randint(0,2)
			if i == 0:
				dm = [["../mars/zen","1.50","0.10"],["../mars/zen2","2.00","0.10"]]
				dmc = random.choices(dm,[2,1])[0]
				play_vlc_all_inTime(dmc[0],mn,dmc[1],dmc[2],1)
			else:
				play_sutra(mn,'800')			
		else:
			dm = [["../mars/buddhaDhamma","1.50","0.075"],["../mars/wisdom-en/mp3","1.00","0.10"]]
			dmc = random.choices(dm,[2,1])[0]
			play_vlc_all_inTime(dmc[0],mn,dmc[1],dmc[2],1)
			# play_vlc_all_inTime(random.choices(dm,[5,1])[0],mn,'1.50','0.1',1)
			
	if mm:
		mn = x_minutes(24)
		fast_buddho('off',mn,'500')
		delay(120)
		bell_5minutes()
		wooden_gong_sound(30,'400','off')
		anapanasati_walk(10,"20%")
		wooden_gong_sound(10,'400','off')
		singing_bowl(5)
		relax_thai()
		breathing1('off',60,'500')
		# i = random.choice([0,1,2,3,4])
		# if i == 0:
		# 	fast_buddho_hiphop('off',60,'500')
		# elif i ==1 :
		# 	kidnor('off',60,'500')
		# elif i == 2:
		# 	buddhodeekwa('off',60,'500')
		# elif i == 3:
		# 	breathing1('off',60,'500')
		# else:
		# 	fast_buddho('off',60,'500')
		bell('1')
		play_mp3('../mars/monk/rbut.mp3',127,'800')

	a = buddha_day()
	if a == 0:
		efp2 = [["../dataen/chanting/anapanasati.mp3",0,"tbc"]]
		efp2 += [["../dataen/chanting/noble8fold.mp3",0,"tbc"]]
		efp2 += [["../datath/chanting/anapanasati.mp3",1,["../mars/anapanasati16.mp3","../mars/bdd/8014.mp3","../mars/bdd/1006.mp3","../mars/bdd/10019.mp3"]]]
		efp2 += [["../datath/chanting/8.mp3",1,["../datath/dhamma/bdd_8foldpath.mp3","../mars/pyt/09_45.wma","../mars/bdd/8025.mp3","../mars/payutto/04_12.wma"]]]
		efp2c = random.choice(efp2)
		play_vlc_file(efp2c[0],'1.00')
		if efp2c[1] == 1:
			play_vlc_file(random.choice(efp2c[2]),'1.50')
		else:
			efp = ["../datath/chanting/paticca.mp3","../dataen/chanting/heart-sutra.mp3"]
			play_vlc_file(random.choice(efp),'1.00')
			efp3 = ["../datath/chanting/sungkharn.mp3","../datath/chanting/dhammaniyam.mp3","../datath/chanting/Bhadhdherattakadha.mp3","../datath/chanting/ituppajjayata.mp3"]
			play_vlc_file(random.choice(efp3),'1.00')
	else:
		play_vlc_file("../mars/bdd/7004.mp3",'2.00')
		play_vlc_file("../mars/bdd/7006.mp3",'2.00')
	mn = 90
	i = weekday()
	if i == 1:
		dm = ["../mars/12paticca","../mars/4nt"]
		play_vlc_all_inTime(random.choice(dm),mn,'1.50','0.1',1)
		# play_vlc_all_inTime("../mars/4nt",mn,'1.50','0.1',1)
	elif i == 2:
		bd = ["../mars/gold","../mars/bdd3","../mars/bdd-3536"]
		play_vlc_all_inTime(random.choice(bd),mn,'1.50','0.1',1)
		# play_vlc_all_inTime("../mars/gold",mn,'1.50','0.1',1)
	elif i == 3:
		play_vlc_all_inTime("../mars/payutto6264",mn,'1.50','0.1',1)
	elif i == 4:
		dm = ["../datath/dhamma","../mars/4nt2"]
		play_vlc_all_inTime(random.choice(dm),mn,'1.50','0.1',1)
		# play_vlc_all_inTime("../datath/dhamma",mn,'1.50','0.1',1)
	elif i == 5:
		play_vlc_all_inTime("../mars/zen",mn,'1.50','0.1',1)
	elif i == 6:
		st = ["../mars/sutta","../mars/sutta3"]
		play_vlc_all_inTime(random.choice(st),mn,'1.50','0.1',1)
	else:
		play_vlc_all_inTime("../mars/wisdom-en/mp3",mn,'1.00','0.1',1)
	return None

def testing_mode5():
	blessed_one(5)
	fast_buddho('off',30,'500')
	chinese_chanting(60)
	os.system("sudo shutdown now")
	return None

def testing_mode7():
	what_time()
	now = int(datetime.today().strftime('%H'))
	if now < 17:
		testing_mode1()
	elif now == 17:
		testing_10()
	elif 17 < now and now < 20:
		wooden_gong_sound(30)
		fast_buddho('off',10,'500')
		sitting_meditation(0,60,'1500')
		bell('1')
		ledc("off")
		now = datetime.today().strftime('%H %M')
		tn = now.split()
		mn = (22-int(tn[0]))*60 - int(tn[1])
		basic_chanting(mn,'300')
		mn = x_minutes(24) + 120
		delay(mn)
		fast_buddho('off',5,'500')
		morning_practice('off','500')
	else:
		ledc('d')
		now = datetime.today().strftime('%H %M')
		tn = now.split()
		mn = (22-int(tn[0]))*60 - int(tn[1])
		m = random.randint(0,3) 
		if m == 0:
			play_mp3('../sound/528Hz.mp3',mn*60)
		elif m == 1:
			fast_buddho('off',mn,'500')
		elif m == 2:
			play_mp3('../sound/432Hz.mp3',mn*60)
		elif m == 3:
			wooden_gong_sound(mn)
		ledc('off')
		mn = x_minutes(24) + 120
		delay(mn)
		fast_buddho('off',5,'500')
		morning_practice('off','500')
	return None

def testing_10():
	buddha_day()
	testing_mode1()
	fast_buddho('off',10,'500')
	sitting_meditation(0,60,'1500')
	ledc('off')
	mn = x_minutes(24) + 120
	delay(mn)
	fast_buddho('off',5,'500')
	morning_practice('off','600')
	return None

#For BuddhaDay
def testing_mode9():
	what_time()
	fast_buddho('off',5,'500')
	sitting_meditation(0,60,'1000')
	mn = x_minutes(24) + 120
	delay(mn)
	fast_buddho('off',5,'500')
	morning_practice('off','500')
	return None
	
def testing_mode6():
	what_time()
	testing_mode1()
	fast_buddho('off',10,'500')
	remind_breathing(5,'500','th2')
	singing_bowl(55)
	bell('1')
	now = datetime.today().strftime('%H %M')
	tn = now.split()
	mn = (22-int(tn[0]))*60 - int(tn[1])
	basic_chanting(mn,'300')
	os.system("sudo shutdown now")
	return None
	
def meditation_7():
	m = random.randint(1,3)
	meditation_goal(1)
	bell('3')
	before_walk()
	anapanasati_walk(10)
	bell('1')
	delay(4)
	before_sit()
	sitting_meditation(1,30,'1000')
	bell('3')
	return None
	
def meditation_3():
	meditation_goal(1)
	before_walk()
	slow_buddho('off',10,'1000',False)
	bell('1')
	delay(2)
	before_sit()
	jungle_meditation(15,'off','4000')
	raining_meditation(15,'off','4000')
	thunder_meditation(15,'off','4000')
	music_meditation(15,'off','4000')
	bell('3')  
	return None

def meditation_5():
	meditation_goal(1)
	bell('3')
	before_walk()
	musk_walk(10)
	bell('1')
	delay(4)
	before_sit()
	bell('1')
	delay(15)
	bell('1')
	delay(15)
	
	bell('1')
	delay(15)
	bell('1')
	delay(15)
	
	bell('3')
	return None

def meditation_1():
	meditation_goal(1)
	bell('1')
	play_mp3("../sound/buddho-30m.mp3",1800)
	bell('1')
	delay(3)
	bell('1')
	play_mp3("../sound/walking-1hr.mp3",3600)
	bell('3')
	return None
	
	
def meditation_2():
	meditation_goal(1)
	bell('3')
	before_walk()
	musk_walk(10)
	bell('1')
	delay(4)
	before_sit()
	jungle_meditation(15,'off','4000')
	raining_meditation(15,'off','4000')
	thunder_meditation(15,'off','4000')
	music_meditation(15,'off','4000')
	bell('3')  
	return None
	

def meditation_6():
	meditation_goal(1)
	bell('3')
	before_walk()
	slow_buddho('off',10,'1000',False)
	bell('1')
	delay(4)
	testing_mode2()
	
	delay(3)
	before_walk()
	slow_buddho('off',10,'1000',False)
	bell('1')
	delay(2)
	testing_mode2()
	
	delay(3)
	before_walk()
	slow_buddho('off',10,'1000',False)
	bell('1')
	delay(2)
	testing_mode2()
	
	delay(3)
	before_walk()
	slow_buddho('off',10,'1000',False)
	bell('1')
	delay(2)
	testing_mode2()
	bell('3')
	return None
	
def meditation_4():
	meditation_goal(1)
	bell('3')
	before_walk()
	anapanasati_walk(10)
	bell('1')
	delay(4)
	before_sit()
	singing_bowl(60)
	bell('1')
	
	delay(3)
	before_walk()
	musk_walk(10)
	bell('1')
	delay(2)
	before_sit()
	om_meditation(30)
	tibetan_meditation(30)
	bell('1')
	
	delay(3)
	before_walk()
	slow_buddho('off',10,'1000',False)
	bell('1')
	delay(2)
	before_sit()
	jungle_meditation(15,'off','4000')
	raining_meditation(15,'off','4000')
	thunder_meditation(15,'off','4000')
	music_meditation(15,'off','4000')
	bell('1')  
	
	delay(3)
	before_walk()
	slow_buddho('off',10,'1000',False)
	bell('1')
	delay(2)
	before_sit()
	
	bell('1')
	fast_buddho('off',15)
	bell('1')
	fast_buddho('off',15)
	
	bell('1')
	delay(15)
	bell('1')
	delay(15)
	
	bell('3')
	return None

def my_sun():
	global proc_name
	sun = ['sun1.gif','sun2.gif','sun3.gif','sun4.gif']
	i = random.randint(0,3)
	command = "export DISPLAY=:0.0; python3 testgif.py -f full -p ../web/images/"+sun[i]
	proc = subprocess.Popen(command, shell=True)
	proc_name = "testgif"
	return proc_name

def my_stars():
	global proc_name
	sun = ['mars.gif','moon.gif','jupiter.gif','titan.gif']
	i = random.randint(0,3)
	command = "export DISPLAY=:0.0; python3 testgif.py -f full -p ../web/images/"+sun[i]
	proc = subprocess.Popen(command, shell=True)
	proc_name = "testgif"
	return proc_name


def the_water():
	speak("water droplet at 2500 fps for visual meditation")
	killPlayer()                
	try:
		command = "cvlc -f --loop --video-on-top ../mp4/water-droplets.mp4"
		proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		press_for_stop('d',proc)
		killPlayer() 
	except:
		speak("sorry can not play video clip")
	return None
	
def the_brain():
	killPlayer()                
	try:
		command = "cvlc -f --loop --video-on-top ../mp4/nerve.mp4"
		proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		press_for_stop('d',proc)
		killPlayer() 
	except:
		speak("sorry can not play video clip")
	return None

def cheer_up(i=4):
	speak("play cheerful video clip")
	killPlayer()               
	cheerful  = ['--stop-time 120 ../mp4/timelapse/flowers.mp4','--start-time 8 --stop-time 208 ../mp4/timelapse/cacti.mp4','../mp4/timelapse/nerve.mp4']
	# cheerful += ['--start-time 10 --stop-time 205 ../sound/timelapse/Bug-Eating-Plants.mp4','../sound/timelapse/nerve.mp4']
	if i > 3:
		i = random.randint(0,2)
	else:
		pass              
	try:
		command = "cvlc -f --video-on-top --play-and-exit " + cheerful[i]
		proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		press_for_stop('d',proc)
		killPlayer() 
	except:
		speak("sorry can not play video clip")
	return None


def cheerful_animals():
	animals = ['--gain 0 ../mp4/animals/panda1.mp4']
	try:
		command = "cvlc -f --video-on-top --play-and-exit " + animals[0]
		proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		press_for_stop('d',proc)
		killPlayer() 
	except:
		speak("sorry can not play video clip")
	return None


def music_meditation(t=0,c='d',vol="1000"):
	ledc(c)
	if t == 0:
		proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../sound/youtubeRelaxmusic.mp3"])
		press_for_stop(c,proc)
	else:
		proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../sound/youtubeRelaxmusic.mp3"])
		delay(t)
		proc.kill()
		clear_q()
	return None
	

def monk_rules(c='o'):
	ledc(c)
	play_mp3_loop("../mars/monk/patimok.mp3",'1','2000','1.75')
	play_vlc_file("../mars/monk/nava_dhamma.mp3",'2.00')
	play_vlc_by_list_all("../mars/monk/8",'0.1','1.75',0)
	return None


def morning():
	vol = '1000'
	a = buddha_day()
	if a == 8 or a == 15:
		play_vlc_file("../sound/a-rahung.mp3",'1.00')
		play_vlc_file("../sound/a-sungvech.mp3",'1.00')
	else:
		play_vlc_file("../datath/chanting/patimok-chanting.mp3",'1.00')
		play_mp3_loop("../datath/chanting/sungkharn.mp3",'2','2000','1')
		# play_vlc_file("../sound/dukkha.mp3",'1.00')
		# play_vlc_file("../datath/chanting/sungkharn.mp3",'1.00')
		
	now = datetime.today().strftime('%H %M')
	tn = now.split()
	if int(tn[0]) < 6:
		mn = (6-int(tn[0]))*60 - int(tn[1]) - 11
		i = random.choices([3,2,1],[5,3,1])[0]
		if i == 1 :
			play_mp3_folder('../mars/blessingmp3',vol,mn)
		elif i == 2:
			basic_chanting(mn,vol)
		elif i == 3:
			thai_chanting(mn,vol)
		# buddha_day()
		play_mp3("../sound/namo.mp3",161,vol)
		bell('1',vol)
		remind_walking2(3,vol,7)
		remind_walking2(3,vol,5)
		play_vlc_file("../mars/phraratanatri.mp3",'1.00')
		ledc('off')
		# os.system("sudo shutdown now")
		delay(40)
		adjust_volume()
		play_vlc_file("../sound/theBuddha.m4a",'1.00')
		thai_chanting(30,'2000')
		play_mp3_folder('../mars/blessingmp3','2000',30)
		i = random.randint(1,2)
		if i == 1:
			delay(60)
		else:
			blessed_one(60)
	play_vlc_file("../mars/theBuddha3.m4a",'1.00')
	# play_vlc_file("../sound/theBuddha.m4a",'1.00')
	morning_dhamma()
	return None

def morning_dhamma():
	#test
	global mdm
	a = buddha_day()
	if a == 8:
		play_vlc_file("../mars/monk/nava_vinai.mp3",'2.00')
		b = random.choices([3,2,1],[3,2,1])[0]
		if b == 1:
			play_vlc_by_list_all("../mars/45",'0.1','1.50',1)
		elif b == 2:
			play_vlc_by_list_all("../mars/monks",'0.1','1.50',1)
		else:
			play_vlc_by_list_all("../mars/pyt",'0.1','1.50',1)
	elif a == 15:
		monk_rules()
	else:
		efp = ["../datath/chanting/8-thai.mp3","../datath/chanting/8.mp3","../mars/nava_muk8.mp3"]
		play_vlc_file(random.choice(efp),'1.00')
		nv = ["../mars/monk/nava_dhamma.mp3","../mars/monk/nava_dhamma_chanting.mp3"]
		play_vlc_file(random.choice(nv),'2.00')
		
		if len(mdm) == 0:
			mdm = [1,2,3,4,5,6,7,8,9,10]
		random.shuffle(mdm)
		m = mdm[0]
		mdm.pop(0)
		print(mdm)
		if m == 1:
			my_dhamma()
		elif m == 2:
			speak("4 noble truth")
			vlc_one(0,'../mars/4nt/',"../mars/log/log_morning.txt",0,'0.1','1.50')
			# play_vlc_by_list_all("../mars/4nt",'0.1','1.50',1)
		elif m == 3:
			speak("Paticcasamupbada")
			vlc_one(0,'../mars/12paticca/',"../mars/log/log_morning.txt",0,'0.1','1.50')
			# play_vlc_by_list_all("../mars/12paticca",'0.1','1.50',1)
		elif m == 4:
			speak("Tipitaka")
			vlc_one(0,'../mars/tripitaka/',"../mars/log/log_morning.txt",0,'0.1','1.50')
			# play_vlc_by_list_all("../mars/tripitaka",'0.1','1.50',1)
		elif m == 5:
			speak("Suttanta")
			vlc_one(0,'../mars/suttanta/',"../mars/log/log_morning.txt",0,'0.1','1.50')
			# play_vlc_by_list_all("../mars/suttanta",'0.1','1.50',0)
		elif m == 6:
			speak("Buddha 's gold")
			vlc_one(0,'../mars/gold/',"../mars/log/log_morning.txt",0,'0.1','1.50')
			# play_vlc_by_list_all("../mars/gold",'0.1','1.50',1)
		elif m == 7:
			speak("Noble Dhamma")
			vlc_one(0,'../mars/4nt2/',"../mars/log/log_morning.txt",0,'0.1','1.50')
			# play_vlc_by_list_all("../mars/one",'0.1','1.50',1)
		elif m == 8:
			speak("Human handbook")
			play_vlc_file("../mars/human-handbook.m4a",'1.50')
		elif m == 9:
			speak("Heart wood from bodhi tree")
			vlc_one(0,'../mars/heartwood/',"../mars/log/log_morning.txt",0,'0.1','1.50')
			# play_vlc_by_list_all("../mars/heartwood",'0.1','1.50',0)
		else:
			play_vlc_file("../mars/zen/blood-sutra.mp3",'1.50')
			play_vlc_file("../mars/zen/TaoTeChing.mp3",'1.50')
	return None


def morning_practice(c='off',vol="500"):
	now = datetime.today().strftime('%H %M')
	tn = now.split()
	if int(tn[0]) == 2 and int(tn[1]) > 10:
		mn = 60 - int(tn[1]) - 5
		m = random.randint(1,3)
		if m == 1:
			fast_buddho_hiphop(c,mn,vol)
		elif m == 2:
			play_mp3('../sound/528Hz.mp3',mn*60)
		else:
			wooden_gong_sound(mn)
	else:
		ledc(c)
		bell('1',vol)
		i = random.choices([0,1],[1,100])[0]
		if i == 0:
			walk = [0,1,4,5,9,10,15,16,17]
			i = random.randint(1,3)
			for x in range(i):
				random.shuffle(walk)
			# warm up
			t = random.randint(2,6)
			mixed_mode('off',t,13,vol)
			mixed_mode('off',10-t,14,vol)
			for i in range(1,5):
				mixed_mode('off',t,walk[i],vol)
				mixed_mode('off',10-t,14,vol)
		elif i == 1:
			mixed_mode('off',5,14,vol)
			m = random.choices([1,2,3,4],[4,4,2,1])[0]
			if m == 1:
				play_mp3('../sound/528Hz.mp3',2400)
			elif m == 2:
				wooden_gong_sound(40)
			elif m == 3:
				fast_buddho_hiphop(c,40,vol)
			else:
				play_mp3('../sound/432Hz.mp3',2400)
			mixed_mode('off',5,14,vol)
	#delay(5)
	bell('1',vol)
	fast_buddho(c,5,vol)
	relax_thai(vol)
	#bell('1',vol)
	# start
	ledc('off')
	play_sutra(55)
	# sitting_meditation(1,50,'1000')
	# cool down
	play_mp3('../mars/monk/rbut.mp3',127,'2000')
	morning_merit(vol)
	play_mp3("../sound/metta.mp3",114,vol)
	# dhamma_dhamma()
	mn = x_minutes(5)
	dhamma_wisdom(mn)
	morning()
	return None


def morning_practice3(c='d',mode=1,vol="500"):
	ledc(c)
	bell('1',vol)
	ch = [0,1,1]
	i = random.choice(ch)
	if i == 0:
		walk = [0,1,4,5,9,10,15,16,17]
		i = random.randint(1,3)
		for x in range(i):
			random.shuffle(walk)
		# warm up
		t = random.randint(2,6)
		mixed_mode('off',t,13,vol)
		mixed_mode('off',10-t,14,vol)
		for i in range(1,5):
			mixed_mode('off',t,walk[i],vol)
			mixed_mode('off',10-t,14,vol)
	elif i == 1:
		mixed_mode('off',5,14,vol)
		fast_buddho(c,40,vol)
		mixed_mode('off',5,14,vol)
	#delay(5)
	bell('1',vol)
	fast_buddho(c,5,vol)
	relax_thai(vol)
	#bell('1',vol)
	# start
	ledc('off')
	play_mp3("../sound/namo.mp3",161,vol)
	# play_vlc_all_inTime()
	if mode == 1:
		remind_breathing(1,vol,'th')
		wooden_gong_sound(45)
		bell('1',vol)
		play_mp3_folder('../mars/classical','1000',45)
		bell('1',vol)
		#tibetan_metta_chanting(vol)
	elif mode == 2:
		play_mp3("../sound/528Hz.mp3",2700,'1000')
		play_sutra(45)
		bell('1',vol)
	elif mode == 3:
		play_vlc_all_inTime()
	elif mode == 4:
		play_mp3("../sound/432Hz.mp3",2700,'1000')
		play_sutra(45)
		bell('1',vol)
	elif mode == 5:
		play_mp3_folder('../mars/guqin','1000',45)
		play_sutra(45)
		bell('1',vol)
	elif mode == 6:
		remind_breathing(1,vol,'th')
		play_mp3("../mars/basic_chanting/pahung.mp3",1800,vol)
		blessed_one(30,vol)
		play_sutra(30)
		bell('1',vol)
	elif mode == 7:
		play_vlc_all_inTime("../mars/luangpoorian")
	else:
		bell('1',vol)
		wooden_gong_sound(15)
		bell('1',vol)
		wooden_gong_sound(15)
		bell('1',vol)
		wooden_gong_sound(15)
		bell('1',vol)
		play_sutra(45)
		bell('1',vol)
	
	# cool down
	play_mp3('../mars/monk/rbut.mp3',127,'600')
	morning_merit(vol)
	play_mp3("../sound/metta.mp3",114,vol)

	m = random.randint(1,5)
	if m == 1:
		play_mp3('../sound/528Hz.mp3',1800)
	elif m == 2:
		play_mp3('../sound/432Hz.mp3',1800)
	elif m == 3:
		om_meditation(30)
	elif m == 4:
		play_mp3_folder('../mars/guqin','1000',30)
	elif m == 5:
		bell('1')
		delay(15)
		bell('1')
		delay(15)

	vol = '1000'
	play_mp3("../datath/chanting/8.mp3",1010,vol)
	now = datetime.today().strftime('%H %M')
	tn = now.split()
	mn = (6-int(tn[0]))*60 - int(tn[1]) - 11

	i = random.randint(1,3)
	if i == 1 :
		play_mp3_folder('../mars/blessingmp3',vol,mn)
	elif i == 2:
		basic_chanting(mn,vol)
	elif i == 3:
		thai_chanting(mn,vol)

	play_mp3("../sound/namo.mp3",161,vol)
	remind_walking2(10,vol,0)
	ledc('off')
	os.system("sudo shutdown now")	
	return None

# For Buddha holy day start at 6:00 pm
def evening_practice(d=0,vol="500"):
	# 8 + 2:30 hrs

	remind_sati_bikkhu()

	bell('3',vol)

	six_stages_th_en ('y',10)

	three_stages_th_en('b',10)

	one_stage_th_en('r',10)

	remind_sati()

	one_stage_en(led_color,10)
   
	slow_buddho('c',20)

	remind_right_sati()

	slow_buddho2('gg',15)
	fast_buddho('dd',15)

	fast_buddho('d',15)
	fast_buddho('off',15)

	vol = "300"
	bell('3',vol)
	ledc('off')

	relax_thai(vol)

	if d == 6:
		d = 0
		singing_bowl(360) # 6 hrs

	else:    
		singing_bowl(60)
		bell('3',vol)
		fast_buddho('off',300,vol) # 5 hrs

	bell('3',vol)

	if d == 1 or d == 2 or d == 3 or d == 4:
		if d == 4:
			d = random.randint(1,3)
		morning_practice3('d',d)
	else:
		morning_practice('d')
 
	return None

def my_dhamma():
	play_vlc_file("../datath/chanting/8-thai.mp3",'1.00')
	files  = [["../datath/sutta/moggallana.mp3","1.75","0.1"],["../mars/anapanasati16.mp3","1.75","0.1"],["../mars/bodhipakkhiyadhamma-37.mp3","1.75","0.05"]]
	files += [["../mars/sati.mp3","1.25","0.2"],["../mars/paticca-daily.mp3","1.25","0.1"],["../mars/yoniso.mp3","1.25","0.1"]]
	for f in files:
		try:
			tfx = media_info(f[0])
			rate = f[1]
			gain = f[2]
			tx = tfx / (1000*float(rate))
			# print(tx)
			speak(str(round(tx/60))+" minutes")
			cmd = "cvlc --play-and-exit --global-key-vol-up u --global-key-vol-down d" + " --gain " + gain + " --rate " + rate + " " + f[0]
			proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stdin=master)
			press_for_stop(led_color,proc,tx)
		except:
			speak("file not found")
# def my_dhamma(t=0,vol='3000',c='off'):
	# killPlayer()
	# files =  " ../datath/sutta/moggallana.mp3 ../mars/anapanasati16.mp3 ../mars/bodhipakkhiyadhamma-37.mp3 ../mars/sati.mp3 ../mars/paticcasamuppda.mp3 ../mars/yoniso.mp3"
	# command = "mpg123 -d 2 -q -Z -f " + vol + files
	# proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	# press_for_stop(c,proc,60*t) 


def my_day(vol='500',st=False):
	what_time()
	if st:
		chk = input("Correct ? y/n \n")
		if chk == 'n':
			yyyy = input('YYYY ')
			mm   = input('MM ')
			dd   = input('DD ')
			hh   = input('HH ')
			mm   = input('MM ')
			set_dt = '"' + yyyy + '-' + mm + '-' + dd + ' ' + hh + ':' + mm + ':00' + '"'
			os.system("sudo date -s " + set_dt)
	now = int(datetime.today().strftime('%H'))
	if 1< now and now < 4:
		if st:
			chk = input("2 a.m - morning practice ? y/n \n")
			if chk == 'y':
				morning_practice()
		else:
			morning_practice()
	elif now == 4:
		if st:
			chk = input("4 a.m - morning ? y/n \n")
			if chk == 'y':
				play_mp3("../sound/metta.mp3",114,vol)
				m = random.randint(1,5)
				print(m)
				if m == 1:
					play_vlc_file2('../mars/zen/blood-sutra.mp3',30,0,'1')
					# play_mp3('../mars/zen/blood-sutra.mp3',1800,'1000','off')
				elif m == 2:
					play_vlc_file2('../mars/zen/TaoTeChing.mp3',30,0,'1')
				elif m == 3:
					play_vlc_file2('../mars/zen/TaoTeChing.mp3',30,30,'1')
				elif m == 4:
					play_vlc_file2('../mars/zen/TaoTeChing.mp3',30,60,'1')
				else:
					play_vlc_file2('../mars/zen/suntzu.mp3',30,0,'1.75')
				morning()
		else:
			play_vlc_file2('../mars/zen/blood-sutra.mp3',30,0,'1')
			morning()
	elif now == 5:
		if st:
			chk = input("5 a.m - morning ? y/n \n")
			if chk == 'y':
				morning()
		else:
			morning()
	elif 6 < now and now < 17:
		if st:
			chk = input("6 a.m - noble dhamma ? y/n \n")
			if chk == 'y':
				play_four_noble_truth_dhamma()
		else:
			dhamma_wisdom()
	elif now > 16:
		if st:
			chk = input("5 p.m - evening practice ? y/n \n")
			if chk == 'y':
				testing_mode7()
		else:
			testing_mode7()
	return None

def wait_for_answer(ans='yes',sec=5):
	# print(q.qsize()) 
	check = False
	words = []
	clear_q()
	ledc('gg')
	timeout = time.time() + sec
	while time.time() < timeout:
		data = q.get()
		if rec.AcceptWaveform(data):
			w = rec.Result()
			z = json.loads(w)
			# print(z["text"])
			words += z["text"].split()
			if ans in words:
				check = True
				# speak(ans)
			print(words)
		else:
			pass
	ledc('off')
	words = []
	clear_q()
	return check


# International Code of Signals
ics  = 'a alfa b bravo c charlie d delta e echo f foxtrot g golf h hotel i india j juliet k kilo l lima m mike n november o oscar p papa '
ics += 'q quebec r romeo s sierra t tango u uniform v victor w whiskey x xray y yankee z zulu'
ics_list = ics.split(' ')
del ics
gc.collect()

# read zenstories file
with open('zenstories.json', 'r') as myfile:
	zdata=myfile.read()

# parse file
d = json.loads(zdata)
m = len(d["zen101"])
n = 0
del zdata
gc.collect()
sequence = [i for i in range(m)]
random.shuffle(sequence)

mdm = [1,2,3,4,5,6,7,8,9,10]
									
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
	'-l', '--list-devices', action='store_true',
	help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
	print(sd.query_devices())
	parser.exit(0)
parser = argparse.ArgumentParser(
	description=__doc__,
	formatter_class=argparse.RawDescriptionHelpFormatter,
	parents=[parser])
parser.add_argument(
	'-m', '--model', type=str, metavar='MODEL_PATH',
	help='Path to the model')
parser.add_argument(
	'-d', '--device', type=int_or_str,
	help='input device (numeric ID or substring)')
parser.add_argument(
	'-r', '--samplerate', type=int, help='sampling rate')
parser.add_argument(
	'-x', '--mode', type=int, help='1=chanting 2=dhamma 3=my_day 4=testing_4')
args = parser.parse_args(remaining)

last_files = []
led_color = 'g'

try:
	if args.model is None:
		args.model = "../model"
	if not os.path.exists(args.model):
		print ("Please download a model for your language from https://alphacephei.com/vosk/models")
		print ("and unpack as 'model' in the current folder.")
		parser.exit(0)
	if args.samplerate is None:
		device_info = sd.query_devices(args.device, 'input')
		# soundfile expects an int, sounddevice provides a float:
		args.samplerate = int(device_info['default_samplerate'])
	if args.mode is None:
		args.mode = 0


	# https://github.com/Motion-Project/motion/
	os.system("sudo service motion stop")

	model = vosk.Model(args.model)

	master, slave = os.openpty()

	with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device, dtype='int16',
							channels=1, callback=callback):
			print('#' * 80)
			print('Press Ctrl+C to stop playing')
			print('#' * 80)

			#TESTER
			
			adjust_volume()
			if args.mode == 0:
				i = random.randint(0,1)
				if i == 1:
					play_vlc_file3("../sound/theBuddha.m4a",'1.00')
				else:
					os.system('espeak -s 130 -a 4 -v "english-us" "Nothing is worth insisting on"')
					os.system('mpg123 -q -f 400 ../voices/hello.mp3')
					time.sleep(1)
					i = random.randint(1,4)
					meditation_goal(i,'600')
				
				buddha_day()
				os.system('mpg123 -q -f 600 ../voices/samesame.mp3')
			else:
				bell('1')
				print(args.mode)

			# new runtime vocabulary
			# new_vocab = runtime_vocabulary()
			# vrun  = '["anat ta '
			# vrun += 'a alfa b bravo c charlie d delta e echo f foxtrot g golf h hotel i india j juliet k kilo l lima m mike n november o oscar p papa '
			# vrun += 'q quebec r romeo s sierra t tango u uniform v victor w whiskey x ray y yankee z zulu '
			# vrun += new_vocab
			# vrun += 'yes no ok coca cola"]'

			vrun  = '["please zen story lord buddha buddhist buddhism what time day play help dhamma meditation english radio start light star list '
			vrun += 'browse chanting mantra say speak stop volume turn on off exit shutdown now thai lyric ip address sutra up down breathing '
			vrun += 'one two three four five six seven eight nine ten zero twelve fifteen twenty thirty forty fifty sixty seventy eighty ninety computer '
			vrun += 'a alfa b bravo c charlie d delta e echo f foxtrot g golf h hotel i india j juliet k kilo l lima m mike n november o oscar p papa '
			vrun += 'q quebec r romeo s sierra t tango u uniform v victor w whiskey x ray y yankee z zulu '
			vrun += 'letter repeat space spelling speaker noble japanese chinese red green blue yellow hello wisdom continuous human book '
			vrun += 'walk walking mode search translate service cancel restart reboot save anat ta sitting music raining thunder jungle tibetan heart brain '
			vrun += 'alpha breathing pure monk rule speech morning evening practice web server sound my math next new causes singing bowl '
			vrun += 'ohm variety basic chinese blessed blessing the sun blooming flower clip quit my display testing water morse code good bye chapter pali '
			vrun += 'korean sixteen seventeen eighteen nineteen plants seed carbon food cell universe your name cheerful silent quiet wooden forest '
			vrun += 'yes no ok coca cola stage fold path nature truth dependent origination webcam loop daily life wise thinking technique"]'
			
			
			rec = vosk.KaldiRecognizer(model, args.samplerate,vrun)

			del vrun
			gc.collect()

			bot    = True
			focus  = False
			zen    = False
			math   = False
			mantra = False
			spell  = False
			save   = False
			yesno  = False
			repeat = False
			sit    = False
			verify = False
			proc_bool   = False
			# mp morning practice , ep evening practice
			cmd = ""
			mp = False
			ep = False
			un = False
			mn = 0
			right_words = []
			add_letter  = ''
			spell_words = ''
			verify_words= ''   
			proc_name = ''
			sc = ""
			t  = 0
			k  = 0
			ch = ['a','b','c','d','e','f','i','j','k','l','q']
			ch_name  = ['fast buddho mantra','breathing in and out mantra in Thai','alpha sound with alpha light']
			ch_name += [' only alpha sound','only alpha light','relax and mindful mantra in Thai','Ohm sound','Meditation Music']
			ch_name += ['Paticca Chanting','Raining sound','Quit']
			# espeak('hi,there! my name is anat ta, please call my name if you want to start','5')
			time.sleep(1)
			with q.mutex:
				q.queue.clear()

			while True:
				data = q.get()
				# print(q.qsize())       
				
				words = []
				with Leds() as leds:

					with Board() as board:
						
						if args.mode == 0:
							pass
						elif args.mode == 1:
							thai_chanting()
							bot = True
							args.mode = 0
						elif args.mode == 2:
							play_dhamma()
							bot = True
							args.mode = 0
						elif args.mode == 3:
							my_day('1000',True)
							bot = True
							args.mode = 0
						elif args.mode == 4:
							print("testing 4")
							umong_testing_4()
							bot = True
							args.mode = 0

						if rec.AcceptWaveform(data):

							w = rec.Result()
							z = json.loads(w)
							# print(z["text"])
							# print(q.qsize()) 
							words += z["text"].split()

							# say "anat ta" to start
							if not bot:
								if z["text"] == "anat ta":
									bot = True
									words = []
									speak("what can i do for you?")
									clear_q()
								elif z["text"] == "computer":
									bot = True
									words = []
									speak("yes no ok coca cola")
									clear_q()
								elif z["text"] == "light on":
									ledc('w')
									board.button.wait_for_press()
								elif z["text"] == "blessing one":
									blessed_one()
								elif z["text"] == "my day":
									my_day('1000')
								elif z["text"] == "please help":
									get_help()
									clear_q()
									words = []
								else:
									words = []
									# answer = input_with_timeout("what's up?",3)
									# if answer == 'c':
									# 	thai_chanting()
									# elif answer == 'd':
									# 	play_dhamma()
									# elif answer == 'm':
									# 	# os.system("sudo service motion stop")
									# 	my_day('1000',True)
									# elif answer == 'b':
									# 	bot = True
								
							
							#Begin
							if not focus and len(words) > 1:

								print(words)

								if "say" in words:
									listToStr = ' '.join(map(str, words))
									listToStr = listToStr.replace("say",'')
									speak("You said, " + listToStr)
									clear_q()

								elif "wise" in words:
									if "two" in words:
										wise_one('gg')
									elif "one" in words:
										wise_one()

								if "morning" in words and "meditation" in words:
									morning_dhamma()
																	
								elif "blessing" in words:
									if "one" in words:
										blessed_one()
									elif "two" in words or "sutra" in words:
										play_sutra(60)
									elif "three" in words:
										play_vlc_by_list_all("../mars/luangpoorian")
									elif "four" in words:
										basic_chanting(0)
									elif "six" in words:
										play_mp3_with_alarm()
									else:
										speak("1 paticca chanting, 2 Sutra, 3 Luang poo riean, 4 basic chanting, 6 play dhamma")
										clear_q()
										
								elif "morse" in words and "code" in words:
									if len(words) > 2:
										lt = words[2]
										if len(lt) == 1:
											try:
												n = ics_list.index(lt) + 1
												espeak('morse code for ' + lt + ' ' + ics_list[n],'5')
												morsecode(lt)
											except:
												pass
									else:
										morsecode('sati sati sati')
								elif "plants" in words:
									i = words.index('plants') + 1
									try:
										if len(words[i]) > 1:
											play_plants(words[i])
										else:
											pass
									except:
										pass

								elif "chapter" in words:
									if "sixteen" in words:
										p = '16'
									elif "seventeen" in words:
										p = '17'
									elif "eighteen" in words:
										p = '18'
									elif "nineteen" in words:
										p = '19'
									else:
										p = ''

									if p == '':
										pass
									else:
										play_tripataka_chapter(p)

								elif "testing" in words:
									if "one" in words:
										speak("testing 1")
										testing_mode1()
									elif "four" in words:
										umong_testing_4()
									# elif "two" in words:
									# 	speak("testing 2")
									# 	testing_mode2()
									# elif "three" in words:
									# 	speak("testing 3")
									# 	testing_mode3()
									# elif "four" in words:
									# 	speak("testing 4")
									# 	my_day()
									# elif "five" in words:
									# 	speak("testing 5")
									# 	testing_mode5()
									# elif "six" in words:
									# 	speak("testing 6")
									# 	testing_mode6()
									elif "seven" in words:
										speak("testing 7")
										testing_mode7()
									elif "nine" in words:
										speak("testing 9")
										testing_mode9()
									elif "ten" in words:
										speak("testing ten")
										testing_10()
										
								elif "anat" in words and "ta" in words or "computer" in words:
									if "stop" in words:
										killPlayer()
										bot = False
										speak("ok, call my name when you need help, bye bye!")
									elif "restart" in words or "reboot" in words:
										speak("reboot the system, please wait")
										os.system("sudo reboot")
										# os.system("sudo systemctl restart myscript.service")
										break
									elif "shutdown" in words:
										shutdown()
										break
									elif "help" in words:
										get_help()

									elif "silent" in words or "quiet" in words or "quit" in words:
										killPlayer()
										if len(proc_name) > 0:
											os.system("pkill -f " + proc_name)
											speak("kill " + proc_name)
											proc_name = ''
										if proc_bool:
											proc.kill()
											proc_bool = False
											speak("kill the process")
										speak("done")
										clear_q()
									else:
										speak("what's up?")

								elif "sound" in words:
									i = int(words.index('sound')) + 1
									
									try:
										r = word2int(words[i])
										if r == 'None':
											h = 0
										else:
											h = int(r)
									except:
										h = 0

									t = h*60
									if t == 0:
										speak("push button to stop")
									else:
										speak(str(t) + " minutes")

									if "raining" in words:
										speak("raining sound meditation")
										bell('3')
										raining_meditation(t)

									elif "thunder" in words:
										speak("thunder storm sound meditation")
										bell('3')
										thunder_meditation(t)

									elif "jungle" in words:
										speak("jungle sound meditation")
										bell('3')
										jungle_meditation(t)

									elif "tibetan" in words:
										speak("Tibetan sound meditation")
										bell('3')
										tibetan_meditation(t)

									elif "ohm" in words:
										speak("Ohm at 417 Herzt sound meditation")
										bell('3')
										om_meditation(t)
									elif "wooden" in words:
										wooden_gong_sound(t)

								elif "human" in words and "book" in words:
									speak("Human handbook")
									play_vlc_file("../mars/human-handbook.m4a",'1.50')

								elif "wooden" in words and "heart" in words:
									speak("wooden heart, heart wood from the bodhi tree")
									play_vlc_by_list_all("../mars/heartwood",'0.1','1.75',0)

								elif "alpha" in words:
									if "sixty" in words:
										t = 60
									elif "ninety" in words:
										t = 90
									elif "thirty" in words:
										t = 30
									else:
										t = 0
									
									if "breathing" in words:
										breathing_alpha_meditation(led_color,t);
									elif "pure" in words:
										pure_alpha() # for martian monk only 
									else:
										alpha_meditation(t,15,'g')

								elif "meditation" in words:
									if "dhamma" in words:
										speak("play all playlist, ok?")
										c = wait_for_answer()
										if c:
											speak("play all playlist")
											dhamma_meditation(0)
										else:
											dhamma_meditation2(0)
									elif "math" in words:
										a = random.randint(1,20)
										b = random.randint(1,20)
										speak("what is "+ str(a) + " plus "+ str(b))
										c = a + b
										sc = ''
										lc = list(str(c))
										for i in lc:
											sc += int2word(int(i))
										focus = True
										math = True
										words = []
									elif "music" in words:
										bell('3')
										music_meditation() 
									elif "time" in words:
										meditation_time()
									elif "four" in words:
										speak("satipathan 4 by phra ajahn vorajak")
										play_vlc_by_list_all("../mars/4/vorajak",'0.1','2.00',0)
									elif "one" in words:
										speak("Do you want to practice 10 minutes walking and 30 minutes sitting?")
										c = wait_for_answer()
										if c:
											meditation_1()
									# elif "two" in words:
									# 	speak("2 hours")
									# 	meditation_2()
									# elif "three" in words:
									# 	speak("1 hours")
									# 	meditation_3()
									# elif "four" in words:
									# 	speak("4 hours meditation")
									# 	meditation_4()
									# elif "five" in words:
									# 	speak("1 hour")
									# 	meditation_5()
									# elif "seven" in words:
									# 	speak("1 hour")
									# 	meditation_7()
									# elif "six" in words:
									# 	speak("4 hours with cheerful clip")
									# 	meditation_6()
										
								elif "chinese" in words and "chanting" in words:
									chinese_chanting(0)

								elif "walking" in words and "japanese" in words:
									three_stages_th_en('off',10,'ja')
									counting_walk(10,False,'ja','2000')
									counting_walk(10,True,'ja','2000')

								elif "walking" in words and "chinese" in words:
									three_stages_th_en('off',10,'zh')
									counting_walk(10,False,'zh','2000')
									counting_walk(10,True,'zh','2000')

								elif "walking" in words and "korean" in words:
									three_stages_th_en('off',10,'ko')
									counting_walk(10,False,'ko','2000')
									counting_walk(10,True,'ko','2000')

								elif "walking" in words and "thai" in words:
									meditation_goal(1)
									three_stages_th_en('off',10,'th')
									counting_walk(5,False,'th','2000')
									bell('1')
									counting_walk(5,True,'th','2000')
									walking_meditation_count()
									
								elif "walking" in words and "english" in words:
									three_stages_th_en('off',10,'en')
									counting_walk(5,False,'en','2000')
									bell('1')
									counting_walk(5,True,'en','2000')
									walking_meditation_count()

								elif "practice" in words:

									if "walking" in words:
										if "one" in words:
											# walking_reward()
											walking_meditation_count()
										elif "two" in words:
											testing_mode1()
										else:
											speak("please speak walking practice one for counting or two for one hour by ten minutes each ramdom walking styles")
											clear_q()

									elif "sitting" in words:

										if "one" in words:
											t = 60
										elif "two" in words:
											t = 120
										else:
											t = 30

										speak("sitting meditation practice for " + str(t) + " minutes")
										speak("which practice mode you like?")

										for i in range(len(ch)):
											speak(ch[i] + ", " + ch_name[i])
											time.sleep(1)

										sit   = True
										focus = True
									# for martian monk only     
									elif "morning" in words and "practice" in words:
										morning_practice()
										

									elif "evening" in words and "practice" in words:
										testing_mode7()
										

								# for martian monk only 
								elif "monk" in words and "rule" in words:
									monk_rules()   
                    

								elif "spelling" in words and "mode" in words:
									speak("spelling mode, please use international code of signals such as, c charlie but can say letter c too")
									spell = True
									focus = True
									yesno = False
									save  = False
									spell_words = ''

								elif "what" in words:
									if "time" in words:
										what_time()
									elif "day" in words:
										what_day()
									elif "your" in words and "name" in words:
										speak("My name is Anat ta but you can call me computer too")

								elif "buddha" in words and "day" in words:
									buddha_day()

								elif "buddha" in words and "monk" in words:
									speak("The Great Monks")
									play_vlc_by_list_all('../mars/monks')
									
								elif "zen" in words and "story" in words:
									nn = sequence[n]
									speak("Do you want to listen to this zen story?")
									speak(d["zen101"][nn]["title"])
									focus = True
									zen = True

								elif "singing" in words and "bowl" in words:
									speak("singing bowl")
									m = random.randint(1,2)
									if m == 1:
										play_mp3("../sound/432Hz.mp3",0,'2000','oo')
									else:
										play_mp3("../sound/528Hz.mp3",0,'2000','oo')

								elif "buddha" in words and "one" in words:
									speak("Buddha History")
									play_vlc_by_list_all("../mars/one")

								elif "buddha" in words and "two" in words:
									speak("45 years of Buddha")
									play_vlc_by_list_all('../mars/45')

								elif "buddha" in words and "three" in words:
									speak("45 years of Buddha by Pope")
									play_vlc_by_list_all('../mars/45pope')

								elif "buddha" in words and "four" in words:
									speak("Buddha said by Buddhadasa")
									play_vlc_by_list_all('../mars/gold')

								elif "four" in words and "truth" in words:
									speak("4 noble truth")
									play_vlc_by_list_all("../mars/4nt")

								elif "twelve" in words and "causes" in words:
									speak("Dependent Origination")
									play_vlc_by_list_all("../mars/12paticca")

								elif "forest" in words and "monk" in words:
									speak("muttothai and forest life")
									play_vlc_file("../mars/muttothai.m4a")
									play_vlc_by_list_all("../mars/mun")

								elif "new" in words and "monk" in words:
									speak("Dhamma for new monk by Payutto")
									play_vlc_by_list_all("../mars/pyt")

								elif "dependent" in words and "origination" in words:
									if "daily" in words:
										play_daily_dependent_origination_thai()
									elif "chanting" in words:
										play_dependent_origination_chanting_thai()
									elif "clip" in words:
										play_dependent_origination_clip()

								elif "buddha" in words and "thinking" in words:
									play_buddha_thinking_thai()                                 

								elif "fold" in words and "path" in words:
									if "thai" in words:
										play_eight_fold_path_chanting_thai()
									elif "english" in words:
										play_eight_fold_path_chanting_english()
									elif "clip" in words:
										speak("play 8 fold path with lyrics")
										play_8_fold_path_clip()

								elif "nature" in words and "truth" in words:
										play_nature_truth_chanting_thai() 

								elif "chanting" in words:

									if "english" in words:
										english_chating()

									elif "thai" in words:
										thai_chanting()

									elif "sutra" in words:
										basic_chanting2(0)

									elif "breathing" in words:
										play_breathing_chanting_thai()

									elif "pali" in words:
										pali_chanting()
										
									elif "basic" in words:
										basic_chanting(0)
										
									elif "heart" in words:

										if "clip" in words:
											speak("play heart sutra with lyrics")
											killPlayer()                
											try:
												command = "export DISPLAY=:0.0; vlc -f --loop --video-on-top ../dataen/chanting/heart-sutra.mp4"
												proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
												press_for_stop('d',proc)
												killPlayer() 
											except:
												speak("sorry can not play video clip")
										else:
											heart_sutra(0)
									else:
										speak("Do you want to play sutta chanting ?")
										c = wait_for_answer()
										if c:
											basic_chanting2(0)
										# speak("Do you want to play Thai Chanting ?")
										# cmd = "thai_chanting"
										# focus = True
										# verify = True

								elif "play" in words and "list" in words:
									play_my_playlist()

								elif "radio" in words:
									if "play" in words or "start" in words:
										play_radio()
									elif "thai" in words:
										play_radio_mp3()
									elif "english" in words:
										play_youtube()
									else:
										speak("Do you want to play online radio ?")
										c = wait_for_answer()
										if c:
											play_radio()
										# cmd = "radio"
										# verify = True
										# focus  = True
																		
								elif "sutra" in words and "play" in words:
									play_sutra2()
									                            
									
								elif "mantra" in words:

									killPlayer() 
									mantra = True  
									focus = True                                  
									  
									if "five" in words:
										t = 5
										speak("Do you want to play slow buddho mantra and push button to stop?")
																			   
									elif "one" in words:  
										t = 1
										speak("Do you want to play one hour buddho mantra?")
									
									elif "two" in words: 
										t = 2
										speak("Do you want to play  mixed mode 1 hour?")                                        

									elif "three" in words:  
										t = 3
										speak("Do you want to play 4 hours mantra and 4 hours alpha sound?")

									elif "four" in words:  
										t = 4
										speak("Do you want to play 4 hours buddho mantra then shutdown?")

									elif "six" in words:  
										t = 6
										speak("Do you want to play mixed mode 4 hours mantra then shutdown?")

									elif "play" in words:
										t = 8
										speak("Do you want to play fast buddho mantra push button to stop?")

									elif "ten" in words:
										t = 10 
										speak("Do you want to play " + str(t) + " minutes buddho mantra?")
									elif "fiftheen" in words:
										t = 15
										speak("Do you want to play " + str(t) + " minutes buddho mantra?")
									elif "twenty" in words:
										t = 20
										speak("Do you want to play " + str(t) + " minutes buddho mantra?")
									elif "thirty" in words:
										t = 30
										speak("Do you want to play " + str(t) + " minutes buddho mantra?")
									elif "forty" in words:
										t = 40
										speak("Do you want to play " + str(t) + " minutes buddho mantra?")
									elif "fifty" in words:
										t = 50
										speak("Do you want to play " + str(t) + " minutes buddho mantra?")
									else:
										t = 0
										mantra = False
										focus = False                             

								elif "stage" in words:

									if "one" in words:

										killPlayer()

										if "five" in words:
											t = 5
										elif "ten" in words:
											t = 10 
										elif "fiftheen" in words:
											t = 15
										elif "twenty" in words:
											t = 20
										else:
											t = 30

										speak(str(t) + " minutes 1 stage walking practice")

										if "english" in words:
											one_stage_en(led_color,t)
										else:
											one_stage_th_en(led_color,t)

									elif "three" in words:
										three_stages_th_en(led_color)

									elif "six" in words:
										six_stages_th_en(led_color)                    
								   
								elif "dhamma" in words:
									if "buddha" in words:
										speak("i will play in order, ok?")
										c = wait_for_answer()
										if c:
											speak("play in order")
											buddha_dhamma(0)
										else:
											buddha_dhamma()
									elif "english" in words:
										dhamma_two()
									elif "my" in words:
										my_dhamma()
									elif "morning" in words:
										morning_dhamma()
									elif "play" in words:
										play_my_dhamma("../datath/dhamma")
										# play_dhamma()
									elif "nine" in words:
										speak("Dhamma 9, Buddhadasa Bikkhu")
										speakThai_mp3(['????????????','?????????','?????????????????????'])
										if "continuous" in words:
											speak("continuous")
											play_vlc_by_list_all("../mars/bdd",'0.1','1.75',1)
										else:
											speak("play 10 dhamma talk")
											play_vlc_by_list("../mars/bdd","dhamma_9",10,0,'0.1','1.75')
										# play_vlc_by_list_all("../mars/bdd")
									elif "one" in words:
										speak("Dhamma 1")
										dhamma_meditation2(0)
										# speak("Do you want to play Buddhadasa Bikkhu years 35 36 ?")
										# c = wait_for_answer('yes')
										# if c:
										# 	play_vlc_by_list_all("../mars/bdd-3536",'0.1','1.50',1)
									elif "two" in words:
										speak("Dhamma 2, Luang poo riean")
										speakThai_mp3(['????????????','?????????','??????????????????'])
										if "continuous" in words:
											speak("continuous")
											play_vlc_by_list_all("../mars/luangpoorian",'0.1','1.50',1)
										else:
											speak("play 4 dhamma talk")
											play_vlc_by_list("../mars/luangpoorian","dhamma_2",4,0)
									elif "three" in words:
										# play_vlc_by_list_all("../mars/char",'0.1','1.50',1)
										speak("Dhamma 3, Luang poo char")
										speakThai_mp3(['????????????','?????????','??????'])
										speak("play 4 dhamma talk")
										play_vlc_by_list("../mars/char","dhamma_3",4,0)
									elif "four" in words:
										speak("Dhamma 4, Luang por Payutto")
										speakThai_mp3(['????????????','?????????','??????????????????'])
										if "continuous" in words:
											speak("continuous")
											play_vlc_by_list_all("../mars/payutto")
										else:
											dhamma_one()
										
									elif "five" in words:
										play_vlc_by_list_all("../mars/12paticca")
										
									elif "six" in words:
										if "continuous" in words:
											speak("continuous")
											play_vlc_by_list_all("../mars/suttanta",'0.1','1.75',1)
										else:
											vlc_one()
											# play_vlc_by_list("../mars/suttanta","dhamma_6",2,0)
									elif "seven" in words:
										speak("Dhamma 7, Luang poo Panya")
										speakThai_mp3(['????????????','?????????','???????????????'])
										dhamma_one(0,'../mars/','panya.json','0.1','1.75',"../mars/log/log_panya.txt")
										# play_vlc_by_list("../mars/panya","dhamma_7",4,0,'0.1','1.75')
									elif "ten" in words:
										i = random.choice([1,0,1,0])
										if i == 0:
											speak("Buddhadasa Bikkhu")
											play_vlc_by_list("../mars/bdd-3536","dhamma_10",4,0,'0.1','1.50')
										else:
											speak("Payutto Bikkhu")
											play_vlc_by_list("../mars/payutto6264","dhamma_10",4,0,'0.1','1.50')
										# speak("Dhamma 10, spoke by Pope")
										# speakThai_mp3(['????????????','?????????','????????????????????????'])
										# speak("play 4 dhamma talk")
										# play_vlc_by_list("../mars/pope","dhamma_10",4,0,'0.1','1.75')
									elif "noble" in words:
										speak("play 4 dhamma talk")
										play_vlc_by_list("../mars/4nt2","dhamma_noble",4,0,'0.1','1.50')
										# play_four_noble_truth_dhamma()
									elif "fifteen" in words:
										play_dhamma2(0)
										# speak("Dhamma 15, Phra Paisan Visalo")
										# play_vlc_by_list("../mars/paisan","dhamma_12",4,0,'0.1','1.50')
									elif "wisdom" in words:
										speak("Dhamma wisdom")
										dhamma_wisdom(240)
									elif "twelve" in words:
										speak("Dhamma 12, Luang por surasak")
										play_vlc_by_list_all("../mars/surasak",'0.1','1.50',1)
										# i = random.choices([0,1],[5,1])[0]
										# if i == 0:
										# 	play_vlc_inTime("../mars/suttanta","12",120)
										# elif i == 1:
										# 	play_vlc_inTime("../mars/gold","12",120)
										# i = random.choices([0,1],[5,1])[0]
										# if i == 0:
										# 	play_vlc_inTime("../mars/one","12",120)
										# 	# dhamma_wisdom(120)
										# elif i == 1:
										# 	play_vlc_inTime("../mars/buddhaDhamma","12",120)
										# thai_chanting()
																			  
								#PLAY
								elif "light" in words and "on" in words:

									if "red" in words:
										c = 'r'
									
									elif "green" in words:
										c = 'g'
									
									elif "blue" in words:
										c = 'b'
									
									elif "yellow" in words:
										c = 'y'

									else:
										c = ''

									if "alpha" in words:
										if len(c) == 1:
										   c += c

									# may say : color sound alpha light on
									if "sound" in words:
										ledc(c)
										proc = subprocess.Popen(["mpg123","-q","--loop","-1","../dataen/alpha12Hz.mp3"])
										proc_bool = True
									else:
										ledc(c)                                        

									board.button.wait_for_press()
									if proc_bool:
										proc.kill()
										proc_bool = False

								# https://www.raspberrypi.org/documentation/remote-access/web-server/nginx.md        
								elif "web" in words and "server" in words:
									ip = get_ip()
									if "start" in words:
										if find_name('nginx'):
											speak("web server already start at ip " + ip)
										else:
											os.system("sudo /etc/init.d/nginx start")
											speak("web server start at ip " + ip)
									if "stop" in words:
										if find_name('nginx'):
											os.system("sudo /etc/init.d/nginx stop")
											speak("stop web server")
										else:
											speak("web server already stop")


								# https://pimylifeup.com/raspberry-pi-webcam-server/ 
								elif "turn" in words and "webcam" in words:
									if "on" in words:
										ip = get_ip()
										speak("Turn on web camera at ip address")
										speak(ip + " port number 8081") 
										os.system("sudo service motion start") 
									elif "off" in words:
										speak("Turn off web camera")
										os.system("sudo service motion stop")
										

								#TEST
								elif "buddha" in words and "story" in words:
									play_buddha_story()

								elif "cheerful" in words and "clip" in words:
									cheer_up()
									cheerful_animals()

								elif "blooming" in words and "flower" in words:
									speak("the blooming flowers time lapse for cheerful meditation")
									killPlayer()  
									cheerful = [['BloomingFlowers.mp4','154'],['flowers-blooming.mp4','192']]
									i = random.randint(0,1)              
									try:
										command = "export DISPLAY=:0.0; vlc -f --loop --stop-time " + cheerful[i][1] + " --video-on-top ../mp4/" + cheerful[i][0]
										proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
										press_for_stop('d',proc)
										killPlayer() 
									except:
										speak("sorry can not play video clip")

								elif "browse" in words:
									if "buddhism" in words:
										speak("open Thai buddhism in wikipedia")
										command = "export DISPLAY=:0.0; chromium-browser --incognito --start-fullscreen --start-maximized https://th.wikipedia.org/wiki/???????????????????????????"
										proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
										press_for_stop(led_color,proc)
										os.system("sudo pkill -f chromium")

									elif "buddhist" in words and "story" in words:
										speak("open youtube for buddhist stories")
										command = "export DISPLAY=:0.0; chromium-browser --incognito --start-fullscreen --start-maximized https://www.youtube.com/watch?v=tI-hgIhFDT0&list=PLYBNr5a72-497Q3UVkpDB24W4NTCD5f2K"
										proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
										press_for_stop(led_color,proc)
										os.system("sudo pkill -f chromium")

									elif "meditation" in words and "technique" in words:
										speak("open youtube for meditation technique")
										command = "export DISPLAY=:0.0; chromium-browser --incognito --start-fullscreen --start-maximized https://www.youtube.com/playlist?list=PLUh8U5np7D-7FMh6ONGwnaltFppPBwTVI"
										proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
										press_for_stop(led_color,proc)
										os.system("sudo pkill -f chromium")
									elif "webcam" in words:
										speak("open webcam on web browser")
										ip = get_ip()
										command = "export DISPLAY=:0.0; chromium-browser --incognito --start-fullscreen --start-maximized " + ip + ":8081"
										proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
										press_for_stop(led_color,proc)
										os.system("sudo pkill -f chromium")

								elif "good" in words and "bye" in words:
									shutdown()
									break
								# aplay -L
								elif "speaker" in words:
									if "up" in words:
										call(["amixer","-q","-M","sset","Master","100%"])
										espeak("set volume to 100%",'10')
									elif "down" in words:
										call(["amixer","-q","-M","sset","Master","50%"])
										espeak("set volume to 60%",'100')
									elif "sixty" in words:
										call(["amixer","-q","-M","sset","Master","60%"])
										espeak("set volume to 60%",'30')
									elif "eighty" in words:
										call(["amixer","-q","-M","sset","Master","80%"])
										espeak("set volume to 80%",'20')

								elif "ip" in words and "address" in words:
									ip = get_ip()
									speak(ip)

								elif len(words) > 0:
									listToStr = ' '.join(map(str, words))
									espeak("words i heard , " + listToStr, '5')
									clear_q()
															   
							else:

								if len(words)>0:

									if verify:
										if "no" in words:
											speak('ok')
											cmd = ""
											mn  = 0
											verify = False
											focus  = False
											clear_q()
										elif "yes" in words:
											if cmd != "":
												if cmd == "radio":
													play_radio()
													cmd = ""
													verify = False
													focus = False
												elif cmd == "sutra":
													play_sutra(30)
													cmd = ""
													verify = False
													focus = False
												elif cmd == "dhamma":
													play_my_dhamma("../datath/dhamma")
													cmd = ""
													verify = False
													focus = False
												elif cmd == "thai_chanting":
													thai_chanting()
													cmd = ""
													verify = False
													focus = False
										else:
											espeak(verify_words,'5')
											espeak("please answer yes or no",'5')
											clear_q()

									elif zen:
										if "no" in words:
											n = n + 1
											if n == m:
												random.shuffle(sequence)
												n = 0
											nn = sequence[n]    
											speak("Do you want to listen to this zen story?")                                     
											speak(d["zen101"][nn]["title"])  
										elif "yes" in words:
											lines = d["zen101"][nn]["story"]
											# print(lines)
											for i in range(len(lines)):
												x = int(lines[i]["voice"])
												engine.setProperty('voice',es_voices[x]) 
												speak(lines[i]["text"])
											zen = False
											focus = False
											engine.setProperty('voice',es_voices[2]) 
											n = n +1 
										else:
											speak("please speak yes or no")
											clear_q()

									elif math:
										
										ans = ''
										for x in words:
											ans += x

										if sc == ans:
											speak("well done")
											a = random.randint(1,20)
											b = random.randint(1,20)
											if a>b:
												speak("what is "+ str(a) + " minus "+ str(b))
												c = a - b
											else:
												speak("what is "+ str(a) + " plus "+ str(b))
												c = a + b
											sc = ''
											lc = list(str(c))
											for i in lc:
												sc += int2word(int(i))
											clear_q()

										elif "stop" in words:
											math = False
											focus = False
											speak("quit math meditation")
											clear_q()
										elif "next" in words:
											speak("the answer is " + sc)
											a = random.randint(1,20)
											b = random.randint(1,20)
											if a>b:
												speak("what is "+ str(a) + " minus "+ str(b))
												c = a - b
											else:
												speak("what is "+ str(a) + " plus "+ str(b))
												c = a + b
											sc = ''
											lc = list(str(c))
											for i in lc:
												sc += int2word(int(i))
											clear_q()                                     

										else:
											speak("i heard "+ ans + " , it's incorrect")
											clear_q()

									elif mantra:

										if "yes" in words:

											if t == 1:
												bell('3','500')
												fast_buddho('y',15)
												fast_buddho('yy',15)
												bell('3','500')
												fast_buddho(led_color,15)
												fast_buddho('gg',15)
												mantra = False
												focus = False

											elif t == 2:
												c = ["r","g","b","y","p","c"]
												n = [0,1,2,3]

												random.shuffle(c)
												random.shuffle(n)

												mixed_mode(c[0],10,n[0])
												mixed_mode(c[1],10,n[1])
												mixed_mode(c[2],10,n[2])
												mixed_mode(c[3],10,n[3])                                       
												
												remind_sati()
												
												slow_buddho(c[4],10)
												fast_buddho(c[5],10)
												mantra = False
												focus = False

											elif t == 3:
												remind_sati_bikkhu()
											
												one_stage_th_en('y',10)

												one_stage_en(led_color,10)

												three_stages_th_en('b',10)
												
												remind_sati()

												slow_buddho2('c',15)
												fast_buddho('gg',15)

												remind_right_sati()

												fast_buddho('off',180)
												
												ledc('off')
												singing_bowl(240)
												mantra = False
												focus = False

											elif t == 4:
												slow_buddho('off',15)
												slow_buddho2('off',15)
																								
												remind_sati()

												slow_buddho2('bb',15)
												fast_buddho('gg',15)

												remind_right_sati()

												fast_buddho('off',180)
												
												os.system("sudo shutdown now")
												break

											elif t == 5:
												slow_buddho('off',0)
												mantra = False
												focus = False

											elif t == 6:
												remind_sati_bikkhu()

												three_stages_th_en('c',10)

												six_stages_th_en('y')

												one_stage_th_en(led_color,15)

												one_stage_en('b',15)

												fast_buddho('p',15)
												
												remind_right_sati()

												slow_buddho('yy',15)

												fast_buddho('off',15)

												remind_sati()

												slow_buddho('gg',15)

												fast_buddho('off',15)

												fast_buddho('off',120)
												
												os.system("sudo shutdown now")
												break

											elif t == 8:
												speak("fast buddho mantra push button to stop")
												bell('3','500')
												fast_buddho('d',0)
												mantra = False
												focus = False

											else :
												speak(str(t) + " minutes buddho mantra")
												bell('3','500')
												fast_buddho(led_color,t)
												mantra = False
												focus = False

										elif "no" in words:
											speak('ok, please repeat your command again')
											mantra = False
											focus = False

										else:
											speak("please speak yes or no")
											clear_q()

									elif spell:

										if len(words) > 1 and not yesno:

											try:
												if len(words[1]) > 1:
													b = ics_list.index(words[1])-1
													add_letter = ics_list[b]
													speak("Do you want to add letter " + add_letter + " " + words[1] + "?")
													yesno = True
												else:
													if len(words[1]) == 1:   
														add_letter = words[1]
														b = ics_list.index(words[1])+1
														speak("Do you want to add letter " + add_letter + " " + ics_list[b] + "?")
														yesno = True
													else:
														pass
											except:
												if words[0] == "letter" and len(words[1]) == 1:
													add_letter = words[1]
													b = ics_list.index(words[1])+1
													speak("Do you want to add letter " + add_letter + " " + ics_list[b] + "?")
													yesno = True
												else:
													if words[1] == "space":
														add_letter = "space"
														speak("Do you want to add letter " + add_letter + "?")
														yesno = True
													else:
														pass

										elif "yes" in words:
											if save:
												#save words for runtime vocabulary
												save_vocabulary(spell_words)
												save = False
											elif add_letter == "space":
												spell_words += ' '
											else:
												spell_words += add_letter

											speak("done, what's next?")
											yesno = False

										elif "repeat" in words:
											spw = list(spell_words)
											for l in spw:
												speak(l)

										elif "speak" in words:
											speak(spell_words)

										elif "no" in words: 
											if save:
												speak("ok, do not save it")
											else:
												speak("please repeat the letter you want again")
											yesno = False

										elif "save" in words:
											speak("Do you really want to save " + spell_words + " to runtime vocabulary?")
											yesno = True
											save = True
											
										elif "search" in words:
											speak("I will google for " + spell_words + "please see the search result on the monitor and push button to quit")
											command = 'export DISPLAY=:0.0; chromium-browser --incognito --start-fullscreen --start-maximized https://www.google.com/search?q="' + spell_words + '"'
											proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
											press_for_stop(led_color,proc)
											os.system("sudo pkill -f chromium")
											focus = False
											spell = False

										elif "translate" in words:
											speak("please see the translation on the monitor and push button to Quit")
											command = 'export DISPLAY=:0.0; chromium-browser --incognito --start-fullscreen --start-maximized https://www.google.com/search?q="translate ' + spell_words + '"'
											proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
											press_for_stop(led_color,proc)
											os.system("sudo pkill -f chromium")
											focus = False
											spell = False

										elif "exit" == words[0]:
											speak("Quit spelling mode")
											focus = False
											spell = False

										else:
											listToStr = ' '.join(map(str, words))
											espeak("i heard , " + listToStr, '5')
											if yesno:
												espeak("please answer yes or no",'5')
											else:
												espeak("next letter please", '5')
											clear_q()   
									
									elif sit:

										if yesno:
											if "yes" in words:
												speak(str(t) + " minutes " + ch_name[k])
												if ch[k] == 'a':
													bell('3','500')
													fast_buddho('off',t)
													bell('1','500')
													focus = False
													sit = False
												elif ch[k] == 'b':
													bell('3','500')
													remind_breathing(t)
													bell('1','500')
													focus = False
													sit = False
												elif ch[k] == 'c':
													breathing_alpha_meditation('gg',t)
													focus = False
													sit = False
												elif ch[k] == 'd':
													breathing_alpha_meditation('off',t)
													focus = False
													sit = False
												elif ch[k] == 'e':
													bell('3','500')
													ledc('gg')
													delay(t)
													bell('1','500')
													focus = False
													sit = False
												elif ch[k] == 'f':
													remind_relax(t)
													focus = False
													sit = False
												elif ch[k] == 'i':
													bell('3','500')
													om_meditation(t)
													bell('1','500')
													focus = False
													sit = False
												elif ch[k] == 'j':
													bell('3','500')
													music_meditation(t)
													bell('1','500')
													focus = False
													sit = False
												elif ch[k] == 'k':
													bell('3','500')
													blessed_one(t)
													bell('1','500')
													focus = False
													sit = False
												elif ch[k] == 'l':
													bell('3','500')
													raining_meditation(t)
													bell('1','500')
													focus = False
													sit = False
											elif "no" in words:
												yesno = False
												speak("please select new choice ")
												speak(ch)
												clear_q()
											else:
												listToStr = ' '.join(map(str, words))
												espeak("i heard , " + listToStr, '5')
												espeak("please answer yes or no",'5')
												clear_q()                                                
											
										elif len(words[0]) == 1:

											if words[0] == 'q':
												speak("Quit sitting practice")
												focus = False
												sit = False
											else:
												try:
													k = ch.index(words[0])
													speak("Do you want to play " + ch_name[k] + "?")
													yesno = True
													
												except:
													listToStr = ' '.join(map(str, words))
													espeak("i heard , " + listToStr, '5')
													speak("please select")
													speak(ch)
													yesno = False
													clear_q()
												

						else:
							qs = q.qsize()
							if bot:
								if qs > qlimit:
									leds.update(Leds.rgb_on(Color.RED))
									qf += 1
									if qf > qlimit:
										qf = 0
										clear_q()
								elif qs > qlimit/2:
									leds.update(Leds.rgb_on(Color.YELLOW))
								else:
									leds.update(Leds.rgb_on(Color.GREEN))
							else:
								leds.update(Leds.rgb_on(Color.BLACK))
								qf += 1
								if qf > qlimit:
									qf = 0
									clear_q()
								# x = rec.PartialResult()
								# print(x)

except KeyboardInterrupt as ki:
	print("Caught:", repr(ki))
	print('\nDone')
	parser.exit(0)
except Exception as e:
	parser.exit(type(e).__name__ + ': ' + str(e))


# For Martian Monk Bhavana practice
# twitter @MartianZenMonk
