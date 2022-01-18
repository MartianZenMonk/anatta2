THANK YOU VERY MUCH TO MR. Peter Malkin FOR GIVING ME THE VOICEKIT AND CORAL DEV BOARD ( MONKS PROPERTY )


THANK YOU VERY MUCH TO MR SUTHEE @ https://www.techtalkthai.com/ FOR GIVING THE ASUS ZENBOOK DUO LAPTOP ( MONKS PROPERTY )


Anatta Meditation Voice For rasberry pi os / ubuntu , and may good for pi zero 2 w too


git clone https://github.com/MartianZenMonk/anatta2

- then you can use git pull for updating

You may have to install the following packages
- sudo apt update
- pip3 install sounddevice
- pip3 install vosk (for pi zero, apt-get install libgfortran3 )
- pip3 install opencv-python
- opencv for pi zero
- sudo apt-get install python3-opencv
- sudo nano /etc/dphys-swapfile #CONF_SWAPSIZE=100 , CONF_SWAPSIZE=2048
- or https://qengineering.eu/install-opencv-lite-on-raspberry-pi.html , https://pimylifeup.com/raspberry-pi-webcam-server/
- ...
- pip3 install pyttsx3
- pip3 install pydub
- sudo apt  install espeak  (and espeak-ng if you like )
- sudo apt  install mpg123
- sudo apt  install vorbis-tools (ogg123 - if you want to use ogg)

- sudo apt install nginx
- sudo nano /etc/nginx/sites-enabled/default , change root documents to /home/pi/anatta2
- unzip  tripitakaofflineV07.zip
- sudo systemctl restart nginx
- for other languages please visit https://github.com/suttacentral or https://github.com/digitalpalireader/digitalpalireader
- python3 -m pip install -U yt-dlp , for pi zero to fix "Illegal instruction" ,  pip3 uninstall pycryptodomex ( use yt-dlp to play youtube playlist, can use youtube-dl too)

For Virtualbox + VirtualBox Extension Pack
- https://www.virtualbox.org/wiki/Downloads
- https://ubuntu-mate.org/download/

For offline Thai voice recognition
- https://github.com/mozilla/DeepSpeech-examples/tree/r0.9/mic_vad_streaming
- https://itml.cl.indiana.edu/models/th/

How to run
- copy folder m_tapaguno to m_yourname
- cd m_yourname
- python3 anatta.py
- note. need webcam for motion detect for terminating some functions , may test the webcam first by using python3 mdetect.py

How to use ( for example )
- say "english chanting" to play english Chanting
- say "thai chanting" to play Thai chanting
- say "play dhamma" to listen to the Thai dhamma
- say "testing one" for 1 hr walking practice
- say "testing three" for 30 minutes walking and 30 minutes sitting practice
- say "chinese walking", or "japanese walking", or "korean walking" or "english walking" for walking practice
- note. walking pracetice is a good meditation pracetice, there are these five benefits of walking meditation https://suttacentral.net/an5.29/en/bodhi
- but it's better to modified the code, design your own meditation style. แต่เป้าหมายจริงๆ คือ อยากให้ แก้ไขโค้ดเอง อยากให้ออกแบบรูปแบบการภาวนาแบบที่ชอบเอง


Let's be meditation tools maker and join our facebook group : https://free.facebook.com/groups/393633318920656/

![templex04](https://user-images.githubusercontent.com/79086623/146861353-9088641e-78f4-4b87-86ee-827bcb0939ac.png)

Meditation tool  สำหรับ ผู้เริ่มต้นฝึกปฏิบัติ จะเน้นช่วยให้เกิดฉันทะ อยากฝึกปฏิบัติอย่างต่อเนื่อง และ ช่วยเน้นการฝึก เจริญ สติ พระท่านว่า สติ ยิ่งมีมากยิ่งดี เพราะเป็น ตัวช่วยให้เกิด สัมมาสมาธิ ได้ง่าย และ ช่วยในการทำวิปัสสนา เป้าหมายการภาวนาของมือใหม่ในเบื้องต้น คือ มีสติไว ใจสงบ

![s24](https://user-images.githubusercontent.com/79086623/146866133-8e84faee-e379-41f2-a1ee-b352e87e6a36.png)
