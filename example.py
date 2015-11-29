#!/bin/python

import autodiscover
from tvcontrol import Remote

tvip = autodiscover.autodiscover_ip()
data = autodiscover.get_local_ip_for_target(tvip, Remote.TV_PORT)
myip = data
mymac = '11:11:11:11:11:11'.replace(":", "-")

with Remote(myip, mymac, tvip) as remote:
	remote.sendKey("KEY_TV")
	