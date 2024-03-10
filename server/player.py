import os
import sys; sys.dont_write_bytecode = True
sys.path.append(os.getcwd() + '/..')
from common.common import *
assert COMMON_IMPORTS,"ERROR : [__main__] missing import"

from table_pool import TablePool
from common.view_model_factory import *
from common.view_model_controller import *

import random

class Player():
    def __init__(self,player_id,player_name,player_avatar_filename):

        self.player_id=player_id
        self.player_name=player_name
        self.player_avatar_filename=player_avatar_filename

        self.options={}
        self.holdcards=[None,None]
        self.view_model=ViewModelFactory.create_player_view_model()
        self.view_model_controller=PlayerViewModelController()

        print("DEBUG : [Player.__init__] id : ",player_id,", name : ",player_name,", avatar_file : ",player_avatar_filename)
        #pr1nt("player[",player_name,"] created")
    def quick_start(self):
        assert TablePool.quick_seat(self),"player.quick_start failed"
    def __repr__(self):
        return self.player_name
    def initialize_view(self):
        self.view_model_controller.initialize(self)
    def get_view(self):
        return self.view_model.copy()

    def read_card(self,card):
        if self.holdcards[0] and self.holdcards[1] :
            assert False,"DealerError||DevError [Player.read_card] has already been dealt 2 cards "
        if self.holdcards[1]:
            self.holdcards[0]=card
        else :
            self.holdcards[1]=card

        #l0g(self.name,card)

        #l0g(self.name," "*(10-len(self.name)),"got dealt ",card)
    def show(self):
        #l0g(self.name," shows ",self.holdcards,end="")

        assert False,"NOT_IMPLEMENTED"
    def read(self,options,chips_inline):
        #l0g("ci : ",chips_inline)
        #self.token=token
        #l0g(self," reading options : ",options)
        self.options=options
        self.chips_inline=chips_inline
        pr1nt("DEBUG : [Player.read] options : ",self.options)
        #l0g("debug : self.chips_inline=",self.chips_inline)
        count=0
        for o in self.options :
            count+=1
        assert count>0,"player.read() count(self.options)==0"
        decision_id=random.randrange(count)

        decision="lalala"
        i=0
        for option in self.options :
            if i==decision_id:
                decision=option
                break
            else :
                i+=1
        #l0g("debug : decision =",decision," ",self.options[decision])

        chips=self.options[decision]
        #l0g("debug :",self.name," folds",self.holdcards)
        response={'player_name':self.player_name,'option':decision,'chips':chips,'cards':self.holdcards};
        #l0g("DEBUG [player.read]: ",response)
        self.options.clear()
        return response

    def muck_cards(self):
        cards=[]
        for c in self.holdcards:
            cards.append(c)
        self.holdcards[0]=None
        self.holdcards[1]=None

        return cards
