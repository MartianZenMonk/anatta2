from gtts import gTTS 
import os

t = 'ไม่กังวล อะไร ไม่ต้องการ สิ่งใด สุขหนอ สุขหนอ'
tx = t.split(' ')
for i in tx:
	speech = gTTS(text = str(i),lang='th',slow = False)
	speech.save(str(i)+".mp3")

