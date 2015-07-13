#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RTable.py

import os

class RTable(object):
	"""docstring for RTable"""
	def __init__(self, nid, K):
		self.nid = nid
		self.K = K
		self.buckets = dict()

		for i in xrange(0,len(self.nid)*4+1):
			self.buckets[i] = list()

		self.buckets[0].append(self.nid)

	
	# 追加nid到K桶
	def append(self, nid):
		distance = int(self.nid, 16) ^ int(nid, 16)
		num = len(bin(distance)) - 2	# 查找对应的K桶号（范围）
		if len(self.buckets[num]) < self.K:
			if nid not in self.buckets[num]:
				self.buckets[num].append(nid)

	# 返回与目标node ID或infohash的最近K个node.
	def find_close_nodes(self, target):
		distance = int(self.nid, 16) ^ int(nid, 16)
		num = len(bin(distance)) - 2 -1
		return self.buckets[num]
		
	# 显示K桶的状态
	def show(self):
		print self.buckets


if __name__ == '__main__':
	K = 2
	#nid = os.urandom(1).encode('hex')
	nid = '3e'
	R = RTable(nid, K)
	for i in xrange(0,1000):
		nid = os.urandom(1).encode('hex')
		R.append(nid)
	R.show()
	print R.find_close_nodes('ea')

	raw_input()
