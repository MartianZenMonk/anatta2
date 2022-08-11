import os
import sys
import time

def thaiwords2(text):
	stext = ""
	for i in range(len(text)):
		stext += " ../voices/thai/" + text[i] + ".mp3"
	return stext

def remind_breathing2(t=30,vol='500'):
	#bell('3',vol)
	text  = ["รู้","ลม","หาย","ใจ","อย่า","มัว","เพลิน","คิด","ปรุง","แต่ง","ใน","เรื่อง","ไม่","จริง"]
	tx   = thaiwords2(text)
	timeout = time.time() + 60*t   
	while True:
		if time.time() > timeout:
			break
		else:
			os.system("mpg123 -f "+ vol + " " + tx)
	bell('1',vol)
	clear_q()
	return None

remind_breathing2(1)