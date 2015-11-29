#!  /usr/bin/python
#	Author: Paul Klingelhuber
#   Original Author: Asif Iqbal

import socket
import base64
import time, datetime

# Function to send keys
def sendKey(skey, dataSock, appstring):
	messagepart3 = chr(0x00) + chr(0x00) + chr(0x00) + \
		chr(len(base64.b64encode(skey))) + chr(0x00) + base64.b64encode(skey);
	part3 = chr(0x00) + chr(len(appstring)) + chr(0x00) + \
		appstring + chr(len(messagepart3)) + chr(0x00) + messagepart3
	dataSock.send(part3);

appstring = "linuxe..iapp.samsung"
#Might need changing to match your TV type
tvappstring = "iphone.UE55C8000.iapp.samsung"
#What gets reported when it asks for permission
remotename = "Python Samsung Remote"

class Remote(object):

	TV_PORT = 55000

	def __init__(self, myip, mymac, tvip):
		self.myip = myip
		self.tvip = tvip
		self.mymac = mymac
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((tvip, Remote.TV_PORT))
		self.__handshake()

	def __handshake(self):
		# First configure the connection
		ipencoded = base64.b64encode(self.myip)
		macencoded = base64.b64encode(self.mymac)
		messagepart1 = chr(0x64) + chr(0x00) + chr(len(ipencoded)) \
		+ chr(0x00) + ipencoded + chr(len(macencoded)) + chr(0x00) \
		+ macencoded + chr(len(base64.b64encode(remotename))) + chr(0x00) \
		+ base64.b64encode(remotename)

		part1 = chr(0x00) + chr(len(appstring)) + chr(0x00) + appstring \
		+ chr(len(messagepart1)) + chr(0x00) + messagepart1
		self.sock.send(part1)

		messagepart2 = chr(0xc8) + chr(0x00)
		part2 = chr(0x00) + chr(len(appstring)) + chr(0x00) + appstring \
		+ chr(len(messagepart2)) + chr(0x00) + messagepart2
		self.sock.send(part2)

	def sendKey(self, key):
		sendKey(key, self.sock, tvappstring)
		time.sleep(0.3)

	def __enter__(self):
		return self

	def __exit__(self, type, value, tb):
		self.close()

	def close(self):
		if self.sock != None:
			self.sock.close()
			self.sock = None



# Key Reference
# Normal remote keys
 #KEY_0
 #KEY_1
 #KEY_2
 #KEY_3
 #KEY_4
 #KEY_5
 #KEY_6
 #KEY_7
 #KEY_8
 #KEY_9
 #KEY_UP
 #KEY_DOWN
 #KEY_LEFT
 #KEY_RIGHT
 #KEY_MENU
 #KEY_PRECH
 #KEY_GUIDE
 #KEY_INFO
 #KEY_RETURN
 #KEY_CH_LIST
 #KEY_EXIT
 #KEY_ENTER
 #KEY_SOURCE
 #KEY_AD #KEY_PLAY
 #KEY_PAUSE
 #KEY_MUTE
 #KEY_PICTURE_SIZE
 #KEY_VOLUP
 #KEY_VOLDOWN
 #KEY_TOOLS
 #KEY_POWEROFF
 #KEY_CHUP
 #KEY_CHDOWN
 #KEY_CONTENTS
 #KEY_W_LINK #Media P
 #KEY_RSS #Internet
 #KEY_MTS #Dual
 #KEY_CAPTION #Subt
 #KEY_REWIND
 #KEY_FF
 #KEY_REC
 #KEY_STOP
# Bonus buttons not on the normal remote:
 #KEY_TV
#Don't work/wrong codes:
 #KEY_CONTENT
 #KEY_INTERNET
 #KEY_PC
 #KEY_HDMI1
 #KEY_OFF
 #KEY_POWER
 #KEY_STANDBY
 #KEY_DUAL
 #KEY_SUBT
 #KEY_CHANUP
 #KEY_CHAN_UP
 #KEY_PROGUP
 #KEY_PROG_UP

