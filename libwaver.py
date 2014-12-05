#coding=utf-8
from __future__ import division
import wave
from numpy import arange,short
from scipy import signal

ratable={
    '0':0,
    '-1':262,'-2':294,'-3':330,'-4':349,'-5':392,'-6':440,'-7':494,
    'L1':262,'L2':294,'L3':330,'L4':349,'L5':392,'L6':440,'L7':494,
    '1':532,'2':587,'3':659,'4':699,'5':784,'6':880,'7':988,
    '+1':1047,'+2':1175,'+3':1319,'+4':1397,'+5':1568,'+6':1760,'+7':1976,
    'H1':1047,'H2':1175,'H3':1319,'H4':1397,'H5':1568,'H6':1760,'H7':1976,
}

class wavefile(object):
    _framerate=16384
    _volumn=15000
    _tall=0
    
    f=None
    data=''
    
    def __init__(self,fname):
        if fname:
            self.f=wave.open(fname,'wb')
            self.f.setnchannels(1)
            self.f.setsampwidth(2)
            self.f.setframerate(self._framerate)
        else:
            self.data=''
        self._tall=0

    def write_bin(self,rate,time):
        t=arange(0,time,1.0/self._framerate)
        wave_data=signal.chirp(t,rate,time,rate,method='linear')*self._volumn
        wave_data=wave_data.astype(short)
        if self.f:
            self.f.writeframes(wave_data.tostring())
        else:
            self.data+=wave_data.tostring()
        self._tall+=time

    def write(self,rate,time):
        if rate!=0:
            ratet=1/rate
            t1=ratet-self._tall%ratet
            self.write_bin(0,t1) #prefix
            time-=t1
            t1=time*7/8+ratet-(time*7/8)%ratet
            self.write_bin(rate,t1) #main
            if time-t1>0:
                self.write_bin(0,time-t1) #suffix
        else:
            self.write_bin(0,time)

    def close(self):
        if self.f==None:
            return False
        else:
            try:
                self.f.flush()
                self.f.close()
            except:
                pass
            return True
