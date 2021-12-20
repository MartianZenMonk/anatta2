from gtts import gTTS 
import os

text = ["ส่ง","ออก","นอก"]

for tx in text:
	print(tx)
	speech = gTTS(text = tx,lang='th',slow = False)
	speech.save("th/"+tx+".mp3")

