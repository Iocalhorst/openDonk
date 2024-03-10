import sys; sys.dont_write_bytecode = True
import os
sys.path.append(os.getcwd() + '/..')
from common.common import *
assert COMMON_IMPORTS,"ERROR : [__main__] missing import"

from pprint import pprint
from common.view_model_factory import *
from common.view_model_controller import *
from common.tools_for_fools import *




class TokenViewModelController():
    def initialize(self,token):
        attribute_names=list(token.view_model.keys())
        for attribute_name in attribute_names:
            token.view_model[attribute_name]=getattr(token,attribute_name)

class HandViewModelController():
    def initialize(self,hand):
        attribute_names=list(hand.view_model.keys())
        for attribute_name in attribute_names:
            hand.view_model[attribute_name]=getattr(hand,attribute_name)

class SeatViewModelController():
    def initialize(self,seat):

        attribute_names=list(seat.view_model.keys())
        for attribute_name in attribute_names:
            seat.view_model[attribute_name]=getattr(seat,attribute_name)

class PlayerViewModelController():
    def initialize(self,player):
        attribute_names=list(player.view_model.keys())
        for attribute_name in attribute_names:
            player.view_model[attribute_name]=getattr(player,attribute_name)

class PotViewModelController():
    def initialize(self,pot):
        attribute_names=list(pot.view_model.keys())
        for attribute_name in attribute_names:
            pot.view_model[attribute_name]=getattr(pot,attribute_name)

class DealerViewModelController():
    def initialize(self,dealer):

        attribute_names=list(dealer.view_model.keys())
        for attribute_name in attribute_names:
            dealer.view_model[attribute_name]=getattr(dealer,attribute_name)


class TableViewModelController():




    def collect_seat_components(self,table):
        seat_components={}
        for seat in table.seats :
            seat_view=seat.get_view()
            seat_components.setdefault(seat.seat_id)
            seat_components[seat.seat_id]=seat_view
        return seat_components

    def collect_pot_components(self,table):
        pot_components={}
        for index,pot in enumerate(table.dealer.pots) :
            pot_view=pot.get_view()
            pot_components.setdefault(index)
            pot_components[index]=pot_view
        return pot_components


    def collect_dealer_components(self,table):
        return table.dealer.get_view()
    def collect_hand_components(self,table):
        #pass
        return table.dealer.current_hand.get_view()
    def collect_token_components(self,table):
        #pass
        return table.dealer.token.get_view()
    def collect_player_components(self,table):
        pass

    #
    ##(current_pot,closed_pots[])
    #pot_components={}
    #for closed_pot in table.dealer.closed_pots
    #    closed_pot_view=closed_pot.get_view()
    #    pot_components.setdefault()
    #    seat_components[seat.seat_id]=seat_view



    def initialize(self,table):


        #meta
        model=table.view_model
        table_meta_key="table_view_meta"
        table_meta=model.get(table_meta_key)

        for attrib in list(table_meta.keys()):
            table_meta[attrib]=getattr(table,attrib)

        table.view_model[table_meta_key]=table_meta
        #meta fin

        #components
        table_components_key="table_view_components"
        table_components_dict=model.get(table_components_key)

        seat_components=self.collect_seat_components(table)
        pot_components=self.collect_pot_components(table)
        hand_components=self.collect_hand_components(table)
        dealer_components=self.collect_dealer_components(table)
        token_components=self.collect_token_components(table)
        player_components=self.collect_player_components(table)

        #this is silly.
        #TODO("clean this up. use dataclasses or sth!")
        seat_components_key="seat_components"
        token_components_key="token_components"
        dealer_components_key="dealer_components"
        hand_components_key="hand_components"
        player_components_key="player_components"
        pot_components_key="pot_components"

        e="oops - keyerror, typo?"
        assert seat_components_key in table_components_dict,e
        assert token_components_key in table_components_dict,e
        assert dealer_components_key in table_components_dict,e
        assert player_components_key in table_components_dict,e
        assert hand_components_key in table_components_dict,e
        assert pot_components_key in table_components_dict,e

        #this is embarresing
        #TODO("clean this up. disgusting!")
        table_components_dict[seat_components_key]=seat_components
        table_components_dict[hand_components_key]=hand_components
        table_components_dict[pot_components_key]=pot_components
        table_components_dict[dealer_components_key]=dealer_components
        table_components_dict[token_components_key]=token_components
        table_components_dict[player_components_key]=player_components

        #this is gonna get me fired
        #TODO("clean this up. CLEAN THIS FUCKING UP!")
        table_components_dict[seat_components_key]=seat_components
        table_components_dict[hand_components_key]=hand_components
        table_components_dict[pot_components_key]=pot_components
        table_components_dict[dealer_components_key]=dealer_components
        table_components_dict[player_components_key]=player_components
        table_components_dict[token_components_key]=token_components

        table.view_model[table_components_key]=table_components_dict





        #pprint(table.view_model)
        #pprint(seat_components)#seat_components.setdefault(seat.)


        #for component in
        #seat_data meta=model.get("table_view_meta")
        #for seat in table.seats:
        #    seat.initialize_view()



        #sub_keys=list(key.keys())
        #    for sub_key in sub_keys:
        #        print(sub_key)

        #    componentlist(keys.get())
            #meta[key]=getattr(table,key)

        #{'table_view_meta': {'table_name': '', 'table_type': 'cashgame', 'game_type': 'nlhe', 'num_seats': '6max', 'stakes': {'sb': 0, 'bb': 0}}, 'table_view_components': {'seat_components': {}, 'hand_components': {}, 'pot_components': {}, 'dealer_components': {}, 'token_components': {}, 'player_components': {}}}
