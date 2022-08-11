from gtts import gTTS 
import os

text = ['ลมหายใจ']
#text = ["ก่อน","จุ","บัน","สุข","ปัจ","ยก","ย่าง","ยกย่างเหยียบ"]
for tx in text:
	print(tx)
	speech = gTTS(text = tx,lang='th',slow = False)
	speech.save("../sound/"+tx+".mp3")

# text = ['右足で行く','左足が行く','台']

# for tx in text:
# 	print(tx)
# 	speech = gTTS(text = tx,lang='ja',slow = False)
# 	speech.save("ja/"+tx+".mp3")

# text = ['右脚走','左脚走','站立']

# for tx in text:
# 	print(tx)
# 	speech = gTTS(text = tx,lang='zh',slow = False)
# 	speech.save("zh/"+tx+".mp3")


#text = ['오른발','왼발','서다']

#for tx in text:
#	print(tx)
#	speech = gTTS(text = tx,lang='ko',slow = False)
#	speech.save("ko/"+tx+".mp3")
