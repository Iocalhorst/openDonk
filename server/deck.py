import os
import sys; sys.dont_write_bytecode = True
sys.path.append(os.getcwd() + '/..')
from common.common import *
assert COMMON_IMPORTS,"ERROR : [__main__] missing import"
from common.tools_for_fools import *


import logging
import functools
import random

values=[ 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10, 11, 12, 13, 14]
v_repr=["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
suites=["c","s","h","d"]

@functools.total_ordering
class Card():
    def __init__(self,card_id,v,s):
        self.val=v
        self.repr=v_repr[v-2]
        self.s=s
        self.card_id=card_id
    def __repr__(self):
        return str(self.repr)+str(self.s)
    def show(self):
        l0g(self)
    def __eq__(self,other):
        return self.val==other.val
    def __lt__(self,other):
        if self.val<other.val :
            return True
        else :
            return False


class Deck():
    def __init__(self):
        self.stack=[]
        i=0
        for v in values:
            for s in suites:
                i+=1
                c=Card(i-1,v,s)
                #l0g(c)
                self.stack.append(c)        
    def __repr__(self):
        i=0
        s="\n"
        for card in self.stack :
            i+=1
            s+=str(card)
            s+=", "
            if i%4==0 :
                s+="\n"
        return s
    def deal(self):
        c=self.stack.pop()
        #self.stack.remove(c)
        pr1nt("DEBUG : [deck.deal] pop ",c)
        return c
    def shuffle(self):
        random.shuffle(self.stack)
    def show(self):
        i=0
        for c in self.stack:
            if i>3 :
                l0g("")
                i=0
            i+=1
            l0g(c,end=" ")
        l0g("")
