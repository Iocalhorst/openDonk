
#from player import *
#from dealer import *
#from deck import *
#from table_seat import *
#from hand_evaluator import *
#from token_pot import *

import os
import sys; sys.dont_write_bytecode = True
sys.path.append(os.getcwd() + '/..')
from common.common import *
assert COMMON_IMPORTS,"ERROR : [__main__] missing import"


from common.view_model_factory import *
from common.view_model_controller import *

class Seat():
    def __init__(self,seat_id):
        self.seat_id=seat_id
        self.chips_inline=0
        self.all_in_flag=False
        self.chips_behind=0
        self.is_occupied=False
        self.is_sitting_out=False
        self.is_open=True
        self.player_id=-1
        self.player_name=None
        self.player_avatar_filename=None
        self.holdcards=[None,None]
        self.holdcard_ids=[-1,-1]
        self.had_option=False
        self.view_model=ViewModelFactory.create_seat_view_model()
        self.view_model_controller=SeatViewModelController()
        self.player=None
        self.inline_return_count=0
        self.pot_assign_count=0
        self.call_count=0
        self.fold_count=0
        self.raise_count=0
        self.check_count=0
        self.inline_return_count=0
        self.pot_assign_count=0
        self.won_without_showdown=0
        self.won_at_showdown=0
        self.split_pots=0
        self.went_to_showdown=0

    def is_not_sitting_out(self):
        if self.is_sitting_out==True :
            return False
        else :
            return True

    def has_player(self):
        if self.player :
            return True
        else :
            return False

    def has_cards(self):
        if len(self.holdcards)==2 and self.holdcards[0] and self.holdcards[1] :
            return True
        else :
            return False

    def verify_integrity(self):
        result="passed"
        details={"seat_id":self.seat_id,"status":"seat_ok"}
        return result,details

    def initialize_view(self):
        self.view_model_controller.initialize(self)
    def get_view(self):
        return self.view_model.copy()

    def register_player(self,player):
        self.player=player
        self.player_id=player.player_id
        self.player_name=player.player_name
        self.player_avatar_filename=player.player_avatar_filename
        self.is_occupied=True
        self.is_open=False
        self.is_sitting_out=False
        self.chips_behind=5000
        self.chips_inline=0

        #pr1nt("DEBUG : seat registering player ",player )

    def __repr__(self):

        s="Seat "+str(self.seat_id)+" : "
        if self.player :
            s+=padl(str(self.player),13)+"["+str(self.chips_behind)+"]"
        else :
            s+="open"
        return s
    def occupy(self,player):
        if self.player :
            pr1nt("is occupied")
            return False
        if player :
            self.player=player
            return True
    def move_chips_inline(self,count):
        self.chips_behind-=count
        self.chips_inline+=count
        if self.chips_behind==0 :
            self.all_in_flag=True


    def has_chips_inline(self):
        #assert self.chips_inline,"seat error, no object 'chips_inline'"
        if self.chips_inline>0 :
            return True
        else :
            return False
    def receive_token(self,token):
#        pr1nt("DEBUG : [seat.receive_token]",self," received token :",token)
        assert token,"[seat.receive_token] token!=None"
        self.token=token
        name="emtpy"
        assert self.player, "[seat.receive_token] self.player!=None"
        assert self.holdcards,"[seat.receive_token] self.holdcards!=None"
        assert self.player.holdcards,"[seat.receive_token] self.player.holdcards!=None"
        options=token.get_options()
        chips_inline=self.chips_inline
        response=self.player.read(options,chips_inline)
        pr1nt("DEBUG : [seat.receive_token] response=",response)
        token.response=response
        token.cards=self.holdcards

    def receive_card(self,card):
        if self.holdcards[0] and self.holdcards[1] :
            print("DEBUG : [seat.receive_card] seat_id : ",self.seat_id,", self.holdcards[0] : ",self.holdcards[0],", [1] : ",self.holdcards[1] )
            assert False,"DealerError assertion failed : self.holdcards[0] and self.holdcards[1] == True"
        if self.holdcards[1]:
            self.holdcards[0]=card
            self.holdcard_ids[0]=card.card_id
        else :
            self.holdcards[1]=card
            self.holdcard_ids[1]=card.card_id
        self.player.read_card(card)
        #self.holdcards.append(card)
    def muck_cards(self):
        self.holdcards=[None,None]
        self.player.holdcards=[None,None]
        self.holdcard_ids[0]=-1
        self.holdcard_ids[1]=-1
    def get_cards(self):
        cards=[]
        for c in self.holdcards:
            cards.append(c)
        return cards
    def handle_request(self,txt,amount):
        if self.player:
            if self.chips_behind:
                if self.chips_behind>=amount:
                    self.chips_inline=amount
                    self.chips_behind-=amount
                    #pr1nt("debug :",txt,", ",amount," ok")
                    s=self.player.player_name+"(Seat"+str(self.seat_id)+")"+" posts "+txt+" "+str(amount)
                    l0g("seat",s)
                    return True
                else :
                    pr1nt("blind post fail")
                    exit(69)
                    #pr1nt("debug :",txt,", ",amount," out of chips")
                    return False
            else :
                pr1nt("error : no chips at all")
                return False
        else :
            pr1nt("error : no player to take chips from")
            return False
        pr1nt("error : unreachable")
        exit(69)
