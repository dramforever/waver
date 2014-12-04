#coding=utf-8
print('Loading Waver (by xmcp)...')

import sys
if sys.version[0]=='2':
    range=xrange
    input=raw_input

import libwaver as waver
import os
from time import sleep

#open file
if len(sys.argv)==2:
    proj=sys.argv[1]
    print('Project loaded: '+proj)
else:
    proj=input('Project Name:')
try:
    with open('projects/%s.txt'%proj,'r') as f:
        lines=f.read().split('\n')
except Exception as e:
    print('[ERROR]')
    print(e)
    print('While reading project.')
    sys.exit(-2048)
print('[BEGIN]')

#find start
try:
    lines=lines[lines.index('[START]')+1:]
except (ValueError,IndexError):
    pass
else:
    print('[START] Trigger Found.')

#process!
f=waver.wavefile('projects/%s.wav'%proj)
try:
    for line in lines:
        if not line:
            continue
        if line[0]=='#':
            if line[1]=='#':
                print(' '+line)
            continue
        if line=='[STOP]':
            print('[STOP] Trigger Found.')
            break
        rate=line.split('\t')[0]
        time=float(line.split('\t')[1])/4
        f.write(waver.ratable[rate],time)
except Exception as e:
    print('[ERROR]')
    print(e)
    print('While processing: '+line)
else: #done
    f.close()
    print('[FINISH]')
    sleep(0.25)
    os.startfile(os.path.join(os.curdir,'projects/%s.wav'%proj))
