# from gtts import gTTS 
import os
# from pydub import AudioSegment
# from pydub.playback import play

def speakThai_mp3(texts,vol='1000'):
	stext = ""
	for tx in texts:
		stext += "thai/" + tx + ".mp3 "	
	os.system('mpg123 -d 2 -f ' + vol + ' ' + stext)
	#os.system("cvlc --play-and-exit --gain 0.10 --rate 2.00 " + stext)
# def speakThai(texts,dB=20):
# 	thsound = AudioSegment.empty()
# 	stext = ""
# 	for tx in texts:
# 		stext = "thai/" + tx + ".mp3"
# 		thsound += AudioSegment.from_mp3(stext)
# 	play(thsound-dB)
# tx = ['ฟัง','ธรรม','ค่ะ']
# # tx = ["รู้","ลม","ยาว","รู้","ลม","สั้น"]
# speakThai_mp3(tx)
# speakThai(tx)

tx = "เรือ ว่าง ชาย คน หนึ่ง ลาก จูง เรือ สอง ลำ เพื่อ ข้าม แม่ น้ำ ปรากฏ มี เรือ ว่าง เปล่า ลำ หนึ่ง ลอย มา จะ ปะทะ ชน กับ เรือ ของ เขา เขา ย่อม พยายาม ลาก จูง เรือ หลบ แต่ หาก มี คน นั่ง อยู่ ใน เรือ ที่ แล่น มา ชน เขา ก็ ตะโกน ให้ เบี่ยง หลบ และ หาก อีก ฝ่าย ยัง นิ่ง เฉย เขา ก็ ลุก ขึ้น ร้อง ด่า"

txs = tx.split(' ')
print(txs)
speakThai_mp3(txs)
# text = ['오른발','왼발','서다']

# for tx in text:
# 	print(tx)
# 	speech = gTTS(text = tx,lang='ko',slow = False)
# 	speech.save("ko/"+tx+".mp3")
