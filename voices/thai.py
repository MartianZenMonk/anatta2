from gtts import gTTS 
import time
text = []
i = 0
m = 3512
n = 9000
# infile = open("thai-wordlist.txt", 'r')
infile = open("tnc_freq.txt", 'r')
#for line in infile :
while i < n:
	line = infile.readline()
	print(i)
	if i>m:
		tx = line.strip().split()
		print(tx[0])
		speech = gTTS(text = tx[0],lang='th',slow = False)
		speech.save("thai/"+tx[0]+".mp3")
		if i%50 == 0:
			time.sleep(300)
		else:
			time.sleep(10)
	i += 1

infile.close() 

# for tx in text:
# 	print(tx)
	# speech = gTTS(text = tx,lang='th',slow = False)
	# speech.save("th/"+tx+".mp3")
