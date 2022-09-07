from gtts import gTTS 
texts = ["รง","สุขหนอ"]
for tx in texts:
	speech = gTTS(text = tx,lang='th',slow = False)
	speech.save("../voices/thai/"+tx+".mp3")