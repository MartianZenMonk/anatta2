import os
import sys
import time
import math
import pyttsx3
import subprocess
import pyttsx3
import csv
import gc

from aiy.board import Board, Led
from aiy.leds import (Leds, Pattern, PrivacyLed, RgbLeds, Color)
import datetime as dt
from datetime import datetime


try:
    import httplib
except:
    import http.client as httplib

def have_internet():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False


import requests
from pprint import pprint
from urllib.request import urlopen
from json import load


def ipInfo(addr=''):
    
    if addr == '':
        url = 'https://ipinfo.io/json'
    else:
        url = 'https://ipinfo.io/' + addr + '/json'
    res = urlopen(url)
    #response from url(if res==None then check connection)
    data = load(res)

    #will load the json response into data
    # for attr in data.keys():
    #     #will print the data line by line
    #     print(attr,' '*13+'\t->\t',data[attr])

    loc = data['loc'].split(',')
    query='lat='+loc[0]+'&lon='+loc[1]
    res=requests.get('https://fcc-weather-api.glitch.me/api/current?'+query)

    return res.json();

# import geocoder
# g = geocoder.ip('me')
# print(g.latlng)

# podcast
# import feedparser
# import webbrowser

# # feed = feedparser.parse("https://dharmachakra.libsyn.com/rss")  
# feed = feedparser.parse("https://dharmabytes.libsyn.com/rss")

# feed_entries = feed.entries
# article_title = feed_entries[0].title
# article_link = feed_entries[0].link


engine = pyttsx3.init()  # object creation
engine.setProperty('voice', 'english-us')
engine.setProperty('rate', 130)
engine.setProperty('volume', 0.1)


with open('myhora-buddha-2564.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

day = datetime.today().strftime('%Y%m%d')
holyday = []
thholyday = []

for i in range(len(data)):
    if i > 0:
        if(int(data[i][1]) > int(day)):
            holyday.append(data[i][1])
            thholyday.append(data[i][0])
t = thholyday[0].replace("(", " ")
x = t.split()

bdaytext = ""
for i in range(len(x)-1):
  bdaytext += " ../thaivoices/thwords/" + x[i] + ".mp3"


def speak(text):
        print(text)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
        return None



# flite Voices available: kal awb_time kal16 awb rms slt  
# def speakf(v,t,*args):
#         os.system('flite -voice ' + v + ' -t "' + str(t) + '"')
#         return None


# if install espeak-ng
# sudo apt-get install synaptic (or install via this)
# sudo apt-get install mbrola mbrola-us (1-3)

# voices = ["en-gb","en-us","en-gb-scotland","en-gb-x-gbclan","en-gb-x-gbcwmd","en-029"]

def speakng(t,v='',*args):
        if v == '':
                v = "en-us"
        os.system('speak-ng -a 15 -v ' + v + ' "' + str(t) + '"')
        return None


def main():
        # os.system("amixer -D pulse sset Master 60%")
        text = ["ยิน","ดี","ต้อน","รับ","สู่","โครง","การ","อนัตตา","ขอ","ให้","ท่าน","มี","ความ","สุข","กับ","การ","ปฏิบัติ","ธรรม","ค่ะ"]
        ftext = ""
        for i in range(len(text)):
                ftext += " ../thaivoices/thwords/" + text[i] + ".mp3"

        os.system('mpg123 -q -f 2000 ' + ftext)
        del text
        del ftext
        gc.collect()
        # text = "Welcome to Anatta Project, press button to play with Dhamma"
        # speak(text)
        button_press = 0
        once = True
        with Leds() as leds:

                # print('RGB: Solid GREEN for 1 second')
                # leds.update(Leds.rgb_on(Color.GREEN))
                # time.sleep(1)

                # print('RGB: Solid YELLOW for 1 second')
                # leds.update(Leds.rgb_on(Color.YELLOW))
                # time.sleep(1)

                # print('RGB: Solid BLUE for 1 second')
                # leds.update(Leds.rgb_on(Color.BLUE))
                # time.sleep(1)

                # print('RGB: Solid PURPLE for 1 second')
                # leds.update(Leds.rgb_on(Color.PURPLE))
                # time.sleep(1)

                # print('RGB: Solid CYAN for 1 second')
                # leds.update(Leds.rgb_on(Color.CYAN))
                # time.sleep(1)

                # print('RGB: Solid WHITE for 1 second')
                # leds.update(Leds.rgb_on(Color.WHITE))
                # time.sleep(1)

                # print('RGB: Solid BLUE for 1 second')
                # leds.update(Leds.rgb_on(Color.BLUE))
                # time.sleep(1)

                # print('Set blink pattern: period=500ms (2Hz)')
                # leds.pattern = Pattern.blink(500)

                # print('RGB: Blink GREEN for 5 seconds')
                # leds.update(Leds.rgb_pattern(Color.GREEN))
                # time.sleep(5)

                leds.update(Leds.rgb_on(Color.YELLOW))

                with Board() as board:
                        while True:
                                if button_press == 0:
                                        proc = subprocess.Popen(["python3", "sati.py"])
                                board.button.wait_for_press()
                                # board.led.state = Led.ON
                                button_press += 1
                                board.button.wait_for_release()
                                # board.led.state = Led.OFF                                    
                                if button_press == 1: 
                                        proc.kill()
                                        if have_internet():
                                                text = ""
                                                
                                                today = dt.datetime.now() 
                                                # text = ["วันนี้","วัน","weekday/%w","ที่","59/%d","เดือน","month/%m","เวลา","59/%H","นาฬิกา","59/%M","นาที"]
                                                t = "วันนี้,วัน,weekday/%w,ที่,59/%d,เดือน,month/%m,เวลา,59/%H,นาฬิกา,59/%M,นาที"
                                                t = t.replace("%w",today.strftime('%w'))
                                                t = t.replace("%d",today.strftime('%d'))
                                                t = t.replace("%m",today.strftime('%m'))
                                                t = t.replace("%H",today.strftime('%H'))
                                                t = t.replace("%M",today.strftime('%M'))
                                                text = t.split(',')
                                                stext = ""
                                                for i in range(len(text)):
                                                        stext += " ../thaivoices/thwords/" + text[i] + ".mp3"
                                                os.system("mpg123 -q -f 2100 "+stext)
                                        else:
                                                text = "../thaivoices/nointernet.mp3 "
                                                os.system("mpg123 -q -f 2100 "+text)

                                        leds.update(Leds.rgb_on(Color.WHITE))
                                        
                                        y = list(str(holyday))
                                        yy = y[2]+y[3]+y[4]+y[5]
                                        mm = y[6]+y[7]
                                        dd = y[8]+y[9]

                                        x = dt.datetime(int(yy), int(mm), int(dd))
                                        # z = x.strftime("%B %A %d")
                                        t = "วันพระ,หน้า,คือ,วัน,weekday/%w,ที่,59/%d,เดือน,month/%m"
                                        t = t.replace("%w",x.strftime('%w'))
                                        t = t.replace("%d",x.strftime('%d'))
                                        t = t.replace("%m",x.strftime('%m'))
                                        text = t.split(',')
                                        stext = ""
                                        for i in range(len(text)):
                                                stext += " ../thaivoices/thwords/" + text[i] + ".mp3" 
                                        os.system("mpg123 -q -f 2100 "+stext) 
                                        os.system("mpg123 -q -f 2100 "+bdaytext) 

                                        if have_internet() and once:
                                                w = ipInfo()
                                                text = 'Country '+w['sys']['country']+'. City '+w['name']+'. Temperature is '+str(w['main']['temp'])+'. Humidity is '+str(w['main']['humidity'])+'. The weather is '+w['weather'][0]['description']
                                                # text += ' Sunrise '+str(w['sys']['sunrise'])+' Sunset '+str(w['sys']['sunset'])
                                                # print(text)
                                                speak(text)
                                                once = False
  
                                elif button_press == 2:
                                        if have_internet():
                                                text = "Listen to Tibetan Buddhist internet radio"
                                                speak(text)
                                                leds.update(Leds.rgb_on(Color.WHITE))
                                                proc = subprocess.Popen(["mpg123","-f","2100","-q","http://199.180.72.2:9097/lamrim"])
                                                # proc = subprocess.Popen(["mpg123","-f","2100","-q",article_link])
                                        else:
                                                leds.update(Leds.rgb_on(Color.YELLOW))
                                                text = " ../thaivoices/words/buddhadham.mp3"
                                                os.system("mpg123 -q -f 2100 "+text) 
                                                proc = subprocess.Popen(["mpg123","-f","2100","-q","-Z","--list","THbuddhadham.txt"]) 
                                elif button_press == 3:
                                        proc.kill()
                                        leds.update(Leds.rgb_on(Color.YELLOW))
                                        text = " ../thaivoices/words/chanting.mp3"
                                        os.system("mpg123 -q -f 2100 "+text) 
                                        proc = subprocess.Popen(["mpg123","-f","2100","-q","-Z","--list","THchanting.txt"]) 
                                elif button_press == 4:
                                        proc.kill()
                                        leds.update(Leds.rgb_on(Color.RED))
                                        text = " ../thaivoices/words/sutra.mp3" #+ " ../datath/sutta/moggallana.mp3"
                                        os.system("mpg123 -q -f 2100 "+text) 
                                        # t1 = time.time()
                                        # board.led.state = Led.ON
                                        # leds.update(Leds.rgb_on(Color.WHITE))
                                        # board.button.wait_for_press()
                                        # t2 = time.time()
                                        # if t2-t1 < 4:
                                        #         text = " ../datath/sutta/moggallana.mp3"
                                        #         os.system("mpg123 -q -f 2100 "+text)
                                        # leds.update(Leds.rgb_on(Color.YELLOW))
                                        proc = subprocess.Popen(["mpg123","-f","2100","-q","-Z","--list","sutra.txt"]) 
                                elif button_press == 5:
                                        proc.kill()
                                        leds.update(Leds.rgb_on(Color.PURPLE))
                                        text = " ../thaivoices/words/dhamma.mp3"
                                        os.system("mpg123 -q -f 2100 "+text) 
                                        proc = subprocess.Popen(["mpg123","-f","2100","-q","-Z","--list","THdhamma.txt"])
                                elif button_press == 6:
                                        proc.kill()
                                        leds.update(Leds.rgb_on(Color.GREEN))
                                        text = "../thaivoices/words/dhamma.mp3 ../thaivoices/words/buddhadasa.mp3"
                                        os.system("mpg123 -q -f 2100 "+text) 
                                        proc = subprocess.Popen(["mpg123","-f","2100","-q","-Z","--list","THbuddhadasa.txt"])
                                elif button_press == 7:
                                        proc.kill()
                                        leds.update(Leds.rgb_on(Color.GREEN))
                                        text = "../thaivoices/words/dhamma.mp3 ../thaivoices/words/payutto.mp3"
                                        os.system("mpg123 -q -f 2100 "+text) 
                                        proc = subprocess.Popen(["mpg123","-f","2100","-q","-Z","--list","THpayutto.txt"])
                                elif button_press == 8:
                                        proc.kill()
                                        leds.update(Leds.rgb_on(Color.RED))
                                        proc = subprocess.Popen(["mpg123","-d","3","-f","1000","-q","--loop","-1","../thaivoices/buddho.mp3"])
                                elif button_press == 9:
                                        proc.kill()
                                        text = "../thaivoices/meditation.mp3"
                                        os.system("mpg123 -q -f 2100 "+text)
                                        leds.update(Leds.rgb_on(Color.BLUE))
                                        # board.led.state = Led.ON
                                        proc = subprocess.Popen(["mpg123","-f","2100","-q","--loop","-1","../dataen/bell15min.mp3"])
                                
                                else:  
                                        os.system("sudo killall mpg123")
                                        button_press = 0
                                        text = "Hello Press button within 3 sec For Exit"
                                        speak(text)
                                        t1 = time.time()
                                        board.button.wait_for_press()
                                        t2 = time.time()
                                        board.led.state = Led.OFF
                                        if t2-t1 < 4:
                                                os.system("sudo killall mpg123")
                                                speak("goodbye, have a nice day.")
                                                break
                                        else:
                                                text = " ../thaivoices/sati.mp3"
                                                os.system("mpg123 -q -f 2100 " + text) 
                                                
if __name__ == '__main__':
        main()

# mpg123 -f 2100 the maximum value of the amplitude is 100% which coressponds to 32768, i use this when i want to run with crontab