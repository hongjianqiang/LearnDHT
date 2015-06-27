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
	def __init__(self, nid):
		self.nid = nid.decode('hex')
		self.ufd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.ufd.settimeout(3)


	def close(self):
		self.ufd.close()

	
	def random_id(self):
		hash = sha1()
		hash.update(os.urandom(20))
		return hash.digest()


	def Int2Ip(self, int_ip):
		return socket.inet_ntoa(struct.pack('I',socket.htonl(int_ip)))


	def send_krpc(self, msg, address):
		self.ufd.sendto(bencode(msg), address)


	def ping(self, address):
		tid = os.urandom(4)		# token id
		#print tid.encode('hex')
		msg = dict(
			t = tid,
			y = "q",
			q = "ping",
			a = dict(id = self.nid)
		)
		self.send_krpc(msg, address)


	def find_node(self, address, target=None):
		target = target.decode('hex') if target else self.nid
		tid = os.urandom(4)		# token id
		#print tid.encode('hex')
		msg = dict(
			t = tid,
			y = "q",
			q = "find_node",
			a = dict(id = self.nid, target = target)
		)
		self.send_krpc(msg, address)


	def get_peers(self, address, info_hash=None):
		info_hash = info_hash.decode('hex') if info_hash else self.nid
		tid = os.urandom(4)		# token id
		#print tid.encode('hex')
		msg = dict(
			t = tid,
			y = "q",
			q = "get_peers",
			a = dict(id = self.nid, info_hash = info_hash)
		)
		self.send_krpc(msg, address)


	# implied_port字段0表示和DHT共用一个端口下载种子文件，1表示使用后面的port字段端口下载种子文件。
	def announce_peer(self, address, info_hash=None, token=None, implied_port=1, port=1234):
		info_hash = info_hash.decode('hex') if info_hash else self.nid
		token = token.decode('hex')
		tid = os.urandom(4) 	# token id
		#print tid.encode('hex')
		msg = dict(
			t = tid,
			y = "q",
			q = "announce_peer",
			a = dict(id = self.nid, implied_port = implied_port, info_hash = info_hash, port = port, token = token)
		)
		self.send_krpc(msg, address)


	def recv_krpc(self):
		try:
			(data, address) = self.ufd.recvfrom(1024)
		except Exception, e:
			self.close()
			print "ErrorInfo:", e
			exit()

		msg = bdecode(data)

		# 把v值转化为16进制，表示客户端的版本号
		if 'v' in msg.keys():
			msg["v"] = msg["v"].encode('hex')

		if 't' in msg.keys():
			msg["t"] = msg["t"].encode('hex')

		if msg["y"]=="r":
			# 把IP和端口解析出来
			if msg.has_key("ip"):
				int_ip = int( msg["ip"].encode('hex')[0:8], 16)
				int_port = int( msg["ip"].encode('hex')[8:12], 16)
				ip = self.Int2Ip(int_ip)
				addr =  "%s:%d" % (ip, int_port)
				msg["ip"] = addr

			# 把nodes值解析出来
			if 'nodes' in msg["r"].keys():
				nodes = msg["r"]["nodes"].encode('hex')
				node = ""
				n = len(nodes)/52 # 返回的节点数量，一般 n=8
				for i in range(n):
					node_id = nodes[0+52*i:40+52*i]		# 分割出node id，以16进制表示的
					node_ip = nodes[40+52*i:48+52*i]	# 分割出node ip，以16进制表示的
					node_port = nodes[48+52*i:52+52*i]	# 分割出node port，以16进制表示的

					int_node_ip = int(node_ip, 16)	# 把node ip，以10进制表示
					node_ip = self.Int2Ip(int_node_ip)
					node_port = int(node_port, 16)	# 把node port，以10进制表示
					tmp = "%s:%s:%d, " % (node_id, node_ip, node_port)
					node = node + tmp
				msg["r"]["nodes"] = node[:-2]

			# 把id值解析出来
			if 'id' in msg["r"].keys():
				msg["r"]["id"] = msg["r"]["id"].encode('hex')

			# 把values值解析出来
			if 'values' in msg["r"].keys():
				for i in range(len(msg['r']['values'])):
					msg['r']['values'][i] = msg['r']['values'][i].encode('hex')
					int_peer_ip = int(msg['r']['values'][i][0:8], 16)	# 分割出peer ip，并以10进制表示的
					int_peer_port = int(msg['r']['values'][i][8:12], 16)	# 分割出peer port，并以10进制表示的
					peer_ip = self.Int2Ip(int_peer_ip)	# 把peer ip表示为 xxx.xxx.xxx.xxx 格式
					msg['r']['values'][i] = "%s:%d" % (peer_ip, int_peer_port)	# 最终 values 表示为 ‘values’:['xxx.xxx.xxx.xxx:xx','xxx.xxx.xxx.xxx:xx']

			# 把token值转化为16进制
			if 'token' in msg["r"].keys():
				msg["r"]["token"] = msg["r"]["token"].encode('hex')

		if msg["y"]=="q":
			if 'id' in msg["a"].keys():
				msg["a"]["id"] = msg["a"]["id"].encode('hex')

			if 'target' in msg["a"].keys():
				msg["a"]["target"] = msg["a"]["target"].encode('hex')

		return msg


# 生成一个随机的nodeID，类似 0ED8DA508F923689C578B494CDA3C94EE3000EE1
def randomID():
	hash = sha1()
	hash.update(os.urandom(20))
	return hash.digest().encode('hex')


if __name__ == "__main__":
	nodeID = "30aca5312a73e74abfdf422ba701064c73a75d63"
	#nodeID = "c09bd1affc4e9b18e176d9818144a4be2f4e8be5"
	#nodeID = randomID()

	print "My nodeID : %s\n" % nodeID
	dht = DHT(nodeID)

	dht.ping(("127.0.0.1", 6881))
	#dht.find_node(("127.0.0.1", 6881), "0ED8DA508F923689C578B494CDA3C94EE3000EE1")
	#dht.get_peers(("127.0.0.1", 6881), "0ED8DA508F923689C578B494CDA3C94EE3000EE1")
	#dht.announce_peer(("127.0.0.1", 6881), "0ED8DA508F923689C578B494CDA3C94EE3000EE1", "88af04c226e5a78add929dc5ee9e812510fae151", 0, 1234)

	sleep(1)
	print dht.recv_krpc()
	dht.close()

	raw_input()
