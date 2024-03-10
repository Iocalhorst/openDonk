
import os
import sys; sys.dont_write_bytecode = True
sys.path.append(os.getcwd() + '/..')
from common.common import *
assert COMMON_IMPORTS,"ERROR : [__main__] missing import"

from common.tools_for_fools import *
from common.view_model_factory import *
from common.view_model_controller import *

valid_hand_states={
                    'state_uninitialized',
                    'state_initialized',
                    'state_await_dealer_cards',
                    'state_await_dealer_open',
                    'state_betting_open',
                    'state_betting_closed',
                    'state_await_pot_consolidation',
                    'state_pot_consolidation_done',
                    'state_await_showdown',
                    'state_await_pot_assignment',
                    'state_hand_completed'
                }

class Hand():

    def __init__(self):
        pr1nt("DEBUG : hand.init")
        self.history=[]
        #self.current_street="preflop"
        self.streets_pending=["street_preflop","street_flop","street_turn","street_river"]
        self.live_players=[]
        #s="Table : "+table.name+str(table.stakes)
        #self.log(s)
        self.bu_index=0
        self.sb_index=0
        self.bb_index=0
        self.action_index=0

        self.is_finished=False
        #@property
        self.current_street="street_uninitialized"
        self.current_state="state_uninitialized"

        self.view_model=ViewModelFactory.create_hand_view_model()
        self.view_model_controller=HandViewModelController()
    def initialize_view(self):
        self.view_model_controller.initialize(self)
    def get_view(self):
        self.initialize_view()
        return self.view_model.copy()
    def register_player(self,player):
        assert player,"hand.register_player(None)"
        self.live_players.append(player.player_name)
        #self.log(player.name)
    def set_bu_index(self,bu_index):
        self.bu_index=bu_index
    def set_sb_index(self,sb_index):
        self.sb_index=sb_index
    def set_bb_index(self,bb_index):
        self.bb_index=bb_index


    def state_assign(self,new_state):
        e="Error : [hand.state_assign] invalidState, hand.current_state["+self.current_state+"] is invalid"
        assert self.current_state in valid_hand_states,e
        e="Error : [hand.state_assign] assignmentNotAllowed, new_state["+new_state+"] is equal to hand.state["+self.current_state+"]"
        assert self.current_state!=new_state,e
        e="Error : [hand.state_assign] valueError, new_state["+new_state+"] is invalid"
        assert new_state in valid_hand_states,e
        s="DEBUG : [hand.state_assign] "+self.current_state+" -> "+new_state
        pr1nt(s)
        self.current_state=new_state
    def street_advance(self):
        required_state='state_await_dealer_cards'
        e="Error : [hand.street_advance] notAllowed, current_state['"+self.current_state+"'] != required_state['"+required_state+"']"
        assert self.current_state==required_state,e
        next_street=self.streets_pending.pop(0)
        s="DEBUG : [hand.street_advance] "+self.current_street+" -> "+next_street
        self.current_street=next_street
        pr1nt(s)
    def remove_live_player(self,player_name):
        if player_name not in self.live_players :
            e="Error : [hand.remove_live_player] "+player_name+" not in "+str(self.live_players)
            pr1nt("live players : ",self.live_players)
            assert False,e
        else :
            s="DEBUG : [hand.remove_live_player] removing "+player_name+" from live_players"#+str(self.live_players)
            pr1nt(s)
            self.live_players.remove(player_name)


    #def abort(self):
    #    self.is_finished=False
    def in_progress(self):
        if self.current_state=='state_hand_completed' :
            return False
        return True
