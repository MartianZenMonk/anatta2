THANK YOU VERY MUCH TO MR. Peter Malkin FOR GIVING ME THE VOICEKIT AND CORAL DEV BOARD


https://aiyprojects.withgoogle.com/voice/


use

git clone https://github.com/MartianZenMonk/anatta.git

- then you can use git pull to update the content after reboot if you like :)


You may have to install the following packages
- sudo pip3 install pyttsx3
- sudo apt  install espeak  (and espeak-ng if you like )
- sudo apt  install mpg123


You may use crontab -e for
- @reboot cd anatta/voicekit && sleep 60 && python3 shutdown_button.py
- @reboot cd anatta/voicekit && sleep 60 && python3 sayhi.py
- # play with button
- @reboot cd anatta/voicekit && sleep 90 && python3 anatta_button.py 



