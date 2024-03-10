import sys; sys.dont_write_bytecode = True
import os
sys.path.append(os.getcwd() + '/..')
from common.common import *
assert COMMON_IMPORTS,"ERROR : [__main__] missing import"
import time
import random
from common.debug_department import DONK_WARNING,DONK_DEBUG,DONK_ERROR
import pyray
#from common.tools_for_fools import *

class Streamer():
    def __init__(self,fx,fy,fvy):
        self.fx=fx
        self.fy=fy
        self.fvy=fvy

class AsciiMatrix():
    def __init__(self,width,height,num_streamers):
        self.available_glyphs=[
            'Ac','Kc','Qc','Jc','Tc','9c','8c','7c','6c','5c','4c','3c','2c',
            'As','Ks','Qs','Js','Ts','9s','8s','7s','6s','5s','4s','3s','2s',
            'Ah','Kh','Qh','Jh','Th','9h','8h','7h','6h','5h','4h','3h','2h',
            'Ad','Kd','Qd','Jd','Td','9d','8d','7d','6d','5d','4d','3d','2d'
            ]
        self.num_streamers=num_streamers
        self.glyphs=[]
        self.alphas=[]
        self.greens=[]
        self.cols=width
        self.rows=height
        while len(self.glyphs)<(self.cols*self.rows) :
            g=random.choice(self.available_glyphs)
            self.glyphs.append(g)
            self.alphas.append(10.0)
            self.greens.append(224.0)
        self.t0=time.time()
        self.change_frequency=0.02
        self.t1=self.t0+self.change_frequency
        self.streamers=[]
        self.last_update=time.time()
    def update_self(self):
        delta_t=time.time()-self.last_update
        self.last_update=time.time()
        if time.time()>self.t1 :
            self.t0=time.time()
            self.t1=self.t0+self.change_frequency
            glyph_index=random.randint(0,len(self.glyphs)-1)
            self.glyphs[glyph_index]=random.choice(self.available_glyphs)
        if len(self.streamers)<self.num_streamers :
            fx=float(random.randint(0,self.cols))
            fy=float(random.randint(0,self.rows))*-1.1
            fvy=8.0+float(random.randint(0,4))
            streamer=Streamer(fx,fy,fvy)
            self.streamers.append(streamer)
        list_streamers_to_delete=[]
        for index,green in enumerate(self.greens):
            if self.greens[index]>142.0 :
                self.greens[index]=142.0
        for streamer in self.streamers :
            streamer.fy+=streamer.fvy*delta_t
            if int(streamer.fy)>=self.rows :
                list_streamers_to_delete.append(streamer)
            else :
                x=int(streamer.fx)
                y=int(streamer.fy)
                idx=x+y*self.cols
                if idx>=0 and idx<len(self.alphas) :
                    self.alphas[idx]=232.0
                    self.greens[idx]=204.0
        for streamer_to_delete in list_streamers_to_delete :
            self.streamers.remove(streamer_to_delete)
        list_streamers_to_delete.clear()
        for idx,alpha in enumerate(self.alphas) :
            #self.alphas[idx]-=delta_t*172.0
            if self.alphas[idx]<142.0 :
                self.alphas[idx]-=delta_t*24.0
            else :
                self.alphas[idx]-=delta_t*172.0
            if self.alphas[idx]<=112.0 :
                self.alphas[idx]=112.0

    def draw_self(self):
        x=0
        y=0
        for index,g in enumerate(self.glyphs) :
            s=str(g)
            a255=self.alphas[index]
            g=self.greens[index]
            a=a255/255
            a=a*a
            a*=255.0
            #self.alphas[index]=a
            #for streamer in self.streamers :
            #    if int(streamer.fx) == x and int(streamer.fy)==y:
            pyray.draw_text(s,4+x*14,4+y*10,11,pyray.Color(24,int(g),14,int(a)))


            #    else :
            #        pyray.draw_text(s,4+x*12,4+y*10,10,pyray.Color(24,128,12,int(a)))
            x+=1
            if x==self.cols :
                y+=1
                x=0
