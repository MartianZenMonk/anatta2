import schedule
import time
import os
import sys

import pyttsx3
engine = pyttsx3.init() # object creation
engine.setProperty('voice','english-us') 
engine.setProperty('rate', 130)
engine.setProperty('volume',0.1)

def speak(text):
        print (text)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
        return None

def sati():
        speak("Do not forget to mind your breathing, mind your body movement and mind your mind.")
        text = " ../thaivoices/sati.mp3"
        os.system("mpg123 -q -f 2000 "+text)
        return None

schedule.every(30).minutes.do(sati)
#schedule.every().hour.do(job)
#schedule.every().day.at("10:30").do(job)
#schedule.every(5).to(10).minutes.do(job)
#schedule.every().monday.do(job)
#schedule.every().wednesday.at("13:15").do(job)
#schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)



# https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds
