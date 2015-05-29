#!/usr/bin/env python
# -*- coding: utf-8 -*-

'a udp server example which send time to client.'

import socket
from bencode import bencode, bdecode

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 绑定端口:
s.bind(('127.0.0.1', 6881))
print 'Bind UDP on 6881...'
while True:
    # 接收数据:
    data, addr = s.recvfrom(1024)
    print 'Received from %s:%s.' % addr
    print '%s' % data
    respon = '{"t":"aa", "y":"r", "r": {"id":"mnopqrstuvwxyz123456"}}'
    s.sendto('%s' % bencode(respon), addr)

raw_input()
