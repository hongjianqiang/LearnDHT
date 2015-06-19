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
		self.ufd.settimeout(3)


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


	def find_node(self, address, nid=None, target=None):
		nid = nid if nid else self.random_id()
		target = target.decode('hex') if target else nid
		# token id
		tid = os.urandom(4)
		msg = dict(
			t = tid,
			y = "q",
			q = "find_node",
			a = dict(id = nid, target = target)
		)
		self.send_krpc(msg, address)


	def get_peers(self, address, nid=None, info_hash=None):
		nid = nid if nid else self.random_id()
		info_hash = info_hash.decode('hex') if info_hash else self.random_id()
		# token id
		tid = os.urandom(4)
		msg = dict(
			t = tid,
			y = "q",
			q = "get_peers",
			a = dict(id = nid, info_hash = info_hash)
		)
		self.send_krpc(msg, address)


	def recv_krpc(self):
		try:
			(data, address) = self.ufd.recvfrom(1024)
		except Exception, e:
			self.close()
			print "ErrorInfo:", e
			exit()
		# (data, address) = self.ufd.recvfrom(1024)
		msg = bdecode(data)
		# 把节点 id 和 token id 用 16进制表示
		msg["r"]["id"] = msg["r"]["id"].encode('hex')
		msg["t"] = msg["t"].encode('hex')
		# 把IP和端口解析出来
		if msg.has_key("ip"):
			int_ip = int( msg["ip"].encode('hex')[0:8], 16)
			int_port = int( msg["ip"].encode('hex')[8:12], 16)
			ip = socket.inet_ntoa(struct.pack('I',socket.htonl(int_ip)))
			addr =  "%s:%d" % (ip, int_port)
			msg["ip"] = addr
		# 把nodes值解析出来
		if 'nodes' in msg["r"].keys():
			nodes = msg["r"]["nodes"].encode('hex')
			node = ""
			for i in range(8):
				node_id = nodes[0+52*i:40+52*i]		# node id
				node_ip = nodes[40+52*i:48+52*i]	# node ip
				node_port = nodes[48+52*i:52+52*i]	# node port

				node_ip = socket.inet_ntoa(struct.pack('I',socket.htonl(int(node_ip, 16))))
				node_port = int(node_port, 16)
				tmp = "%s:%s:%d, " % (node_id, node_ip, node_port)
				node = node + tmp
			msg["r"]["nodes"] = node[:-2]
		
		return msg



if __name__ == "__main__":
	dht = DHT()
	nid = dht.random_id()
	# dht.ping(("router.bittorrent.com", 6881), nid)
	# dht.ping(("dht.transmissionbt.com", 6881), nid)
	# dht.ping(("router.utorrent.com", 6881), nid)

	# dht.ping(("router.bittorrent.com", 6881), nid)
	# dht.find_node(("router.bittorrent.com", 6881), nid, "32f54e697351ff4aec29cdbaabf2fbe3467cc267")
	# dht.get_peers(("router.bittorrent.com", 6881), nid, "32f54e697351ff4aec29cdbaabf2fbe3467cc267")

	dht.ping(("127.0.0.1", 47979), nid)
	#dht.find_node(("127.0.0.1", 47979), nid, "32f54e697351ff4aec29cdbaabf2fbe3467cc267")

	sleep(1)
	print dht.recv_krpc()
	dht.close()

	raw_input()
