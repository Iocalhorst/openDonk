
import os
import sys; sys.dont_write_bytecode = True
sys.path.append(os.getcwd() + '/..')
from common.common import *
assert COMMON_IMPORTS,"ERROR : [__main__] missing import"


from common.view_model_factory import *
from common.view_model_controller import *

from hand import *


class TableToken():
    def __init__(self,dealer):
        self.dealer=dealer
        self.request=None
        self.response=None
        self.seat_id=0
        self.cards=[]
        self.chips=0

        self.view_model=ViewModelFactory.create_token_view_model()
        self.view_model_controller=TokenViewModelController()
    def initialize_view(self):
        self.view_model_controller.initialize(self)
    def get_view(self):
        return self.view_model.copy()

    def __repr__(self):
        s="\n"
        s+="[Token] seat_id = "+str(self.seat_id)+"\n"
        s+="            req = "+str(self.request)+"\n"
        s+="            res = "+str(self.response)+"\n"
        s+="          chips = "+str(self.chips)+"\n"
        s+="          cards = "+str(self.cards)+"\n"
        return str(s)
    def return_to_dealer(self):
        self.dealer.receive_token(self)
    def reset(self):
        self.request=None
        self.response=None
        self.adress=self.dealer
    def advance(self):
        while True:
            next_seat_id=self.seat_id+5
            next_seat_id%=len(self.dealer.table.seats)
        #l0g("debug : [token.advance] from ",self.seat_id," to ",next_seat_id)
            self.seat_id=next_seat_id
            self.adress=self.dealer.table.seats[self.seat_id]
            if self.adress.had_option==False and self.adress.has_cards():
                break
            #if self.adress.player and self.adress.holdcards and self.adress.holdcards[0] and self.adress.holdcards[1] and self.adress.chips_behind>0 :


            #    break

    def has_chips(self):
        if self.response['chips'] :
            return True
        return False
    def get_chips(self):
        return self.response['chips']

    def has_options(self):
        if self.request:
            if self.request:
                l0g(self.request)
                return True
            else :
                l0g("error : no request")
                exit(69)
                return False

    def get_options(self):
        return self.request
