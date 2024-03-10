#from player import *
#from dealer import *
#from deck import *
#from table_seat import *
#from hand_evaluator import *
#from token_pot import *

from dealer import *
from common.view_model_factory import *
from common.view_model_controller import *
from pprint import pprint
from table_token import TableToken
#from table import Table

class Table():
    def __init__(self,table_id,table_name,num_seats,game_type,stakes):
        self.table_id=table_id
        self.table_name=table_name
        self.num_seats=num_seats
        self.game_type=game_type
        self.stakes=stakes
        self.view_model=ViewModelFactory.create_table_view_model()
        self.view_model_controller=TableViewModelController()

        self.seats=[]
        self.dealer=Dealer(game_type,self)
        self.stakes=stakes
        self.chips_sum=0
        #self.token=TableToken(self.dealer)
        self.board=[]
        self.observer=None
        #self.table_meta_data={
        #    "table_name":table_name,
        #    "num_seats":num_seats,
        #    "game_type":game_type,
        #    "stakes":stakes}
        #    }
        #self.table_seats_data={}
        #self.table_view_model={
        #    "table_meta_data":self.table_meta_data,
        #    "table_seats_data":None,
        #    "table_pots_data":None,
        #    "table_hand_data":None,
        #    "table_players_data":None,
        #    }

    def initialize_view(self):
        for seat in self.seats:
            seat.initialize_view()
        self.dealer.initialize_view()
        self.view_model_controller.initialize(self)
            #pprint(self.view_model)
            #for setattr(x, attr, 'magic')
    def get_view(self):
        self.initialize_view()
        #print("DEBUG : table.get_view()")
        #pprint(self.view_model.copy())
        return self.view_model.copy()
    def check_seat_count(self):
        if len(self.seats)!=self.num_seats:
            return "failed"
        else :
            return "passed"


    def check_seats(self):

        dict_results={}
        #print("DEBUG : [Table] table.check_seats :")
        result="passed"
        for index,seat in enumerate(self.seats):
            seat_result,seat_result_details=seat.verify_integrity()
            dict_results.setdefault(index)
            dict_results[index]=(seat_result,seat_result_details)
            if seat_result!="passed" :
                result="failed"
            #print("       ",index," : ",seat_result,", ",seat_result_details)

        return result,dict_results

    def verify_integrity(self,silent=False):

        results={
        "check_seat_count":self.check_seat_count(),
        "check_seats":self.check_seats(),
        }
        #if silent==True :
            #pprint(results)

    def add_seat(self,seat):
        self.seats.append(seat)
        #self.table_seats_data.set_default(seat.seat_id)
        #self.table_seats_data[seat.seat_id]=seat.get_view_model()

    def has_player_id(self,player_id):
        for seat in self.seats :
            if seat.player_id and seat.player_id==player_id :
                print("WARNING : [table.has_player_id] duplicate player id")
                return True
        #print("DEBUG : [table.has_player_id] player_id not present")
        return False


    def quick_seat(self,player):
        if self.has_player_id(player.player_id):
            print("Error : [table.quick_seat] denied for player : id=",player.player_id,", name=",player.player_name," PLAYER_IS_ALREADY_PRESENT")
            return False
        else :
            for seat in self.seats :
                if seat.is_occupied==False and seat.is_open==True :
                    seat.register_player(player)
                    self.chips_sum+=seat.chips_behind
                    print("DEBUG : [table] self.chips_sum = ",self.chips_sum)
                    msg=seat.player_name+", id : "+str(seat.player_id)+", has joined the table"
                    print(msg)
                    seat_event_data={"SEAT_EVENT_TYPE":"PLAYER_JOIN","SEAT_ID":seat.seat_id}
                    self.observer.handle_table_event(table_event_type="SEAT_EVENT",table_event_data=seat_event_data)
                    print("DEBUG : [table.quick_seat] : quick seat success")
                    return True




    def set_observer(self,observer):
        self.observer=observer

    #def __repr__(self):
    #    s=str("Table : ["+self.name+"]\n\n")
    #    for seat in self.seats :
    #        s+=str(seat)+"\n"
    #    return s

    def get_seat(self):
        #check if player is already seated
        for seat in self.seats:
            if seat.is_occupied==False :
                return seat
        assert False,"out of seats"

        #find open seat,assign player to seat
        #for seat in self.seats:
        #    if not seat.player:
        #        seat.occupy(player)
        #        seat.chips_behind=100
        #        print(player.name," has joined the table")
        #        return True
        #    else :
        #        print("get_seat failed")
    def has_nothing_to_do(self):
        if self.dealer.current_hand.current_state=="state_uninitialized" :
            return True
        else :
            #l0g("table","something to do")
            return False
                        #l0g("table","hand uninitialized")


            #l0g("table","something weird is going on")

        #elif self.hand.in_progress() :
        #    l0g("table","hand in progress")
        #    return False
    def has_enough_players(self):
        available_player_count=0
        #l0g("table","test")


        for seat in self.seats :
            #l0g("seat","test")
            if seat.has_player() :
                #l0g("table","has_player")
                if seat.is_not_sitting_out():
                    #l0g("table","is not sitting out")
                    if seat.chips_behind>self.stakes['bb'] :
                        #l0g("table","is ready to playe")
                        available_player_count+=1
                    #else :
                        #l0g("table","out_of_chips")
                #else :
                    #l0g("table","is sitting out")
        if available_player_count>2 :
            #l0g("table","enough players")
            return True
        else :
            return False

    #def start_hand(self):
    #    print("INFO :","starting new hand","[",self.name,"]\n")

    #    self.hand=Hand(self)
    #    self.dealer.initialize_hand(self.hand)

    #    self.token.reset()
    #    self.pot=Pot()
    #def join(self,player):
    #    seat=self.get_seat()
    #    seat.register_player(player)
    #    seat.view_model_controller.initialize(seat)
    #    self.view_model_controller.initialize(self)
    #    print(player.player_name," has joined the table")



    def has_hand_in_progress(self):
        if self.dealer.current_hand.in_progress():
            return True
        else :
            return False
    def advance_dealer(self):
        self.dealer.advance_hand()
        #update_observer .... etc
        #TODO("implement update_messages for the 'view'")
