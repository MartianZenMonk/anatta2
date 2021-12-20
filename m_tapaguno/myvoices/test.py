from gtts import gTTS 
import os

# file = open("moggallana.txt", "r").read().replace("\n", " ")
# speech = gTTS(text = str(file),lang='en',slow = False)
# speech.save("moggallana.mp3")

# for i in range(59,60):
# 	speech = gTTS(text = str(i),lang='th',slow = False)
# 	speech.save(str(i)+".mp3")

#weekday = ["อาทิตย์","จันทร์","อังคาร","พุทธ","พฤหัสบดี","ศุกร์","เสาร์"]

#month = ["เดือน","มกราคม","กุมภาพันธ์","มีนาคม","เมษายน","พฤกษภาคม","มิถุนายน","กรกฎาคม","สิงหาคม","กันยายน","ตุลาคม","พฤศจิกายน","ธันวาคม"]

#others = ["วันนี้","วัน","ที่","เวลา","นาฬิกา","นาที","วันพระ","ถัดไป","คือ","สวดมนต์","ฟังธรรม","ท่านพุทธทาส","ท่าน ป. อ. ปยุตโต","พุทธธรรม","พระสูตร"]

# for i in range(0,15):
# 	speech = gTTS(text = str(others[i]),lang='th',slow = False)
# 	speech.save(str(i)+".mp3")

#text = "ชั่วโมงปฏิบัติธรรม เสียงระฆังจะดังทุกๆสิบห้านาที ผู้ปฏิบัติอาจจะเริ่ม ด้วยการเดินจงกรมก่อน แล้วค่อยนั่ง เพื่อการ ผ่อนคลาย การเดินจงกรมอาจจะเดิน สามจังหวะ ยก ย่าง เหยียบ หรือ ขวา ย่าง หนอ ซ้าย ย่างหนอ "
#text += "หรือหนึ่งจังหวะ รู้เหยียบ หรือ ขวา พุท ซ้าย โธ"

# text = "สัพเพ ธัมมา นาลัง อภินิเวสายะ สิ่งทั้งหลายทั้งปวง ไม่ควรยึดมั่นถือมั่น ธรรมะสวัสดีค่ะ"

text = ["ยก","ย่าง","ยกย่างเหยียบ"]

for tx in text:
	print(tx)
	speech = gTTS(text = tx,lang='th',slow = False)
	speech.save("mp3/th/"+tx+".mp3")



# text = ['起重','移动','踩踏',"常设"]
# for tx in text:
# 	print(tx)
# 	speech = gTTS(text = tx,lang='zh',slow = False)
# 	speech.save("mp3/zh/"+tx+".mp3")

# text = ['リフティング','動く','踏む',"立っている"]
# for tx in text:
# 	print(tx)
# 	speech = gTTS(text = tx,lang='ja',slow = False)
# 	speech.save("mp3/ja/"+tx+".mp3")

# text = ['리프팅','움직이는','밟기','서 있는','1','2','3','4','5','6','7','8','9','10']
# for tx in text:
# 	print(tx)
# 	speech = gTTS(text = tx,lang='ko',slow = False)
# 	speech.save("mp3/ko/"+tx+".mp3")


