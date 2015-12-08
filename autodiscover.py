import logging
import socket
from six.moves import http_client
from six.moves.urllib import parse
from six import BytesIO
from six import b, u


class SSDPResponse(object):
    class _FakeSocket(BytesIO):
        def makefile(self, *args, **kw):
            return self
    def __init__(self, response):
        r = http_client.HTTPResponse(self._FakeSocket(response))
        r.begin()
        self.location = r.getheader("location")
        self.usn = r.getheader("usn")
        self.st = r.getheader("st")
        self.cache = r.getheader("cache-control").split("=")[1]
    def __repr__(self):
        return "<SSDPResponse({location}, {st}, {usn})>".format(**self.__dict__)

def discover(service, localIp, timeout=2, retries=1):
    group = ("239.255.255.250", 1900)
    message = "\r\n".join([
        'M-SEARCH * HTTP/1.1',
        'HOST: {0}:{1}',
        'MAN: "ssdp:discover"',
        'ST: {st}','MX: 3','',''])
    socket.setdefaulttimeout(timeout)
    responses = {}
    for _ in range(retries):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # the next line is only required on windows to make udp multicast responses work!
        sock.bind((localIp, 0))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.sendto(b(message.format(*group, st=service)), group)
        while True:
            try:
                response = SSDPResponse(sock.recv(1024))
                responses[response.location] = response
            except socket.timeout:
                break
    return responses.values()

def autodiscover_tv_ip(localIp):
	results = discover('ssdp:all', localIp)
	for result in results:
		if result.location.lower().find('remotecontrolreceiver') > -1:
			return parse.urlparse(result.location).hostname
	raise 'no ip for samsung tv found'

def get_local_ip_for_target(targethost, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		s.connect((targethost,port))
		return s.getsockname()[0]
	finally:
		s.close()


if __name__=='__main__':
    print('trying to autodiscover a samsung tv ip on your network')
    myip = get_local_ip_for_target('8.8.8.8', 53)
    tvip = autodiscover_tv_ip(myip)
    print('found tv @ ip ' + tvip)