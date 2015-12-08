#!/bin/python

# Remote control via keyboard from a shell, comfortable navigation e.g. when surfing
# with your laptop on the couch and watching tv in the background

import autodiscover
from tvcontrol import Remote
import curses

# simple hack to get the local ip. assumes that the network-IF which is used
#  to connect to the internet is the same you use for communicating with your tv
#  also assumes you have internet ;)
myip = autodiscover.get_local_ip_for_target('8.8.8.8', '53')
tvip = autodiscover.autodiscover_tv_ip(myip)
mymac = '11:11:11:11:11:11'.replace(":", "-")

mapping = {
	'10':'KEY_ENTER',
	'65':'KEY_UP',
	'66':'KEY_DOWN',
	'67':'KEY_RIGHT',
	'68':'KEY_LEFT',
	'43':'KEY_VOLUP',
	'45':'KEY_VOLDOWN',
	'116':'KEY_TOOLS', # t -> tools
	'112':'KEY_POWEROFF', # P -> poweroff
	'120':'KEY_EXIT', # x -> exit
	'127':'KEY_RETURN', # <- -> return
	'105':'KEY_INFO', # i -> info
	'103':'KEY_GUIDE', # g -> guide
	'104':'KEY_HDMI1' # h -> hdmi
}

stdscr = curses.initscr()
try:
	lastKey = None
	key = None
	with Remote(myip, mymac, tvip) as remote:
		while key != 113:
			#curses.flushinp()
			lastKey = key
			key = stdscr.getch()
			print("got %s %s"%(str(key), key))
			rkey = mapping.get(str(key))
			if rkey != None:
				print("key %s"%rkey)
				remote.sendKey(rkey)
			elif key > ord('0') and key <= ord('9'):
				print('sending: KEY_%s'%chr(key))
				remote.sendKey('KEY_%s'%chr(key))
finally:
	import time
	print('exiting')
	time.sleep(1)
	curses.endwin()
	