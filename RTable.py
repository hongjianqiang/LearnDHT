#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RTable.py

import os

class RTable(object):
	"""docstring for RTable"""
	def __init__(self, node, K):
		self.node		= node
		self.K			= K
		self.buckets	= dict() 

		# 初始化，生成空K-bucket桶
		for i in xrange(0,len(self.node[2])*4):
			self.buckets[i] = list()

		self.buckets[0].append(self.node)


	# 追加nid到K桶
	def append(self, node):
		distance = int(self.node[2], 16) ^ int(node[2], 16)
		num = len(bin(distance)) - 3	# 查找对应的K桶号（范围）
		
		flag = 'ignore'
		if 0 == len(self.buckets[num]):
			flag = 'insert'
		if len(self.buckets[num]) < self.K:
			for index, nodes in self.buckets.items():
				for n in nodes:
					# 过滤掉与K-Buckets里 IP 相同的node
					if n[0] == node[0]:
						flag = 'ignore'
						break
					else:
						flag = 'insert'
					# 过滤掉与K-Buckets里 ID 相同的node
					if n[2] == node[2]:	
						flag = 'ignore'
						break
					else:
						flag = 'insert'

		if 'insert' == flag:
			self.buckets[num].append(node)


	# 返回与目标node ID或infohash的最近K个node.
	def find_close_nodes(self, target):
		distance = int(self.node[2], 16) ^ int(target, 16)
		num = len(bin(distance)) - 3
		print "\nbuckets[%d]:" % num,
		return self.buckets[num]

	def show(self):
		print self.buckets



if __name__ == '__main__':
	K		= 8
	#nid 	= os.urandom(20).encode('hex')
	#node	= ('127.0.0.1',6881,nid)
	#node	= ('127.0.0.1',6881,'46011263f1bbcec88859909aa21a54185c224c7a')
	#node	= ('127.0.0.1',6881,'4d0393b57e601e99f1bce87e56030b2688dfc935')
	#node	= ('127.0.0.1',6881,'4d9120e8e7b132a0390f0fa453ca24a53874fd9a')
	node	= ('127.0.0.1',6881,'4da80660a0df662932e39b21df84bc7bbc895f41')

	R = RTable(node, K)
	for i in xrange(0,1000):
		nid = os.urandom(20).encode('hex')
		R.append(('127.0.0.%d' % i, 6881, nid))
	R.show()

	#print R.find_close_nodes('dcba')
	print R.find_close_nodes('4da6136d0d3145f4ba33d664fde40a36f8c12437')

	raw_input()