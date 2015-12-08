#!/bin/python

import autodiscover
from tvcontrol import Remote

myip = autodiscover.get_local_ip_for_target('8.8.8.8', 53)
tvip = autodiscover.autodiscover_tv_ip(myip)
mymac = '11:11:11:11:11:11'.replace(":", "-")

with Remote(myip, mymac, tvip) as remote:
	remote.sendKey("KEY_TV")
	