# from gtts import gTTS 
import os
import random
import time
from pydub import AudioSegment
from pydub.playback import play

def speakThai_mp3(texts,d='1',vol='1000'):
	stext = ""
	for tx in texts:
		stext += "thai/" + tx + ".mp3 "	
	os.system('mpg123 -d ' + d + ' -f ' + vol + ' ' + stext)


def speakThai_vlc(texts,rate='1.50',gain='0.1'):
	stext = ""
	for tx in texts:
		stext += "thai/" + tx + ".mp3 "	
	os.system('cvlc --play-and-exit --rate ' + rate + ' --gain ' + gain + ' ' + stext)

def speakThai(texts,dB=20):
	thsound = AudioSegment.empty()
	stext = ""
	for tx in texts:
		a = AudioSegment.empty()
		stext = "thai/" + tx + ".mp3"
		try:
			a = AudioSegment.from_mp3(stext)
			b = len(a)
			if b > 600 :
				b = b/2
			thsound += a[:b]
		except:
			pass
	play(thsound-dB)

# tx = ['ฟัง','ธรรม','ค่ะ']
# # tx = ["รู้","ลม","ยาว","รู้","ลม","สั้น"]
# speakThai_mp3(tx)
# speakThai(tx)


tx = [
["เรือ ว่าง"],
["ชาย คน หนึ่ง ลาก จูง เรือ สอง ลำ เพื่อ ข้าม แม่ น้ำ"],
["ปรากฏ มี เรือ ว่าง เปล่า ลำ หนึ่ง ลอย มา จะ ปะทะ ชน กับ เรือ ของ เขา"],
["เขา ย่อม พยายาม ลาก จูง เรือ หลบ"],
["แต่ หาก มี คน นั่ง อยู่ ใน เรือ ที่ แล่น มา จะ ชน เขา"],
["เขา ก็ ตะโกน ให้ เบี่ยง หลบ และ หาก อีก ฝ่าย ยัง นิ่ง เฉย เขา ก็ ลุก ขึ้น ร้อง ด่า"]
]

for x in tx:
	txs = x[0].split(' ')
	print(txs)
	speakThai(txs)
	# time.sleep(5)
	# i =  random.randint(1,2)
	# speakThai_mp3(txs,str(i))
	# i = random.choices(['1.00','1.25','1.50','1.75','2.00'])[0]
	# speakThai_vlc(txs,i)