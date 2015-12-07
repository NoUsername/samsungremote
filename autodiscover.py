import subprocess
import re
import logging
import socket

def autodiscover_ip():
	try:
		output = subprocess.check_output('gssdp-discover --timeout=3 | grep Samsung', shell=True)
		for line in output.split('\n'):
			if line.find('Location') >= 0:
				m = re.search('http://([^:/]+)[:/]', line)
				if m != None:
					return m.group(1)
	except:
		logging.info('could not autodiscover samsung tv (possible reasons: not online, gupnp-tools not installed)')

def get_local_ip_for_target(targethost, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		s.connect((targethost,port))
		return s.getsockname()[0]
	finally:
		s.close()


if __name__=='__main__':
	print('discovering...')
	print('found %s'%autodiscover_ip())