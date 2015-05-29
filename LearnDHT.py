#!/usr/bin/env python
# -*- coding: utf-8 -*-
# LearnDHT.py

import os
import socket
import struct
from bencode import bencode, bdecode
from hashlib import sha1
from random import randint
from time import sleep

class DHT(object):
	"""docstring for LearnDHT"""
	def __init__(self):
		self.ufd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def close(self):
		self.ufd.close()
	
	def random_id(self):
		hash = sha1()
		hash.update(os.urandom(20))
		return hash.digest()

	def Int2Ip(self, Int):
		return self.ufd.inet_ntoa(struct.pack("!I",ip))

	def send_krpc(self, msg, address):
		self.ufd.sendto(bencode(msg), address)

	def ping(self, address, nid=None):
		nid = nid if nid else self.random_id()
		# token id
		tid = os.urandom(4)
		msg = dict(
			t = tid,
			y = "q",
			q = "ping",
			a = dict(id = nid)
		)
		self.send_krpc(msg, address)

	def recv_krpc(self):
		(data, address) = self.ufd.recvfrom(1024)
		msg = bdecode(data)
		# 把IP和端口解析出来
		int_ip = int( msg["ip"].encode('hex')[0:8], 16)
		int_port = int( msg["ip"].encode('hex')[8:12], 16)
		ip = socket.inet_ntoa(struct.pack('I',socket.htonl(int_ip)))
		addr =  "%s:%d" % (ip, int_port)
		msg["ip"] = addr
		msg["r"]["id"] = msg["r"]["id"].encode('hex')
		msg["t"] = msg["t"].encode('hex')
		return msg

if __name__ == "__main__":
	dht = DHT()
	nid = dht.random_id()
	# dht.ping(("127.0.0.1", 6881), nid)
	# dht.ping(("router.bittorrent.com", 6881), nid)
	# dht.ping(("dht.transmissionbt.com", 6881), nid)
	# dht.ping(("router.utorrent.com", 6881), nid)
	dht.ping(("router.bittorrent.com", 6881), nid)
	sleep(1)
	print dht.recv_krpc()
	dht.close()

	raw_input()
