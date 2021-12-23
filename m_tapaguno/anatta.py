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
		engine.say(text)
		engine.runAndWait()
		engine.stop()
		return None


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
				'á': ".--.-", 'é': "..-.."}


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
				{"voice":"2","text":"But if by doing this you don't shake off your drowsiness, then — percipient of what lies in front & behind — set a distance to meditate walking back & forth, your senses inwardly immersed, your mind not straying outwards. It's possible that by doing this you will shake off your drowsiness."},
				{"voice":"2","text":"But if by doing this you don't shake off your drowsiness, then — reclining on your right side — take up the lion's posture, one foot placed on top of the other, mindful, alert, with your mind set on getting up. As soon as you wake up, get up quickly, with the thought, 'I won't stay indulging in the pleasure of lying down, the pleasure of reclining, the pleasure of drowsiness.' That is how you should train yourself."},
				{"voice":"2","text":"Furthermore, Moggallana, should you train yourself: 'I will not visit families with my pride lifted high.' That is how you should train yourself. Among families there are many jobs that have to be done, so that people don't pay attention to a visiting monk. If a monk visits them with his trunk lifted high, the thought will occur to him, 'Now who, I wonder, has caused a split between me and this family? The people seem to have no liking for me.' Getting nothing, he becomes abashed. Abashed, he becomes restless. Restless, he becomes unrestrained. Unrestrained, his mind is far from concentration."},
				{"voice":"2","text":"Furthermore, Moggallana, should you train yourself: 'I will speak no confrontational speech.' That is how you should train yourself. When there is confrontational speech, a lot of discussion can be expected. When there is a lot of discussion, there is restlessness. One who is restless becomes unrestrained. Unrestrained, his mind is far from concentration."},
				{"voice":"2","text":"It's not the case, Moggallana, that I praise association of every sort. But it's not the case that I dispraise association of every sort. I don't praise association with householders and renunciates. But as for dwelling places that are free from noise, free from sound, their atmosphere devoid of people, appropriately secluded for resting undisturbed by human beings: I praise association with dwelling places of this sort."},
				{"voice":"1","text":"When this was said, Ven. Moggallana said to the Blessed One"},
				{"voice":"3","text":"Briefly, lord, in what respect is a monk released through the ending of craving, utterly complete, utterly free from bonds, a follower of the utterly holy life, utterly consummate: foremost among human & heavenly beings?"},
				{"voice":"2","text":"There is the case, Moggallana, where a monk has heard, 'All phenomena are unworthy of attachment.' Having heard that all phenomena are unworthy of attachment, he fully knows all things. Fully knowing all things, he fully comprehends all things. Fully comprehending all things, then whatever feeling he experiences — pleasure, pain, neither pleasure nor pain — he remains focused on inconstancy, focused on dispassion, focused on cessation, focused on relinquishing with regard to that feeling. As he remains focused on inconstancy, focused on dispassion, focused on cessation, focused on relinquishing with regard to that feeling, he is unsustained by anything in the world. Unsustained, he is not agitated. Unagitated, he is unbound right within. He discerns: 'Birth is ended, the holy life fulfilled, the task done. There is nothing further for this world"},
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
	os.system("mpg123 --loop " + str(dur) + ' -f 6000 ' + freq)

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
			pass
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

def int_or_str(text):
	"""Helper function for argument parsing."""
	try:
		return int(text)
	except ValueError:
		return text

def callback(indata, frames, time, status):
	"""This is called (from a separate thread) for each audio block."""
	if status:
		print(status, file=sys.stderr)
	if q.qsize() > 15:
		with q.mutex:
			q.queue.clear()
	else:
		q.put(bytes(indata)) 


def clear_q():
	time.sleep(1)
	with q.mutex:
		q.queue.clear()

# see leds_example.py

def ledc(c='', f='alpha'):
	pass

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


def delay(t):
	time.sleep(60*t)
	return None


def press_for_stop(c='',proc=0,t=0):
	if t == 0:
		motion_detect(proc)
	else:
		time.sleep(t)
	proc.kill()
	pkill_proc_name()
	killPlayer()
	with q.mutex:
		q.queue.clear()
	return None


def get_help():
	text =  '''
			Thai Chanting 
            Play Dhamma 
            Play Sutra 
            Meditation One
            Thai Walking 
            Sitting Practice
			'''
	speak(text)
	time.sleep(3)
	with q.mutex:
		q.queue.clear()
	return None


def shutdown():
	os.system("mpg123 -f 6000 ../voices/dead.mp3")
	espeak("The system is shutting down, wait until the green light in the box turn off, bye bye",'10')
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
def motion_detect(proc):
	bk = False
	# Assigning our static_back to None
	static_back = None
	# List when any moving object appear
	motion_list = [ None, None ]
	video = cv2.VideoCapture(0)
	while True:
		# Reading frame(image) from video
		check, frame = video.read()
		# if frame is None: 
	 #    print("empty frame")
	 #    exit(1)

		# Initializing motion = 0(no motion)
		motion = 0

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
		cnts,_ = cv2.findContours(thresh_frame.copy(),
						cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		for contour in cnts:
			if cv2.contourArea(contour) < 60000:
				continue
			motion = 1

			(x, y, w, h) = cv2.boundingRect(contour)
			print(str(w*h))
			# making green rectangle arround the moving object
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
			if w*h > 300000:
				bk = True

		# Appending status of motion
		motion_list.append(motion)

		if bk:
			break

		#cv2.imshow("Gray Frame", gray)
		#cv2.imshow("Difference Frame", diff_frame)
		#cv2.imshow("Threshold Frame", thresh_frame)
		# cv2.imshow("Color Frame",frame)
		# key = cv2.waitKey(1)
		# if q entered whole process will stop
		# if key == ord('q'):
		#     break

	proc.kill()
	video.release()
	# Destroying all the windows
	# cv2.destroyAllWindows()
		
	return None


def speakThai(text):
	stext = ""
	for i in range(len(text)):
		stext += " ../voices/th/" + text[i] + ".mp3"
	os.system('mpg123 -d 2 -f 6000 ' + stext)


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
	writer.writerow(thislist)


def buddha_day():
	today = dt.datetime.now()
	year  = today.strftime("%Y")
	with open('../csv/'+ year + '.csv', newline='') as f:
		reader = csv.reader(f)
		data = list(reader)

	day = datetime.today().strftime('%Y%m%d')
	holyday = []
	thholyday = []

	for i in range(len(data)):
		if i > 0:
			if(int(data[i][1]) > int(day)):
				holyday.append(data[i][1])
				thholyday.append(data[i][0])
	t = thholyday[0].replace("(", " ")
	x = t.split()
	
	bdaytext = ""
	for i in range(len(x)-1):
	  bdaytext += " ../voices/th/" + x[i] + ".mp3"

	if have_internet():
		today = dt.datetime.now()
		z = today.strftime("%B %A %d %H %M")
		speak("Today is" + z)
		t = "วันนี้,วัน,weekday/%w,ที่,59/%d,เดือน,month/%m,เวลา,59/%H,นาฬิกา,59/%M,นาที"
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
	t = "วันพระ,หน้า,คือ,วัน,weekday/%w,ที่,59/%d,เดือน,month/%m"
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
	return None


def fast_buddho(c='off', t=30, vol='6000'):

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


def bell(l='3',vol='6000'):
	subprocess.run(["mpg123","-q","-f",vol,"--loop",l,"../sound/bell.mp3"])
	return None


def relax_thai(vol="6000"):

	text  = ["ทำ","ตัว","ผ่อน","คลาย","หาย","ใจ","ยาว","ยาว","คลาย","ความ","กังวล","ตั้ง","จิต","มั่น","รู้","ลม","หาย","ใจ"]
	text += ["เข้า","ออก","สั้น","ยาว","หยาบ","ละเอียด","เกิด","ดับ","ไม่","เที่ยง","หนอ","แล"]
	text += ["ไม่","มี","ทุกข์","ไม่","มี","สุข","มี","แต่","ความ","ที่","สติ","เป็น","ธรรมชาติ","บริสุทธิ์","เพราะ","อุเบกขา","แล้ว","แล","อยู่"]
	stext = thwords(text)
	# print(stext)
	os.system("mpg123 -q -f " + vol + " " + stext)
	del stext
	gc.collect()
	return None


def relax_walk(t=5,vol='6000'):
	call(["amixer","-q","-M","sset","Master","80%"])
	text  = ["พุท","โธ","พุท","โธ","เหยียบ","เหยียบ","รู้","ลม","หาย","ใจ","รู้","กาย","เคลื่อน","ไหว","รู้","ใจ","นึก","คิด","มี","จิต","เบิก","บาน"]
	text += ["พุท","โธ","พุท","โธ","เหยียบ","เหยียบ","ถอน","ความ","พอ","ใจ","และ","ความ","ไม่","พอ","ใจ","ใน","ใจ","ออก","เสีย","ได้"]
	text += ["พุท","โธ","พุท","โธ","เหยียบ","เหยียบ","จิต","เบิก","บาน","หาย","ใจ","เข้า","จิต","โล่ง","เบา","หาย","ใจ","ออก"]
	text += ["พุท","โธ","พุท","โธ","เหยียบ","เหยียบ","รู้","ลม","ยาว","รู้","ลม","สั้น","รู้","กาย","ทั้ง","ปวง","ทำ","กาย","ลม","ให้","ประ","ณีต"]
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
	call(["amixer","-q","-M","sset","Master","100%"])
	return None


def anapanasati_walk(ts=5):
	call(["amixer","-q","-M","sset","Master","80%"])
	t  = 'พุท โธ พุท โธ เหยียบ เหยียบ รู้ ลม ยาว รู้ ลม สั้น รู้ กาย ทั้ง ปวง ทํา กาย ลม ให้ ประ ณีต '
	t += 'พุท โธ พุท โธ เหยียบ เหยียบ รู้ ปี ติ รู้ สุข รู้ เว ทะ นา ทํา เว ทะ นา ให้ ระ งับ '
	t += 'พุท โธ พุท โธ เหยียบ เหยียบ รู้ พร้อม ซึ่ง จิต ทํา ให้ จิต บัน เทิง ทํา จิต ให้ ตั้ง มั่น ทํา จิต ให้ ปล่อย ' 
	t += 'พุท โธ พุท โธ เหยียบ เหยียบ ตาม เห็น ความ ไม่ เที่ยง ตาม เห็น ความ คลาย กํา หนัด ตาม เห็น ความ ดับ ไม่ เหลือ ตาม เห็น ความ สลัด คืน'
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
			os.system("aplay -q " + tx_list[i] + ".wav")
		time.sleep(0.25)
		if i < n:
			i += 1
		else:
			i = 1
	os.system("aplay -q " + tx_list[i] + ".wav")
	time.sleep(1)
	del t
	del text
	del tx
	del tx_list
	gc.collect()
	clear_q()
	call(["amixer","-q","-M","sset","Master","100%"])
	return None


def musk_walk(ts=5):
	call(["amixer","-q","-M","sset","Master","80%"])
	t  = 'พุท โธ พุท โธ เหยียบ เหยียบ ความ เห็น ชอบ สัม มา ทิฏ ฏิ ความ รู้ ใน ทุกข์ ความ รู้ ใน เหตุ ให้ เกิด ทุกข์ ความ รู้ ใน ความ ดับ แห่ง ทุกข์ ความ รู้ ใน ทาง ดำ เนิน ให้ ถึง ความ ดับ แห่ง ทุกข์ '
	t += 'พุท โธ พุท โธ เหยียบ เหยียบ ความ ดำริ ชอบ สัม มา สัง กัป โป ดำริ ใน การ ออก จาก กาม ดำริ ใน การ ไม่ มุ่ง ร้าย ดำริ ใน การ ไม่ เบียด เบียน '
	t += 'พุท โธ พุท โธ เหยียบ เหยียบ การ พูด จา ชอบ สัม มา วา จา เว้น จาก การ พูด ไม่ จริง เว้น จาก การ พูด ส่อ เสียด เว้น จาก การ พูด หยาบ เว้น จาก การ พูด เพ้อ เจ้อ '
	t += 'พุท โธ พุท โธ เหยียบ เหยียบ การ ทำ การ งาน ชอบ สัม มา กัม มัน โต เว้น จาก การ ฆ่า เว้น จาก การ ถือ เอา สิ่ง ของ ที่ เจ้า ของ ไม่ ได้ ให้ เว้น จาก การ ประพฤติ ผิด ใน กาม '
	t += 'พุท โธ พุท โธ เหยียบ เหยียบ การ เลี้ยง ชี วิต ชอบ สัม มา อา ชี โว ไม่ ทำ อา ชีพ ทุ จริต ทำ อา ชีพ สุ จริต '
	t += 'พุท โธ พุท โธ เหยียบ เหยียบ ความ เพียร ชอบ สัม มา วา ยา โม ไม่ ทำ ชั่ว ใหม่ เลิก ทำ ชั่ว ที่ ยัง ทำ อยู่ ทำ ความ ดี เพิ่ม รัก ษา ความ ดี ที่ ทำ ไว้ '
	t += 'พุท โธ พุท โธ เหยียบ เหยียบ ความ ระ ลึก ชอบ สัม มา สติ มี สติ ใน กาย มี สติ ใน เว ทะ นา มี สติ ใน จิต มี สติ ใน ธรรม มี ความ เพียร เผา กิเลส มี ความ รู้ สึก ตัว มี สติ ถอน ความ พอ ใจ และ ความ ไม่ พอ ใจ ใน ใจ ออก เสีย ได้ '
	t += 'พุท โธ พุท โธ เหยียบ เหยียบ ความ ตั้ง ใจ มั่น ชอบ สัม มา สมา ธิ เข้า ถึง ปฐม ฌาน มี วิตก วิจาร ปีติ สุข เอกัคคตา เข้า ถึง ทุติย ฌาน ไม่ มี วิตก วิจาร มี แต่ ปีติ สุข เอกัคคตา '
	t += 'เข้า ถึง ตติย ฌาน ไม่ มี ปีติ มี ความ สุข ด้วย นามกาย เป็น ผู้ อยู่ อุ เบก ขา มี สติ อยู่ เป็น ปกติ สุข เข้า ถึง จตุตถ ฌาน ไม่ มี ทุกข์ ไม่ มี สุข มี แต่ ความ ที่ สติ เป็น ธรรมชาติ บริสุทธ์ เพราะ อุ เบก ขา แล้ว แล อยู่'

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
	call(["amixer","-q","-M","sset","Master","100%"])
	return None

def cheerful_mantra_th1(c='off', t=30, vol='6000'):

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
	# speak("pure alpha sound, push button for stop")
	os.system("mpg123 -f 6000 ../voices/right_concentation.mp3")
	# proc = subprocess.Popen(["mpg123","-q","--loop","-1","../datath/basic_chanting/pureAlpha1hr.mp3"])
	proc = subprocess.Popen(["mpg123","-q","--loop","-1","../sound/OM417Hz.mp3"])
	press_for_stop(c,proc)
	return None

def alpha_wave(t,vol='6000'):
	# proc = subprocess.Popen(["mpg123","-q","-f",vol,"--loop","-1","../sound/pureAlpha2.mp3"])
	proc = subprocess.Popen(["mpg123","-q","--loop","-1","../sound/OM417Hz.mp3"])
	delay(t)
	proc.kill()
	clear_q()
	return None
	
	
def mars_wind(t):
	proc = subprocess.Popen(["mpg123","-q","--loop","-1","../sound/wind-on-mars.mp3"])
	# proc = subprocess.Popen(["mpg123","-q","-f","6000","--loop","-1","../sound/wind-on-mars.mp3"])
	delay(t)
	proc.kill()
	clear_q()
	return None

def ligo_sound(t):
	proc = subprocess.Popen(["mpg123","-q","-f","6000","--loop","-1","../sound/ligo1.mp3"])
	delay(t)
	proc.kill()
	clear_q()
	return None

#BHAVANA
def remind_breathing(t=30,vol='6000',l='th',ts=0):
	bell('1',vol)
	if l == 'zh':
		text = ['欢快地吸气','呼气并感到放松']
		tx   = zhwords(text)
	elif l == 'ja':
		text = ['陽気な心_吸い込む','安心した_息を吐き']
		tx   = jawords(text)
	elif l == 'en':
		text = ['cheerful_breathing_in','relieved_breathing_out']
		tx   = engwords(text)
	elif l == 'th1':
		text = ["พุท05","โธ05","พุท05","โธ05","หาย","ใจ","เข้า","พุท05","หาย","ใจ","ออก","โธ05"]
		tx   = thaiwords(text)
	elif l == 'th2':
		text = ["หาย","ใจ","เข้า05","หาย","ใจ","ออก05","พุท05","โธ05"]
		tx   = thaiwords(text)
	elif l == 'th3':
		text = ["หาย","ใจ","เข้า05","หาย","ใจ","ออก05"]
		tx   = thaiwords(text)
	elif l == 'th4':
		text = ["พุท05","โธ05"]
		tx   = thaiwords(text)
	elif l == 'th5':
		text = ['ไม่กังวล','อะไร','ไม่ต้องการ','สิ่งใด','สุขหนอ','สุขหนอ']
		tx   = thaiwords(text)
	else:
		text = ["จิต","เบิก","บาน","หาย","ใจ","เข้า","จิต","โล่ง","เบา","หาย","ใจ","ออก"]
		tx   = thwords(text)

	timeout = time.time() + 60*t   
	while True:
		if time.time() > timeout:
			break
		else:
			# os.system("mpg123 -q " + tx)
			os.system("mpg123 -q -f "+ vol + " " + tx)
			time.sleep(ts)
	bell('1',vol)
	clear_q()
	return None
 
 
def remind_breathing2(t=30,vol='6000'):
	#bell('3',vol)
	text  = ["มี","สติ","รู้","ลม","หาย","ใจ","อยู่","หนอ"]
	tx   = thaiwords(text)
	timeout = time.time() + 60*t   
	while True:
		if time.time() > timeout:
			break
		else:
			# os.system("mpg123 -q " + tx)
			os.system("mpg123 -f "+ vol + " " + tx)
	bell('1',vol)
	clear_q()
	return None


def remind_b4walking(vol='6000',lg=''):
	bell('1',vol)
	if lg == 'th':
		text  = ["รู้","เท้า","เคลื่อน","ไหว","รู้","ใจ","นึก","คิด","มี","จิต","เบิก","บาน","อยู่","กับ","ปัจ","จุ","บัน"]
		tx   = thaiwords(text)
		# os.system("mpg123 " + tx)
		os.system("mpg123 -f "+ vol + " " + tx)
	else:
		speak("mind your step")
	bell('1',vol)
	clear_q()
	return None


def remind_walking(t=30,vol='6000',n=0):
	#bell('3',vol)
	if n == 1:
		text = ['ไม่กังวล','อะไร','ไม่ต้องการ','สิ่งใด','สุขหนอ','สุขหนอ']
		tx   = thaiwords(text)
	elif n == 2:
		text = ["มี","สติ","รู้","เท้า","เคลื่น","ไหว"]
		tx   = thaiwords(text)
	else:
		text  = ["รู้","เท้า","เคลื่อน","ไหว","รู้","ใจ","นึก","คิด","มี","จิต","เบิก","บาน","อยู่","กับ","ปัจ","จุ","บัน"]
		tx   = thaiwords(text)
	timeout = time.time() + 60*t   
	while True:
		if time.time() > timeout:
			break
		else:
			# os.system("mpg123 " + tx)
			os.system("mpg123 -f "+ vol + " " + tx)
	# bell('1',vol)
	clear_q()
	return None


def remind_walking2(t=30,vol='6000',n=0):
	tt = 0.5
	if n == 1:
		text  = [["คิด"],["ก่อน"],["พูด"],["หนอ"],["พุท"],["โธ"],["พุท"],["โธ"]]
	elif n == 2:
		text =  [["รู้"],["เท้า"],["เคลื่อน"],["ไหว"],["รู้"],["ใจ"],["นึก"],["คิด"],["มี"],["จิต"],["เบิก"],["บาน"],["อยู่"],["กับ"],["ปัจ"],["จุ"],["บัน"]]
	elif n == 3:
		text = ["ตะ","ถะ","ตา","เช่น","นั้น","เอง","อิ","ทัป","ปัจ","จะ","ยะ","ตา","เพราะ","มี","สิ่ง","นี้","สิ่ง","นี้","เป็น","ปัจ","จัย","สิ่ง","นี้","สิ่ง","นี้","จึง","เกิด","ขึ้น"]
	elif n == 4:
		text  = [["ไม่"],["คิด"],["หนอ"],["ไม่"],["คิด"],["หนอ"],["พุท"],["โธ"],["พุท"],["โธ"]]
	elif n == 5:
		text  = [["ยกย่างเหยียบ1"],["ยกย่างเหยียบ1"]]
		tt = 0
	elif n == 6:
		text  = [["รู้"],["เท้า"],["เคลื่อน"],["ไหว"],["ไม่"],["ส่ง"],["ใจ"],["ออก"],["นอก"]]
	else:
		text =  [["รู้"],["กาย"],["เคลื่อน"],["ไหว"],["รู้"],["ใจ"],["นึก"],["คิด"],["มี"],["จิต"],["เบิก"],["บาน"],["อยู่"],["กับ"],["ปัจ"],["จุ"],["บัน"]]
	
	timeout = time.time() + 60*t   
	while True:
		if time.time() > timeout:
			break
		else:
			for t in text:
				tx   = thaiwords(t)
				# os.system("mpg123 " + tx)
				os.system("mpg123 -f "+ vol + " " + tx)
				time.sleep(tt)
	bell('1',vol)
	clear_q()
	return None


def remind_walking_en(t=30,vol='10',n=0):
	ts = 0.5
	if n == 1:
		text  = ["mind","your","step","unanxious","no desire","Ah happiness!","Ah happiness!"]
	elif n == 2:
		text = ["mind right foot","mind left foot"]
	elif n == 3:
		text = ["lifting moving treading","lifting moving treading","lift move tread","lift move tread"]
		ts = 0
	else:
		text =  ["right go thus","left go thus","mind","your","breath","mind","your","movements","mind","the","mind","be","cheerful","be","here","and","now","left go thus","right go thus","left go thus"]
	
	timeout = time.time() + 60*t   
	while True:
		if time.time() > timeout:
			break
		else:
			for tx in text:
				speak(tx)
				time.sleep(ts)
	bell('1',vol)
	clear_q()
	return None


def remind_relax(t=30,vol='6000'):
	bell('3',vol)
	text  = ["ทำ","ตัว","ผ่อน","คลาย","หาย","ใจ","ยาว","ยาว","คลาย","ความ","กังวล","ตั้ง","จิต","มั่น","รู้","ลม","หาย","ใจ"]
	text += ["เข้า","ออก","สั้น","ยาว","หยาบ","ละเอียด","เกิด","ดับ","ไม่","เที่ยง","หนอ"]
	tx   = thwords(text)
	timeout = time.time() + 60*t   
	while True:
		if time.time() > timeout:
			break
		else:
			# os.system("mpg123 " + tx)
			os.system("mpg123 -f "+ vol + " " + tx)
	bell('1',vol)
	clear_q()
	return None


def loop_sati(t=30,vol='6000'):
	bell('3',vol)
	os.system('mpg123 -f ' + vol + ' -loop -1 ')
	proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../voices/sati-cut.mp3"])
	delay(t)
	proc.kill()
	bell('1',vol)
	clear_q()
	return None


def wise_one(c='off',vol="6000"):
	proc = subprocess.Popen(["mpg123","-d","3","-f",vol,"-q","--loop","-1","../voices/buddho.mp3"])
	press_for_stop(c,proc)
	return None


def breathing_alpha_meditation(c='g',t=30):

	vol = "6000"
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


def alpha_meditation(m=60,t=15,c='off',vol="6000"):


	speak(str(m) + " minutes alpha sound")
	if t > 0:
		speak("and "+ str(t) + " minutes bell sound")

	bell('3',vol)

	if len(c) == 1:
		ledc(c+c)
	else:
		ledc(c)

	if t == 0:
		t = m
		alpha_wave(t)
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


def slow_buddho(c='',t=30,vol='6000',alpha=True):
	ledc(c)
	th_stand = thwords(["ยืน","หนอ"])
	for i in range(3):
		os.system('mpg123 ' + th_stand)
		# os.system('mpg123 -f ' + vol + ' ' + th_stand)
		time.sleep(1)

	del th_stand
	gc.collect()

	if alpha:
		mp3 = "../sound/buddho0.mp3"
	else:
		mp3 = "../sound/buddho1.mp3"

	if t==0:
		proc = subprocess.Popen(["mpg123","--loop","-1",mp3])
		# proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1",mp3])
		press_for_stop(c,proc)
	else:
		proc = subprocess.Popen(["mpg123","--loop","-1",mp3])
		# proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1",mp3])
		delay(t)
		proc.kill()
	
	return None


def slow_buddho2(c='',t=30,vol='6000'):
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
	proc = subprocess.Popen(["mpg123","-f","6000","-q","--loop","-1","../dataen/one_stage.mp3"])
	delay(t)
	proc.kill()
	return None

def one_stage_th_en(c='',t=5):

	th_right = thwords(['ขวา','ย่าง','หนอ'])
	th_left = thwords(['ซ้าย','ย่าง','หนอ'])
	th_stand = thwords(["ยืน","หนอ"])
	en_right = enwords(['right','goes','thus'])
	en_left = enwords(['left','goes','thus'])
	
	ledc(c)
	for i in range(3):
		os.system('mpg123 -f 6000 ' + th_stand)
		time.sleep(1)
		speak("standing")
		time.sleep(1)
	timeout = time.time() + 60*t
	while True:
		
		if time.time() > timeout:
			break
		else:
			os.system('mpg123 -f 6000 ' + th_right)
			time.sleep(1)
			os.system('mpg123 -f 6000 ' + th_left)
			time.sleep(1)

			os.system('mpg123 -f 6000 ' + en_right)
			time.sleep(1)
			os.system('mpg123 -f 6000 ' + en_left)
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
		stand = thwords(["ยืน","หนอ"])
		stage = thwords(["ยกหนอ","ย่างหนอ","เหยียบหนอ"])
	elif lg == 'zh':
		stand = zhwords(["常设"])
		stage = zhwords(['起重','移动','踩踏'])
	elif lg == 'ja':
		stand = jawords(["立っている"])
		stage = jawords(['リフティング','動く','踏む'])
	elif lg == 'ko':
		stand = kowords(["서있는"])
		stage = kowords(['리프팅','움직이는','밟기'])
	else:
		stand = ""
		stage = enwords(['lifting','moving','treading'])

	en_stage = enwords(['lifting','moving','treading'])
	
	
	ledc(c)
	for i in range(3):
		os.system('mpg123 -f 6000 ' + stand)
		time.sleep(1)
		speak("standing")
		time.sleep(1)
	timeout = time.time() + 60*t
	while True:
		
		if time.time() > timeout:
			break
		else:
			os.system('mpg123 -f 6000 ' + stage)
			time.sleep(1)
			os.system('mpg123 -f 6000 ' + en_stage)
			time.sleep(1)

			os.system('mpg123 -f 6000 ' + stage)
			time.sleep(1)
			os.system('mpg123 -f 6000 ' + en_stage)
			time.sleep(1)

	del stage
	del stand
	del en_stage
	gc.collect() 

	return None


def six_stages_th_en(c='',t=5):

	killPlayer()   
	speak(str(t) + " minutes 6 stages walking practice")
	th_stand = thwords(["ยืน","หนอ"])
	th_stage = thwords(["ยกส้นหนอ","ยกหนอ","ย่างหนอ","ลงหนอ","ถูกหนอ","กดหนอ"])
	en_stage = enwords(["heelup","lifting","moving","lowering","touching","pressing"])
	ledc(c)
	for i in range(3):
		os.system('mpg123 -f 6000 ' + th_stand)
		time.sleep(1)
		speak("standing")
		time.sleep(1)
	timeout = time.time() + 60*t
	
	while True:
		
		if time.time() > timeout:
			break
		else:
			os.system('mpg123 -f 6000 ' + th_stage)
			time.sleep(1)
			os.system('mpg123 -f 6000 ' + en_stage)
			time.sleep(1)

			os.system('mpg123 -f 6000 ' + th_stage)
			time.sleep(1)
			os.system('mpg123 -f 6000 ' + en_stage)
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

def meditation_goal(g=1,vol='6000'):
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


def before_walk(l="th",vol="6000"):
	if l == "en":
		st = "percipient of what lies in front & behind, set a distance to meditate walking back & forth, your senses inwardly immersed, your mind not straying outwards"
		espeak(t,vol)
	else:
		st = " ../voices/before_walking.mp3"
		os.system("mpg123 -q -f "+ vol + st)       


def before_sit(l="th1",vol="6000"):
	if l == 'th1':
		st = " ../voices/at_the_present.mp3"
	else:
		st = " --loop 3 ../voices/cheerful_breathing.mp3"

	os.system("mpg123 -q -f "+ vol + st)
	relax_thai(vol)


def be_happy(vol='6000'):
	st = " --loop 3 ../voices/happy.mp3"
	os.system("mpg123 -q -f "+ vol + st)


def cheerful_payutto(t=1,vol='6000'):
	proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../sound/cheerful_payutto.mp3"])
	delay(t)
	proc.kill()
	return None

def cheerful_payutto2(t=1,vol='3000'):
	i = random.randint(1,2)
	if i == 1:
		fn = "../sound/cheerful_citta.mp3"
	else:
		fn = "../sound/cheerful_citta2.mp3"
	proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1",fn])
	delay(t)
	proc.kill()
	return None

def walking_reward():
	read_sutta(sutta["sutta"][0]) 
	return None


def remind_sati():
	speak("Do not forget to mind your breathing, mind your body movement and mind your mind.")
	text = " ../voices/sati.mp3"
	os.system("mpg123 -q -f 6000 "+text)


def remind_sati_bikkhu():
	entext = """
			Come you, monk, have mindfulness and situational awareness. Act with situational awareness 
			when going out and coming back; when looking ahead and aside; when bending and extending the limbs; 
			when bearing the outer robe, bowl and robes; when eating, drinking, chewing, and tasting; 
			when urinating and defecating; when walking, standing, sitting, sleeping, waking, speaking, and keeping silent.
			"""
	speak(entext)
	text = " ../voices/sati_bikkhu.mp3"
	os.system("mpg123 -q -f 6000 "+text)


def remind_right_sati():
	speak("Ardent, fully aware, and mindful, after removing avarice and sorrow regarding the world.")
	text = " ../voices/right_sati.mp3"
	os.system("mpg123 -q -f 6000 "+text)


def remind_dead():
	text = " ../voices/dead.mp3"
	os.system("mpg123 -q -f 6000 "+text)


def mixed_mode(c='',t=10,n=0,vol='6000'):
	# remind_b4walking(vol,'th')
	if n == 15:
		pass
	else:
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
		slow_buddho(c,t,'2000',True)
	elif n == 5:
		slow_buddho(c,t,'2000',False)
	elif n == 6:
		slow_buddho2(c,t)
	elif n == 7:
		anapanasati_walk(t)
	elif n == 8:
		remind_breathing(t,'3000','th5')
	elif n == 9:
		remind_walking2(t,vol,1)
	elif n == 10:
		remind_walking2(t,vol,2)
	elif n == 11:
		remind_walking_en(t,vol,1)
	elif n == 12:
		remind_walking_en(t,vol,0)
	elif n == 13:
		remind_walking2(t,vol,1)
	elif n == 14:
		remind_walking2(t,vol,4)
	elif n == 15:
		remind_walking2(t,vol,5)
	elif n == 16:
		remind_walking2(t,vol,6)
	elif n == 17:
		alpha_wave(t)
	elif n == 18:
		remind_walking_en(t,vol,3)
	else:
		one_stage_th_en(c,t)
	return None


def get_new_dhamma_files(fp="../datath/basic_chanting/dhamma"):
	new_files = []
	for file in os.listdir(fp):
		if file.endswith(".mp3"):
			new_files.append(os.path.join(fp, file))

	# print(new_files)
	random.shuffle(new_files)
	newfiles = " + ".join(str(x) for x in new_files) 
	# print(newfiles)
	del new_files
	gc.collect()
	return newfiles

def adjust_volume():
	now = datetime.today().strftime('%H %M')
	tn = now.split()
			
	if int(tn[0]) > 18 or int(tn[0]) < 6:
		call(["amixer","-q","-M","sset","Master","65%"])
	else:
		call(["amixer","-q","-M","sset","Master","95%"])


def play_dhamma(fp="../datath/dhamma",v='1',vol='9000'):
	play_mp3("../voices/pay-attention.mp3",15)
	files= get_new_dhamma_files(fp)
	cmd = "mpg123 -C -d " + v + " -f " + vol + " " + files
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stdin=master)
	motion_detect(proc)
	os.write(slave, b'f')
	motion_detect(proc)
	os.write(slave, b'f')
	motion_detect(proc)
	os.write(slave, b'f')
	motion_detect(proc)
	os.write(slave, b'f')
	motion_detect(proc)
	os.write(slave, b'f')
	motion_detect(proc)
	killPlayer()    
	del files
	gc.collect() 
	return None


def play_dhamma2(fp="../datath/dhamma",v='1',vol='9000'):
	play_mp3("../voices/pay-attention.mp3",15)
	files= get_new_dhamma_files(fp)
	cmd = "mpg123 -C -z -d " + v + " -f " + vol + " " + files
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stdin=master)
	motion_detect(proc)
	killPlayer()    
	del files
	gc.collect() 
	return None

	
def play_my_dhamma_vlc(fp="../datath/dhamma"):
	play_mp3("../voices/pay-attention.mp3",15)
	play_mp3("../voices/pay-attention.mp3",15)
	files= get_new_dhamma_files(fp)
	cmd = "cvlc --loop --rate=1.00 "+files
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stdin=master)
	press_for_stop('d',proc)   
	del files
	gc.collect() 
	return None
	
   
def play_dhamma_with_alarm(t=60,ts=15,fp="../datath/dhamma",vol='6000',b=True):
	play_mp3("../voices/pay-attention.mp3",15)
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
	  
	
def play_mp3_with_alarm(t=60,ts=15,f="../datath/basic_chanting/paticca.mp3",vol='6000',b=False):
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
	
# Features
def what_time():
	today = datetime.today().strftime('%H %M')
	speak("The time is " + today)
	
	
def what_time2():
	today = datetime.today().strftime('%H %M')
	speak(today)


def what_day():
	today = datetime.today().strftime('%B %A %d')
	speak("Today is " + today)
	today = dt.datetime.now() 
	# text = ["วันนี้","วัน","weekday/%w","ที่","59/%d","เดือน","month/%m","เวลา","59/%H","นาฬิกา","59/%M","นาที"]
	t = "วันนี้,วัน,weekday/%w,ที่,59/%d,เดือน,month/%m,เวลา,59/%H,นาฬิกา,59/%M,นาที"
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
	del t
	del text
	del stext
	gc.collect()
	

def play_mp3(path,sec=0,vol='6000',c='off'):
	killPlayer() 
	adjust_volume() 
	proc = subprocess.Popen(["mpg123","-f",vol,"--loop","-1",path])
	press_for_stop(c,proc,sec)
	
	
def blessed_one(t=0,vol='6000'):
	play_mp3('../datath/basic_chanting/paticca.mp3',t*60,vol,'d')
	
	
def basic_chanting(t=0,vol='6000',c='off'):
	killPlayer() 
	adjust_volume()
	files = " ../datath/basic_chanting/pahung.mp3 ../datath/basic_chanting/7tamnan.mp3 ../datath/basic_chanting/7kampee.mp3 ../datath/basic_chanting/matika.mp3"
	command = "mpg123 -q -Z -f " + vol + files
	proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	press_for_stop(c,proc,60*t) 
	
def variety_chanting(t=0,vol='6000',c='off'):
	pass
	# killPlayer() 
	# command = "mpg123 -q -Z -f " + vol + " ../datath/basic_chanting/Tibetan_prayer.mp3 ../datath/basic_chanting/heart-sutra-jp.mp3 ../datath/basic_chanting/heart-sutra-tibetan.mp3 ../datath/basic_chanting/Tibet-heart-sutra.mp3 ../datath/basic_chanting/heart-sutra-zh.mp3"
	# proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	# press_for_stop(c,proc,60*t) 
	
	
def chinese_chanting(t=0,vol='6000',c='off'):
	killPlayer() 
	files = " ../datath/chinese_chanting/kuan-im-taisue.mp3 ../datath/chinese_chanting/Mantra_of_Avalokiteshvara.mp3 ../datath/chinese_chanting/Avalokiteshvara.mp3 ../datath/chinese_chanting/heart-sutra-zh.mp3 ../datath/chinese_chanting/avalo-thai.mp3"
	command = "mpg123 -q -Z -f " + vol + files
	proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	press_for_stop(c,proc,60*t) 
	

def play_daily_dependent_origination_thai(vol='6000'):
	killPlayer()  
	speak("Dependent Origination Application in Everyday Life in Thai")
	proc = subprocess.Popen(["mpg123","-f",vol,"../datath/buddhadham/paticcasamuppda.mp3"])
	motion_detect(proc)


def play_buddha_thinking_thai(vol='6000'):
	killPlayer()
	os.system("mpg123 -f 6000 -q ../voices/yoniso_thai.mp3")
	speak("Thai Buddhadham Yonisomanasikan")
	proc = subprocess.Popen(["mpg123","-f",vol,"../datath/buddhadham/yoniso.mp3"])
	motion_detect(proc)


def play_breathing_chanting_thai(vol='6000'):
	killPlayer()
	if "loop" in words:
		speak("Thai Anapanasati chanting")
		proc = subprocess.Popen(["mpg123","-f",vol,"-C","--loop","-1","../datath/chanting/anapanasati-cut.mp3"], stdin=master)
		motion_detect(proc)
	else:
		subprocess.run(["mpg123","-f","6000","../datath/chanting/anapanasati-cut.mp3"])


def play_nature_truth_chanting_thai(vol='6000'):
	killPlayer()
	speak("Thai Dhamma Ni yam chanting")
	proc = subprocess.Popen(["mpg123","-f",vol,"-C","--loop","-1","../datath/chanting/dhammaniyam.mp3"], stdin=master)
	motion_detect(proc)


def play_dependent_origination_chanting_thai(vol='6000'):
	killPlayer()  
	speak("Thai Itup paj ja ya ta Pa tij ja sa mup path chanting")
	proc = subprocess.Popen(["mpg123","-f",vol,"-C","--loop","-1","../datath/chanting/ituppajjayata.mp3"], stdin=master)
	motion_detect(proc)

def play_eight_fold_path_chanting_thai(vol="6000"):
	killPlayer()   
	# speak("Thai Noble 8 fold path chanting")
	proc = subprocess.Popen(["mpg123","-f",vol,"-C","--loop","-1","../datath/chanting/8.mp3"], stdin=master)
	press_for_stop('off',proc)


def play_eight_fold_path_chanting_english(vol='6000'):
	killPlayer()   
	speak("English Noble 8 fold path chanting")
	proc = subprocess.Popen(["mpg123","-f",vol,"-C","--loop","-1","../dataen/chanting/noble8fold.mp3"], stdin=master)
	motion_detect(proc)


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


def english_chating(vol='6000'):
	killPlayer()  
	speak("English chanting")
	subprocess.run(["mpg123","-f",vol,"-C","--list","chanting.txt"])


def thai_chanting(t=0,vol="6000"):
	killPlayer()   
	# speak("Thai chanting")
	proc = subprocess.Popen(["mpg123","-f",vol,"-C","-Z","--list","THchanting.txt"], stdin=master)
	press_for_stop('off',proc,t)


def play_radio(vol='6000'):
	killPlayer()                                    
	if have_internet():
		speak("Tibetan Buddhist internet radio")
		proc = subprocess.Popen(["mpg123","-f",vol,"-q","http://199.180.72.2:9097/lamrim"])
		press_for_stop('d',proc)
	else:
		speak("sorry no internet connection")  


def meditation_time(vol='6000'):
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
	proc = subprocess.Popen(["mpg123","-f",vol,"-q","--loop","-1","../dataen/bell15min.mp3"])
	motion_detect(proc)


def buddha_dhamma(vol='6000'):
	killPlayer()    
	speak("Buddha dhamma")
	proc = subprocess.Popen(["mpg123","-f",vol,"-q","-z","--list","THbuddhadham.txt"]) 
	press_for_stop('b',proc)

def play_sutra(vol="6000",t=0):
	killPlayer()    
	proc2 = subprocess.Popen(["mpg123","-f",vol,"-C","-z","--list","sutra.txt"], stdin=master)
	press_for_stop('d',proc2,60*t)


def play_buddha_story():
	speak("play buddha story")
	killPlayer()                
	try:
		command = "export DISPLAY=:0.0; vlc -f --play-and-exit ../mp4/buddha-story.mp4"
		proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		press_for_stop('d',proc,455)
		killPlayer() 
	except:
		speak("sorry can not play video clip")


def walking_meditation_count(c='oo'):
	
	speak("one stage walking practice, please count your step then you can verify it in the end")

	th_right = thwords(['ขวา','ย่าง','หนอ'])
	th_left = thwords(['ซ้าย','ย่าง','หนอ'])
	th_stand = thwords(["ยืน","หนอ"])
	en_right = enwords(['right','goes','thus'])
	en_left = enwords(['left','goes','thus'])
	
	ledc(c)
	for i in range(3):
		os.system('mpg123 -f 6000 ' + th_stand)
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
			os.system('mpg123 -f 6000 ' + th_right)
			time.sleep(t1)
			os.system('mpg123 -f 6000 ' + th_left)
			time.sleep(t2)

			os.system('mpg123 -f 6000 ' + en_right)
			time.sleep(t2)
			os.system('mpg123 -f 6000 ' + en_left)
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


def counting_walk(t=15,fast=False,l='th',vol='6000'):

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
		# cmd = 'mpg123 -q '
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
	speak("out off service!")
	pass


def heart_sutra(t=0,c='d',vol="6000"):
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

def wooden_gong_sound(t=0,vol='6000',c='off'):
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



def raining_meditation(t=0,c='d',vol="6000"):
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


def thunder_meditation(t=0,c='d',vol="6000"):
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


def jungle_meditation(t=0,c='d',vol="6000"):
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


def tibetan_meditation(t=0,c='d',vol="6000"):
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


def om_meditation(t=0,c='d',vol="6000"):
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
	speak("out off service!")
	pass
	# plants = ['cells.mp4','light-sd.mp4','seed-sd.mp4','water-sd.mp4','co2.mp4','npk.mp4']
	# plists = ['cell','light','seed','water','carbon','food']           
	# try:
	# 	i = plists.index(w)
	# 	speak("Play Plants " + w)
	# 	command = "export DISPLAY=:0.0; vlc -f --loop --video-on-top ../datath/basic_chanting/plants/" + plants[i]
	# 	proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	# 	motion_detect(proc)
	# except:
	# 	speak("sorry can not play video clip")

def play_tripataka_chapter(p):
	speak("out off service!")
	pass
	# killPlayer()  
	# speak("play Thai reading Tripitaka Chapter " + p)
	# proc = subprocess.Popen(["mpg123","-d","2","-f","6000","../datath/basic_chanting/tripitaka/Tripidok" + p + ".mp3"])
	# press_for_stop('d',proc)

def pali_chanting():
	speak("out off service!")
	pass

def morning_merit(vol="6000"):
	killPlayer()  
	proc = subprocess.Popen(["mpg123","-f",vol,"../datath/chanting/morning-merit.mp3"])
	press_for_stop('d',proc,192)
	
def tibetan_metta_chanting(vol="6000"):
	killPlayer()  
	proc = subprocess.Popen(["mpg123","-f",vol,"../datath/basic_chanting/tibetanmetta.mp3"])
	press_for_stop('d',proc,545)
	
def metta_chanting(vol="6000"):
	killPlayer()  
	proc = subprocess.Popen(["mpg123","-f",vol,"--loop","-1","../datath/basic_chanting/metta-sutta-chanting.mp3"])
	press_for_stop('d',proc,1800)
	
def metta_chanting_thai(vol="6000"):
	killPlayer()  
	proc = subprocess.Popen(["mpg123","-f",vol,"-Z","../datath/basic_chanting/metta-sutta.mp3","../datath/basic_chanting/metta-sutta-chanting.mp3"])
	press_for_stop('d',proc,1800)

def hdmi_display(s='on'):
	if s == 'off':
		os.system("/opt/vc/bin/tvservice -o")
	else:
		os.system("/opt/vc/bin/tvservice -p")
	espeak("turn display " + s, '50')
	return None
	
	
def sitting_sound_with_alarm(m,t=60,ts=15,vol='6000',b=True):
	speak("out off service!")
	pass
		

# sitting 1 hr
def testing_mode2():
	killPlayer()
	bell('3') 
	cheerful  = [['../sound/BloomingFlowers.mp4','154'],['../sound/flowers-blooming.mp4','192'],['../mp4/flowers.mp4','120']]
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
	alpha_wave(30)
	bell('1')
	alpha_wave(15)
	bell('1')
	alpha_wave(15)
	bell('1')
	pkill_proc_name()
	clear_q()
	return None

# walking 1 hr
def testing_mode1():
	adjust_volume()
	meditation_goal(1)
	lg = ['th','en','zh','ja','ko']
	lgx = random.choice(lg)
	walk = [0,1,2,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
	i = random.randint(1,3)
	for x in range(i):
		random.shuffle(walk)

	#bell('3')
	#relax_walk(5,'6000')
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
	i = 0
	
	mixed_mode('off',10,walk[i])
	i += 1
	
	mixed_mode('off',10,walk[i])
	i += 1
	if walk[i] == 2:
		i += 1
	
	mixed_mode('off',10,walk[i])
	i += 1
	if walk[i] == 2:
		i += 1
	
	mixed_mode('oo',10,walk[i])
	#proc1.kill()
	#pkill_proc_name("testgif")
	bell('1')
	clear_q()
	return None

def testing_mode3():
	adjust_volume()
	vol = '4000'
	meditation_goal(1)
	# walking
	lg = ['th','en'] # ['zh','ja','ko']
	lgx = random.choice(lg)
	bell('1')
	three_stages_th_en('off',10,lgx)
	bell('1')
	counting_walk(10,False,lgx)
	bell('1')
	counting_walk(10,True,lgx)
	bell('1')
	# sitting
	speak("you have 5 miniutes before sitting meditation start")
	delay(5)
	bell('1')
	play_mp3('../sound/bhadhdhe-phakhue.mp3',130)
	cheerful_payutto2(1,vol)
	bell('1')
	delay(10)
	bell('1')
	delay(10)
	bell('1')
	delay(10)
	bell('3')
	tibetan_metta_chanting(vol)


def testing_mode4():
	adjust_volume()
	vol = '4000'
	meditation_goal(1)
	# walking
	lg = ['th','en'] # ['zh','ja','ko']
	lgx = random.choice(lg)
	bell('1')
	three_stages_th_en('off',10,lgx)
	bell('1')
	counting_walk(10,False,lgx)
	bell('1')
	counting_walk(10,True,lgx)
	bell('1')
	# sitting in nature
	speak("you have 5 miniutes before sitting meditation start")
	delay(5)
	bell('1')
	play_mp3('../datath/chanting/Bhadhdherattakadha.mp3',137)
	cheerful_payutto2(1,vol)
	bell('1')
	om_meditation(10,'off',vol)
	thunder_meditation(10,'off',vol)
	jungle_meditation(10,'off',vol)
	bell('3')
	tibetan_metta_chanting(vol)


def testing_mode5():
	what_time()
	testing_mode1()
	fast_buddho('off',10,'6000')
	remind_breathing(5,'6000','th')
	alpha_wave(55)
	bell('1')
	now = datetime.today().strftime('%H %M')
	tn = now.split()
	mn = (22-int(tn[0]))*60 - int(tn[1])
	basic_chanting(mn,'5000')
	os.system("sudo shutdown now")

def testing_mode6():
	what_time()
	testing_mode1()
	fast_buddho('off',10,'6000')
	remind_breathing(5,'6000','th')
	alpha_wave(55)
	bell('1')
	ledc("off")
	now = datetime.today().strftime('%H %M')
	tn = now.split()
	mn = (22-int(tn[0]))*60 - int(tn[1])
	blessed_one(mn)
	delay(240)
	fast_buddho('off',5,'6000')
	n = [1,3,4,5]
	random.shuffle(n)
	morning_practice('off','6000',n[0])
	return None

def testing_mode7():
	what_time()
	now = datetime.today().strftime('%H %M')
	tn = now.split()
	mn = (22-int(tn[0]))*60 - int(tn[1])
	if int(tn[0]) == 17:
		testing_mode1()
	elif int(tn[0]) == 18:
		meditation_goal(1)
		three_stages_th_en('off',10,'th')
		counting_walk(5,False,'th','6000')
		bell('1')
		counting_walk(5,True,'th','6000')
		walking_meditation_count()
	else:
		pass
	fast_buddho('off',10,'6000')
	remind_breathing(5,'6000','th')
	alpha_wave(55)
	bell('1')
	ledc("off")
	blessed_one(mn,'3000')
	delay(240)
	fast_buddho('off',5,'6000')
	n = [1,3,4,5]
	random.shuffle(n)
	morning_practice('off','6000',n[0])
	return None

def testing_10():
	what_time()
	testing_mode1()
	fast_buddho('off',10,'6000')
	remind_breathing(5,'6000','th')
	alpha_wave(55)
	bell('1')
	ledc("off")
	now = datetime.today().strftime('%H %M')
	tn = now.split()
	mn = (22-int(tn[0]))*60 - int(tn[1])
	basic_chanting(mn,'6000')
	delay(240)
	fast_buddho('off',5,'6000')
	n = [1,3,4,5]
	random.shuffle(n)
	morning_practice('off','6000',n[0])
	return None
		
#For BuddhaDay
def testing_mode9():
	what_time()
	testing_mode1()
	fast_buddho('off',10,'6000')
	remind_breathing(5,'6000','th2')
	alpha_wave(55)
	bell('1')
	now = datetime.today().strftime('%H %M')
	tn = now.split()
	mn = (22-int(tn[0]))*60 - int(tn[1])
	basic_chanting(mn,'6000')
	# alpha_wave(240)
	delay(240)
	fast_buddho('off',5,'6000')
	n = [2,6]
	random.shuffle(n)
	morning_practice('off','6000',n[0])
	# os.system("sudo shutdown now")
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
	sitting_sound_with_alarm(m)
	bell('3')
	return None
	
def meditation_3():
	meditation_goal(1)
	before_walk()
	slow_buddho('off',10,'6000',False)
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
	before_walk()
	anapanasati_walk(10)
	bell('1')
	speak("you have 4 minutes before sitting practice start")
	delay(4)
	bell('1')
	m = random.randint(0,2)
	before_sit()
	if m == 1:
		remind_breathing(1,'6000')
		fast_buddho('off',10)
		remind_breathing2(1,'6000')
		om_meditation(10)
		remind_breathing2(1,'6000')
		delay(10)
		remind_breathing2(1,'6000')
		delay(10)
	elif m == 2:
		bell('1')
		delay(10)
		bell('1')
		delay(10)
		bell('1')
		delay(10)
		bell('1')
		delay(10)
	else:
		thunder_meditation(10,'off','6000')
		raining_meditation(10,'off','6000')
		jungle_meditation(10,'off','6000')
		music_meditation(10,'off','4000')

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
	alpha_wave(30)
	bell('1')
	alpha_wave(30)
	bell('1')
		
	delay(3)
	before_walk()
	slow_buddho('off',10,'6000',False)
	bell('1')
	delay(2)
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
	slow_buddho('off',10,'6000',False)
	bell('1')
	delay(4)
	testing_mode2()
	
	delay(3)
	before_walk()
	slow_buddho('off',10,'6000',False)
	bell('1')
	delay(2)
	testing_mode2()
	
	delay(3)
	before_walk()
	slow_buddho('off',10,'6000',False)
	bell('1')
	delay(2)
	testing_mode2()
	
	delay(3)
	before_walk()
	slow_buddho('off',10,'6000',False)
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
	alpha_wave(60)
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
	slow_buddho('off',10,'6000',False)
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
	slow_buddho('off',10,'6000',False)
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
	command = "export DISPLAY=:0.0; python3 testgif.py -f full -p ../images/"+sun[i]
	proc = subprocess.Popen(command, shell=True)
	proc_name = "testgif"
	return proc_name

def my_stars():
	global proc_name
	sun = ['mars.gif','moon.gif','jupiter.gif','titan.gif']
	i = random.randint(0,3)
	command = "export DISPLAY=:0.0; python3 testgif.py -f full -p ../images/"+sun[i]
	proc = subprocess.Popen(command, shell=True)
	proc_name = "testgif"
	return proc_name


def the_water():
	speak("out off service!")
	pass
	
def the_brain():
	speak("out off service!")
	pass

def the_universe(i=7,title='the space video clip'):
	speak("out off service!")
	pass


def cheer_up(i=4):
	speak("play cheerful video clip")
	killPlayer()               
	cheerful  = ['--stop-time 120 ../mp4/flowers.mp4','--start-time 8 --stop-time 208 ../mp4/flowers-blooming.mp4','../mp4/BloomingFlowers.mp4']
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
	pass


def music_meditation(t=0,c='d',vol="6000"):
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

def morning_practice(c='off',vol="6000",mode=1):
	ledc(c)
	walk = [0,1,2,4,5,9,16,17]
	i = random.randint(1,3)
	for x in range(i):
		random.shuffle(walk)
	# warm up
	t = random.randint(2,6)
	mixed_mode('off',t,14,vol)
	mixed_mode('off',10-t,15,vol)
	mixed_mode('off',t,13,vol)
	mixed_mode('off',10-t,15,vol)
	for i in range(1,5):
		mixed_mode('off',t,walk[i],vol)
		mixed_mode('off',10-t,15,vol)
	#delay(5)
	fast_buddho(c,5,vol)
	relax_thai(vol)
	#bell('1',vol)
	# start
	ledc('off')
	if mode == 1:
		cheerful_payutto2(1,vol)
		alpha_wave(15)
		bell('1',vol)
		remind_breathing2(1)
		alpha_wave(15)
		bell('1',vol)
		remind_breathing2(1)
		alpha_wave(15)
		bell('1',vol)
		remind_breathing2(1)
		alpha_wave(15)
		bell('1',vol)
		#tibetan_metta_chanting(vol)
	elif mode == 2:
		metta_chanting_thai(vol)
		remind_breathing2(1)
		blessed_one(30,vol)
		bell('1',vol)
	elif mode == 3:
		cheerful_payutto2(1,vol)
		thunder_meditation(30,c,vol)
		remind_breathing2(1)
		blessed_one(30,vol)
		bell('1',vol)
		#tibetan_metta_chanting(vol)
	elif mode == 4:
		om_meditation(30,c,'6000')
		remind_breathing2(1)
		blessed_one(30,vol)
		bell('1',vol)
		#tibetan_metta_chanting(vol)
	elif mode == 5:
		cheerful_payutto2(1,vol)
		alpha_wave(30)
		remind_breathing2(1)
		play_mp3("../datath/basic_chanting/pahung.mp3",1800,vol)
		bell('1',vol)
	elif mode == 6:
		cheerful_payutto2(1,vol)
		play_mp3("../datath/basic_chanting/pahung.mp3",1800,vol)
		blessed_one(30,vol)
		bell('1',vol)
		#tibetan_metta_chanting(vol)
	
	# cool down
	# tibetan_metta_chanting(vol)
	morning_merit(vol)
	i = random.randint(1,3)
	if i == 1 :
		play_dhamma_with_alarm(50,10,'../datath/blessingmp3',vol)
	elif i == 2:
		basic_chanting(30,vol)
		blessed_one(20,vol)
	elif i == 3:
		thai_chanting(1800,vol)
		blessed_one(20,vol)
	ledc('d')
	cheerful_payutto(1,vol)
	play_mp3("../datath/chanting/8.mp3",1010,vol)
	# play_sutra('6000',20)
	now = datetime.today().strftime('%H %M')
	tn = now.split()
	mn = (6-int(tn[0]))*60 - int(tn[1])
	chinese_chanting(mn)
	os.system("sudo shutdown now")
	return None


def morning_practice_chanting_mode(c='d',m=1,vol="1000"):
	speak("out off service!")
	pass

# For Buddha holy day start at 6:00 pm
def evening_practice(d=0,vol="6000"):
	speak("out off service!")
	pass

def i_heard(words):
	listToStr = ' '.join(map(str, words))
	espeak("words i heard , " + listToStr, '20')
	clear_q()

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
args = parser.parse_args(remaining)

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

	# https://github.com/Motion-Project/motion/
	# os.system("sudo service motion stop")

	model = vosk.Model(args.model)

	master, slave = os.openpty()

	with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device, dtype='int16',
							channels=1, callback=callback):
			print('#' * 80)
			print('Press Ctrl+C to stop playing')
			print('#' * 80)
			# print(args.samplerate)
			# print(args.device)
			#metta_chanting_thai()

			os.system('espeak -s 130 -v "english-us" "Nothing is worth insisting on"')
			os.system('mpg123 -q -f 6000 ../voices/hello.mp3')
			
			# new runtime vocabulary
			new_vocab = runtime_vocabulary()
			vrun  = '["please zen story lord buddha buddhist buddhism what time day play help dhamma meditation english radio start light star noble '
			vrun += 'browse chanting mantra say speak stop volume turn on off exit shutdown now thai lyric ip address sutra up down breathing '
			vrun += 'one two three four five six seven eight nine ten zero fifteen twenty thirty forty fifty sixty seventy eighty ninety dryad '
			vrun += 'a alfa b bravo c charlie d delta e echo f foxtrot g golf h hotel i india j juliet k kilo l lima m mike n november o oscar p papa '
			vrun += 'q quebec r romeo s sierra t tango u uniform v victor w whiskey x ray y yankee z zulu letter repeat space spelling speaker  mendicant '
			vrun += 'walk walking mode search translate service cancel restart save anat ta sitting music raining thunder jungle tibetan heart brain '
			vrun += 'red green blue yellow alpha breathing pure monk rule speech morning evening practice web server sound my math next new computer '
			vrun += 'ohm variety basic chinese blessed blessing the sun blooming flower clip quit my display testing water morse code good bye chapter pali japanese chinese '
			vrun += 'korean sixteen seventeen eighteen nineteen plants seed carbon food cell universe your name cheerful silent quiet wooden '
			vrun += new_vocab
			# vrun += ' how are you today what can i do for you ' #test
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
			uni = ['you are here','why the moon','Mars 60000 days','the sun','earth view from ISS','night sky','the universe']
			time.sleep(1)
			i = random.randint(1,5)
			meditation_goal(i,'6000')
			time.sleep(1)
			os.system('mpg123 -q ../voices/samesame.mp3')
			# espeak('hi,there! my name is anat ta, please call my name if you want to start','50')
			time.sleep(1)
			with q.mutex:
				q.queue.clear()

			while True:
				data = q.get()
				# print(q.qsize())       
				
				words = []

				if rec.AcceptWaveform(data):
					w = rec.Result()
					z = json.loads(w)
					print(z["text"])
					print(q.qsize()) 
					words += z["text"].split()

					# say "anat ta" to start
					if z["text"] == "anat ta":
						if not bot:
							bot = True
							words = []
							speak("yes, what can i do for you?")
							clear_q()
					elif z["text"] == "hello":
						espeak("Hello!",'20')
						clear_q()
					elif z["text"] == "computer":
						espeak("what's up?",'20')
						clear_q()
					elif z["text"] == "dryad":
						espeak("hi!",'20')
						clear_q()
					elif z["text"] == "please help":
						get_help()
						clear_q()
						words = []
					elif not bot:
						words = []

					if repeat:  

						if not yesno and bot and len(words) > 0:
							espeak("Do you said " + z["text"] + "?",'10') 
							right_words = words
							words = []
							yesno = True
							clear_q()
						elif yesno:
							if "no" in words:
								words = []
								yesno = False
								espeak("ok, please speak again",'50')
								clear_q()
							elif "yes" in words:
								words = right_words
								speak(words)
								yesno = False
							else:
								words = []
								text  =  " ".join(str(x) for x in right_words) 
								espeak("Do you said " + text + "?",'50')
								espeak("please answer yes or no",'50')
								clear_q()
						else:
							words = []
					 
					#coding
					if not focus and len(words) > 1:

						print(words)

						if "say" in words:
							listToStr = ' '.join(map(str, words))
							listToStr = listToStr.replace("say",'')
							speak("You said, " + listToStr)
							clear_q()

						elif "wise" in words:
							if "alpha" in words:
								wise_one('gg')
							elif "one" in words:
								wise_one()
							else:
								i_heard(words)

						elif "morning" in words:
							if "one" in words:
								x = [1,3,4,5,2,6]
								random.shuffle(x)
								if x[0] == 1:
									espeak("morning practice 1, alpha sound",'50')
									morning_practice('off','6000',1)
								elif x[0] == 3:
									espeak("morning practice 3, thunder",'50')
									morning_practice('off','6000',3)
								elif x[0] == 4:
									espeak("morning practice 4, tibetan music",'50')
									morning_practice('off','6000',4)
								elif x[0] == 5:
									espeak("morning practice 5, par hoong",'50')
									morning_practice('off','6000',5)						
							elif "two" in words:
								espeak("morning practice 2, metta",'50')
								morning_practice('off','6000',2)
							elif "six" in words:	
								espeak("morning practice 6, par hoong and metta",'50')
								morning_practice('off','6000',6)
																
						elif "blessing" in words:
							if "one" in words:
								blessed_one()
							elif "two" in words or "sutra" in words:
								play_sutra()
							elif "four" in words:
								basic_chanting(0)
							# elif "five" in words:
							# 	variety_chanting(0)
							elif "six" in words:
								play_mp3_with_alarm()
							else:
								speak("1 paticca chanting, 2 Sutra, 4 basic chanting")
								clear_q()
								
						elif "morse" in words and "code" in words:
							if len(words) > 2:
								lt = words[2]
								if len(lt) == 1:
									try:
										n = ics_list.index(lt) + 1
										espeak('morse code for ' + lt + ' ' + ics_list[n],'50')
										morsecode(lt)
									except:
										pass
							else:
								morsecode('sati sati sati')
						# elif "plants" in words:
						# 	i = words.index('plants') + 1
						# 	try:
						# 		if len(words[i]) > 1:
						# 			play_plants(words[i])
						# 		else:
						# 			pass
						# 	except:
						# 		pass

						# elif "chapter" in words:
						# 	if "sixteen" in words:
						# 		p = '16'
						# 	elif "seventeen" in words:
						# 		p = '17'
						# 	elif "eighteen" in words:
						# 		p = '18'
						# 	elif "nineteen" in words:
						# 		p = '19'
						# 	else:
						# 		p = ''

						# 	if p == '':
						# 		pass
						# 	else:
						# 		play_tripataka_chapter(p)

						elif "testing" in words:
							if "one" in words:
								speak("testing 1")
								testing_mode1()
							elif "two" in words:
								speak("testing 2")
								testing_mode2()
							elif "three" in words:
								speak("testing 3, 30 minutes walking and 30 minutes sitting")
								testing_mode3()
							elif "four" in words:
								speak("testing 4, 30 minutes walking and 30 minutes sitting in nature sound")
								testing_mode4()
							elif "five" in words:
								speak("testing 5")
								testing_mode5()
							elif "six" in words:
								speak("testing 6")
								testing_mode6()
							elif "seven" in words:
								speak("testing 7")
								testing_mode7()
							elif "nine" in words:
								speak("testing 9")
								testing_mode9()
							elif "ten" in words:
								speak("testing ten")
								testing_10()
							else:
								i_heard(words)
								
						elif "repeat" in words:
							if "on" in words:
								repeat = True
								speak("Repeat mode on")
							elif "off" in words:
								repeat = False
								speak("Repeat mode off")

						elif "anat" in words and "ta" in words:
							if len(words) == 2:
								speak("yes!")
							elif "play" in words:
								if "dhamma" in words:
									play_dhamma()
								else:
									pass
							elif "stop" in words:
								killPlayer()
								bot = False
								speak("ok, call my name when you need help, bye bye!")
							elif "restart" in words:
								speak("restart the service, please wait")
								os.system("sudo reboot")
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

						elif "alpha" in words:
							if "sixty" in words:
								t = 60
							elif "ninety" in words:
								t = 90
							else:
								t = 30
							
							if "breathing" in words:
								breathing_alpha_meditation('g',t);
							elif "pure" in words:
								pure_alpha() # for martian monk only 
							else:
								alpha_meditation(t,15,'g')

						elif "meditation" in words:
							if "math" in words:
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
							elif "one" in words:
								speak("10 minutes walking and 40 minutes sitting")
								meditation_1()
							elif "two" in words:
								speak("2 hours")
								meditation_2()
							elif "three" in words:
								speak("1 hours")
								meditation_3()
							elif "four" in words:
								speak("4 hours meditation")
								meditation_4()
							elif "five" in words:
								speak("1 hour")
								meditation_5()
							elif "seven" in words:
								speak("1 hour")
								meditation_7()
							elif "six" in words:
								speak("4 hours with cheerful clip")
								meditation_6()
							else:
								i_heard(words)
								
						elif "chinese" in words and "chanting" in words:
							chinese_chanting(0)

						elif "walking" in words and "japanese" in words:
							three_stages_th_en('off',10,'ja')
							counting_walk(10,False,'ja','6000')
							counting_walk(10,True,'ja','6000')

						elif "walking" in words and "chinese" in words:
							three_stages_th_en('off',10,'zh')
							counting_walk(10,False,'zh','6000')
							counting_walk(10,True,'zh','6000')

						elif "walking" in words and "korean" in words:
							three_stages_th_en('off',10,'ko')
							counting_walk(10,False,'ko','6000')
							counting_walk(10,True,'ko','6000')

						elif "walking" in words and "thai" in words:
							meditation_goal(1)
							three_stages_th_en('off',10,'th')
							counting_walk(5,False,'th','6000')
							bell('1')
							counting_walk(5,True,'th','6000')
							walking_meditation_count()
							
						elif "walking" in words and "english" in words:
							three_stages_th_en('off',10,'en')
							counting_walk(5,False,'en','6000')
							bell('1')
							counting_walk(5,True,'en','6000')
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
							# # for martian monk only     
							# elif "morning" in words:
							# 	if"one" in words:
							# 		verify_words = 'Do you want to play pahoong chanting morning practice?'
							# 		mn = 1
							# 	elif "two" in words:
							# 		verify_words = 'Do you want to play martika chanting morning practice?'
							# 		mn = 2
							# 	elif "three" in words:
							# 		verify_words = 'Do you want to play 7 kumpee chanting morning practice?'
							# 		mn = 3
							# 	else:
							# 		verify_words = 'Do you want to play morning practice?'
							# 		mn = 0

							# 	mp = True    
							# 	verify = True
							# 	focus  = True

							# elif "evening" in words:
							# 	if "one" in words:
							# 		verify_words = 'Do you want to play pahoong chanting in the morning?'
							# 		mn = 1
							# 	elif "two" in words:
							# 		verify_words = 'Do you want to play martika chanting in the morning?'
							# 		mn = 2
							# 	elif "three" in words:
							# 		verify_words = 'Do you want to play 7 kumpee chanting in the morning?'
							# 		mn = 3
							# 	elif "four" in words:
							# 		verify_words = 'Do you want to play random chanting in the morning?'
							# 		mn = 4
							# 	elif "six" in words:
							# 		verify_words = 'Do you want to play alpha sound in the evening?'
							# 		mn = 6 
							# 	else:
							# 		verify_words = 'Do you want to play basic mode evening practice?'
							# 		mn = 0

							# 	ep = True
							# 	verify = True
							# 	focus  = True
							# else:
							# 	speak("what practice mode do you want ?")
							# 	clear_q()                             

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
								speak("My name is Anat ta")

						elif "buddha" in words and "day" in words:
							buddha_day()
							
						elif "zen" in words and "story" in words:
							nn = sequence[n]
							speak("Do you want to listen to this zen story?")
							speak(d["zen101"][nn]["title"])
							focus = True
							zen = True

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

						elif "chanting" in words:

							if "english" in words:
								english_chating()

							elif "thai" in words:
								thai_chanting()

							elif "breathing" in words:
								play_breathing_chanting_thai()

							elif "nature" in words:
								play_nature_truth_chanting_thai() 

							elif "pali" in words:
								pali_chanting()
								
							elif "basic" in words:
								basic_chanting(0)
								
							elif "variety" in words:
								variety_chanting(0)

							elif "heart" in words:

								if "clip" in words:
									speak("play heart sutra with lyrics")
									killPlayer()                
									try:
										command = "export DISPLAY=:0.0; vlc -f --loop --video-on-top ../mp4/heart-sutra.mp4"
										proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
										press_for_stop('d',proc)
										killPlayer() 
									except:
										speak("sorry can not play video clip")
								else:
									heart_sutra(0)
							else:
								speak("Do you want to play Thai Chanting ?")
								cmd = "thai_chanting"
								focus = True
								verify = True

						elif "radio" in words:
							if "play" in words or "start" in words:
								play_radio()
							else:
								speak("Do you want to play online tibetan radio ?")
								cmd = "radio"
								verify = True
								focus  = True
																
						elif "sutra" in words:
							if "play" in words or "start" in words:
								play_sutra()
							else:
								speak("Do you want to play sutra?")
								cmd = "sutra"
								verify = True
								focus  = True                              
							
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
									one_stage_en('g',t)
								else:
									one_stage_th_en('g',t)

							elif "three" in words:
								three_stages_th_en('g')

							elif "six" in words:
								six_stages_th_en('g')                    
						   
						elif "dhamma" in words:
							if "buddha" in words:
								pass
							elif "play" in words:
								play_dhamma()
							elif "one" in words:
								play_dhamma2()
							elif "two" in words:
								play_dhamma_with_alarm(180,15,'../datath/dhamma')
							elif "three" in words:
								play_dhamma_with_alarm(120,15,'../datath/chanting')
							elif "six" in words:
								play_dhamma_with_alarm(120,15,'../datath/sutta','6000',False)
							else:
								speak("Do you want to play dhamma ?")
								cmd = "dhamma"
								verify = True
								focus  = True
						  
						#PLAY

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

						elif "my" in words and "sun" in words:
							espeak("open sun gif animation",'4')
							sun = ['sun1.gif','sun2.gif']
							i = random.randint(0,1)
							command = "export DISPLAY=:0.0; python3 testgif.py -f full -p ../sound/"+sun[i]
							proc = subprocess.Popen(command, shell=True)
							proc_name = "testgif"
							proc_bool = True
							# fast_buddho('d',0)

						elif "cheerful" in words and "clip" in words:
							cheer_up()
							cheerful_animals()

						elif "blooming" in words and "flower" in words:
							speak("the blooming flowers time lapse for cheerful meditation")
							killPlayer()  
							cheerful = [['BloomingFlowers.mp4','154'],['flowers-blooming.mp4','192']]
							i = random.randint(0,1)              
							try:
								command = "export DISPLAY=:0.0; vlc -f --loop --stop-time " + cheerful[i][1] + " --video-on-top ../sound/" + cheerful[i][0]
								proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
								press_for_stop('d',proc)
								killPlayer() 
							except:
								speak("sorry can not play video clip")

						elif "browse" in words:
							if "buddhism" in words:
								speak("open Thai buddhism in wikipedia")
								command = "export DISPLAY=:0.0; chromium-browser --incognito --start-fullscreen --start-maximized https://th.wikipedia.org/wiki/ศาสนาพุทธ"
								proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
								motion_detect(proc)
								os.system("sudo pkill -f chromium")

							elif "buddhist" in words and "story" in words:
								speak("open youtube for buddhist stories")
								command = "export DISPLAY=:0.0; chromium-browser --incognito --start-fullscreen --start-maximized https://www.youtube.com/watch?v=tI-hgIhFDT0&list=PLYBNr5a72-497Q3UVkpDB24W4NTCD5f2K"
								proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
								motion_detect(proc)
								os.system("sudo pkill -f chromium")

							elif "meditation" in words and "technique" in words:
								speak("open youtube for meditation technique")
								command = "export DISPLAY=:0.0; chromium-browser --incognito --start-fullscreen --start-maximized https://www.youtube.com/playlist?list=PLUh8U5np7D-7FMh6ONGwnaltFppPBwTVI"
								proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
								motion_detect(proc)
								os.system("sudo pkill -f chromium")
							elif "webcam" in words:
								speak("open webcam on web browser")
								ip = get_ip()
								command = "export DISPLAY=:0.0; chromium-browser --incognito --start-fullscreen --start-maximized " + ip + ":8081"
								proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
								motion_detect(proc)
								os.system("sudo pkill -f chromium")

						elif "good" in words and "bye" in words:
							shutdown()
							break
						# aplay -L , aplay -lL, amixer -c1
						elif "volume" in words:
							if "up" in words:
								call(["amixer","-q","-M","sset","Master","100%"])
								espeak("set volume to 100%",'10')
							elif "down" in words:
								call(["amixer","-q","-M","sset","Master","50%"])
								espeak("set volume to 40%",'100')
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
							i_heard(words)
													   
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
									if mp:
										if mn == 0:
											morning_practice()
										else:
											morning_practice_chanting_mode('d',mn)
										verify = False
										mp = False
										focus = False
									elif ep:
										evening_practice(d)
										verify = False
										ep = False
										focus = False
									elif un:
										the_universe(mn,uni[mn])
										un = False
										verify = False
										focus = False
									
									elif cmd != "":
										if cmd == "radio":
											play_radio()
											cmd = ""
											verify = False
											focus = False
										elif cmd == "sutra":
											play_sutra()
											cmd = ""
											verify = False
											focus = False
										elif cmd == "dhamma":
											play_dhamma()
											cmd = ""
											verify = False
											focus = False
										elif cmd == "thai_chanting":
											thai_chanting()
											cmd = ""
											verify = False
											focus = False


								else:
									espeak(verify_words,'50')
									espeak("please answer yes or no",'50')
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
										bell('3','6000')
										fast_buddho('y',15)
										fast_buddho('yy',15)
										bell('3','6000')
										fast_buddho('g',15)
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

										one_stage_en('g',10)

										three_stages_th_en('b',10)
										
										remind_sati()

										slow_buddho2('c',15)
										fast_buddho('gg',15)

										remind_right_sati()

										fast_buddho('off',180)
										
										ledc('off')
										alpha_wave(240)
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

										one_stage_th_en('g',15)

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
										bell('3','6000')
										fast_buddho('d',0)
										mantra = False
										focus = False

									else :
										speak(str(t) + " minutes buddho mantra")
										bell('3','6000')
										fast_buddho('g',t)
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
									motion_detect(proc)
									os.system("sudo pkill -f chromium")
									focus = False
									spell = False

								elif "translate" in words:
									speak("please see the translation on the monitor and push button to Quit")
									command = 'export DISPLAY=:0.0; chromium-browser --incognito --start-fullscreen --start-maximized https://www.google.com/search?q="translate ' + spell_words + '"'
									proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
									motion_detect(proc)
									os.system("sudo pkill -f chromium")
									focus = False
									spell = False

								elif "exit" == words[0]:
									speak("Quit spelling mode")
									focus = False
									spell = False

								else:
									listToStr = ' '.join(map(str, words))
									espeak("i heard , " + listToStr, '50')
									if yesno:
										espeak("please answer yes or no",'50')
									else:
										espeak("next letter please", '50')
									clear_q()   
							
							elif sit:

								if yesno:
									if "yes" in words:
										speak(str(t) + " minutes " + ch_name[k])
										if ch[k] == 'a':
											bell('3','6000')
											fast_buddho('off',t)
											bell('1','6000')
											focus = False
											sit = False
										elif ch[k] == 'b':
											bell('3','6000')
											remind_breathing(t)
											bell('1','6000')
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
											bell('3','6000')
											ledc('gg')
											delay(t)
											bell('1','6000')
											focus = False
											sit = False
										elif ch[k] == 'f':
											remind_relax(t)
											focus = False
											sit = False
										elif ch[k] == 'i':
											bell('3','6000')
											om_meditation(t)
											bell('1','6000')
											focus = False
											sit = False
										elif ch[k] == 'j':
											bell('3','6000')
											music_meditation(t)
											bell('1','6000')
											focus = False
											sit = False
										elif ch[k] == 'k':
											bell('3','6000')
											blessed_one(t)
											bell('1','6000')
											focus = False
											sit = False
										elif ch[k] == 'l':
											bell('3','6000')
											raining_meditation(t)
											bell('1','6000')
											focus = False
											sit = False
									elif "no" in words:
										yesno = False
										speak("please select new choice ")
										speak(ch)
										clear_q()
									else:
										listToStr = ' '.join(map(str, words))
										espeak("i heard , " + listToStr, '50')
										espeak("please answer yes or no",'50')
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
											espeak("i heard , " + listToStr, '50')
											speak("please select")
											speak(ch)
											yesno = False
											clear_q()
											

except KeyboardInterrupt:
	print('\nDone')
	parser.exit(0)
except Exception as e:
	parser.exit(type(e).__name__ + ': ' + str(e))


# https://raspberrypi.stackexchange.com/questions/61305/how-do-you-clean-up-unused-files-in-memory-sd-card