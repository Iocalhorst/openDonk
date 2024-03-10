import sys; sys.dont_write_bytecode = True
import os
sys.path.append(os.getcwd() + '/..')
from common.common import *
from common.tools_for_fools import *
assert COMMON_IMPORTS,"ERROR : [__main__] missing import"

class ViewModelFactory():

    def create_table_view_model():

        table_view_model={

            "table_view_meta":{
                "table_id":None,
                "table_name":None,
                "game_type":None,
                "num_seats":None,
                "stakes":None#{
                    #"sb":0,
                    #"bb":0
                    #},
                },

            "table_view_components":{

                "seat_components":{},
                "hand_components":{},
                "pot_components":{},
                "dealer_components":{},
                "token_components":{},
                "player_components":{},
                }
            }

        return table_view_model

    def create_player_view_model():
        TODO("review player_view_model")
        player_view_model={
            "player_name":None,
            "player_id":None
            }
        return player_view_model

    def create_seat_view_model():
        seat_view_model={
            "seat_id":None,
            "chips_inline":None,
            "chips_behind":None,
            "is_occupied":None,
            "is_sitting_out":None,
            "is_open":None,
            "player_id":None,
            "all_in_flag":None,
            "holdcard_ids":[-1,-1],
            "had_option":None,
            "player_name":None,
            "player_id":None,
            "player_avatar_filename":None
        }
        return seat_view_model

    def create_dealer_view_model():
        dealer_view_model={
                #"deck_attributes":{},
                #"table":"table",
                #"muck":[],
                "options":{
                    "fold":0,
                    "call":2,
                    },
                #"current_pot":{},
                #"closed_pots":[],
                "action_is_closed":False,
                "action_seat":-1,
                "action_is_up_to":-1,
                "limit_raises":2, #for debugging
                "to_raise":4,
                "board_card_ids":[-1,-1,-1,-1,-1]
                #:{
                #    "flop" :  { "first" :-1, "second":-1, "third":-1 },
                #    "turn" :  { "fourth":-1 },
                #    "river" : { "fifth" :-1 },
                #    }
                }
        return dealer_view_model

    def create_pot_view_model():
        pot_view_model={
                "total_amount":None,
                "pot_id":None,
                "seat_ids":None,
                "is_closed":None
                }
        return pot_view_model

    def create_hand_view_model():
        hand_view_model={
               "current_street":"street_uninitialized",
               "current_state":"state_uninitialized",
               "streets_pending":["street_preflop","street_flop","street_turn","street_river"],
               "live_players":[],
               "bu_index":0,
               "sb_index":0,
               "bb_index":0,
               "is_finished":False,
               "action_index":0
               }
        return hand_view_model

    def create_token_view_model():
        token_view_model={}
        token_view_model_={
            "dealer":None,
            "request":{},
            "response":{},
            "seat_id":-1,
            #"cards":[],
            "chips":0
            }
        return token_view_model
