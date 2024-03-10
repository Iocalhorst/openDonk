import os
import sys; sys.dont_write_bytecode = True
sys.path.append(os.getcwd() + '/..')
from common.common import *
assert COMMON_IMPORTS,"ERROR : [__main__] missing import"

from table_token import TableToken
from deck import *
from pot import Pot
from hand import Hand
from hand_evaluator import *
from common.tools_for_fools import *
from common.view_model_factory import *
from common.view_model_controller import *
from pot_manager import PotManager
from pprint import pprint


class Dealer():
    def __init__(self,game,table):
        assert game=="nlhe","NOT_IMPLEMENTED, only nlhe is supported for now"
        self.num_hands_played=0
        self.deck=Deck()
        self.table=table
        self.muck=[]
        self.options={'fold':0,'call':2}
        self.pots=[]
        self.action_is_closed=False
        self.action_seat=-1
        self.action_is_up_to=0
        self.limit_raises=2 #for debugging
        self.to_raise=4
        self.board=[]
        self.board_card_ids=[-1,-1,-1,-1,-1]
        self.last_bu_index=random.randrange(6)+6
        self.last_sb_index=self.last_bu_index-1
        self.last_bb_index=self.last_bu_index-2
        self.last_bu_index%=6
        self.last_sb_index%=6
        self.last_bb_index%=6

        self.bu_stats=[0,0,0,0,0,0]
        self.sb_stats=[0,0,0,0,0,0]
        self.bb_stats=[0,0,0,0,0,0]

        self.sum_pots_assigned=0
        self.num_pots_assigned=0

        self.current_hand=Hand()
        self.last_hand=None
        self.view_model=ViewModelFactory.create_dealer_view_model()
        self.view_model_controller=DealerViewModelController()
        self.token=TableToken(self)

        self.has_announced_to_start_soon=False
        self.time_of_planned_start=None
        self.commit_count=0
        self.t0=time.time()
    def table_report(self):
        return
        n=self.num_hands_played
        n%=50
        if n>0 :
            return
        os.system('clear')
        avg_potsize=self.sum_pots_assigned/self.num_pots_assigned
        h_per_second=round(self.num_hands_played/(time.time()-self.t0),2)
        h_per_minute=round(60*self.num_hands_played/(time.time()-self.t0),2)
        h_per_hour=round(3600*self.num_hands_played/(time.time()-self.t0),2)

        print("hands played : ",self.num_hands_played,",   average potsize : ",round(avg_potsize,2),",   hands/s : ",h_per_second,",   h/m : ",h_per_minute,",   /h : ",h_per_hour)

        for seat in self.table.seats :
            print("")
            print("seat id : ",seat.seat_id,",  name: ",padl(seat.player_name,13),", chips : ",padl(str(seat.chips_behind),8),", bu : ",padl(str(self.bu_stats[seat.seat_id]),8),", sb : ",padl(str(self.sb_stats[seat.seat_id]),6),", bb : ",padl(str(self.bb_stats[seat.seat_id]),8))
            print(" checks : ",str(seat.check_count),", folds: ",padl(str(seat.fold_count),5),", calls : ",padl(str(seat.call_count),5),", raises : ",padl(str(seat.raise_count),5)," pot_assign_count : ",seat.pot_assign_count,", inline_returns : ",seat.inline_return_count)
            print(" went_to_showdown : ",seat.went_to_showdown,", won_without_showdown : ",seat.won_without_showdown," won_at_showdown : ",seat.won_at_showdown," split_pots : ",seat.split_pots)


        time.sleep(0.1)
    def has_not_announced_to_start_soon(self):
        if self.has_announced_to_start_soon==False :
            return True
        else :
            return False
    def announce_to_start_in(self,time_span):
        #this should probably be publicly pushed to all subscribers
        #todo : think about event domain groups
        t_str=str(time_span)
        msg="starting new hand in "+t_str+" seconds"
        #self.table.observer.handle_dealer_event(msg)
        self.has_announced_to_start_soon=True
        self.time_of_planned_start=time.time()+time_span

    def time_has_come_to_start(self):
        if self.time_of_planned_start :
            if time.time()>self.time_of_planned_start:
                self.t0=time.time()
                return True
        else :
            return False
    def cancel_announcement(self):
        self.has_announced_to_start_soon=False
        self.time_of_planned_start=None
        #self.table.observer.handle_dealer_event("hand was cancelled")
        #self.table.observer.handle_dealer_event("waiting for players")
    def commit_players(self):
        self.commit_count+=1
        pr1nt("DEBUG : [Dealer.commit_players] commit_count==",self.commit_count)
        e="Error : [Dealer.commit_players] hand.live_players != empty"
        if len(self.current_hand.live_players)!=0:
            pr1nt(e)

            assert False,e
        else :
            for seat in self.table.seats :
                if seat.has_player() and seat.is_not_sitting_out() and seat.chips_behind>self.table.stakes['bb'] :
                    self.current_hand.register_player(seat.player)
        pr1nt("DEBUG : [Dealer.commit_players] hand.live_players==",self.current_hand.live_players)


    def check_integrity(self):
        ##########seats,holdcards###########
        for s in self.table.seats :
            e="seat_id"+str(s.seat_id)+" has_cards(), s.holdcards=="+str(s.holdcards)
            assert s.has_cards()==False,"seat_was_left_with cards"#TODO : do deck/muck integrity check

        ##########seats,inline##############
        for seat in self.table.seats :
            e="seat "+str(seat.seat_id)+" was left with "+str(seat.chips_inline)+" inline!"
            assert seat.chips_inline==0,e

        ##########seats,chips_behind,sum####
        seat_chips_sum=0
        for seat in self.table.seats :
            seat_chips_sum+=seat.chips_behind
        e="chips in seats.chips_behind missing! expected : "+str(self.table.chips_sum)+", but got : "+str(seat_chips_sum)
        assert seat_chips_sum==self.table.chips_sum,e

        ##########deck,muck###########
        sum_card_entities=len(self.muck)+len(self.deck.stack)
        if sum_card_entities!=52 :
            pr1nt("muck : ",len(self.muck))
            pr1nt("deck : ",len(self.deck.stack))
        assert sum_card_entities==52,"sum_card_entities != 52 "
        ##########pots###########
        assert len(self.pots)==0,"theres a 'forgotten' pot in the dealers list. the list should be empty"

    def reset(self):
        self.check_integrity()



        self.muck.clear()
        self.deck=Deck()
        self.deck.shuffle()
        self.current_hand=Hand()
        self.options={'fold':0,'call':2}




        self.action_is_closed=False
        self.action_seat=-1
        self.action_is_up_to=0
        self.limit_raises=2 #for debugging
        self.to_raise=4
        self.board.clear()
        self.board_card_ids=[-1,-1,-1,-1,-1]
        self.token=TableToken(self)

    def initialize_hand(self):
        self.reset()

        e="ERROR : [dealer.initialize_hand] false initialization, hand.live_players[] not empty"
        assert len(self.current_hand.live_players)==0,e
        self.commit_players()
        #bu_index=random.randrange(6)
        #sb_index=bu_index+5
        #bb_index=sb_index+5
        #bu_index%=6
        #sb_index%=6
        #bb_index%=6

        bu_index=self.last_bu_index+5
        bu_index%=self.table.num_seats
        sb_index=self.last_sb_index+5
        sb_index%=self.table.num_seats
        bb_index=self.last_bb_index+5
        bb_index%=self.table.num_seats
        self.last_bu_index=bu_index
        self.last_sb_index=sb_index
        self.last_bb_index=bb_index
        self.current_hand.set_bu_index(bu_index)
        self.current_hand.set_sb_index(sb_index)
        self.current_hand.set_bb_index(bb_index)

        self.bu_stats[bu_index]+=1
        self.sb_stats[sb_index]+=1
        self.bb_stats[bb_index]+=1
            #register players that are eligible
            #for now its just "hanging around" and "not sitting out" and "chips_behind>stakes["bb"]"

        #s="bu is at "+str(self.current_hand.bu_index)
        #l0g("dealer",s)
        #hand.log("Button is at Seat "+str(bu_index))

        #s="sb is at "+str(self.current_hand.sb_index)
        #l0g("dealer",s)

        #s="bb is at "+str(self.current_hand.bb_index)
        #l0g("dealer",s)
        sb=self.table.seats[self.current_hand.sb_index]
        bb=self.table.seats[self.current_hand.bb_index]

        if sb.handle_request("sb",1) :
            s=sb.player.player_name+" posts sb "+str(1)
            #l0g("dealer",s)#hand.log(s)

            seat_event_data={
                "SEAT_EVENT_TYPE":"POST",
                "SEAT_ID":sb.seat_id,
                "AMOUNT":1,
                "SEAT_EVENT_TEXT":s
            }

            self.table.observer.handle_table_event(table_event_type="SEAT_EVENT",table_event_data=seat_event_data)#seat_event(seat_event_data)
            time.sleep(0.5)

        else :
            self.table_report()
            e="sb wasnt posted"
            #print(e)
            assert False,e
        if bb.handle_request("bb",2):
            s=bb.player.player_name+" posts bb "+str(2)
            #l0g("dealer",s)
            seat_event_data={
                "SEAT_EVENT_TYPE":"POST",
                "SEAT_ID":bb.seat_id,
                "AMOUNT":2,
                "SEAT_EVENT_TEXT":s
            }
            self.table.observer.handle_table_event(table_event_type="SEAT_EVENT",table_event_data=seat_event_data)
            time.sleep(0.5)
            #l0g("debug : sb posted sb")
        else :
            self.table_report()
            e="bb wasnt posted"
            assert False,e

        self.action_is_up_to=self.table.stakes['bb']
        self.current_hand.state_assign("state_initialized")

    def initialize_view(self):
        self.view_model_controller.initialize(self)
    def get_view(self):
        self.initialize_view()
        return self.view_model.copy()

    def receive_token(self,token):
        self.token=token
        assert self.token,"no token provided"
        assert self.token.response,"expected token.response, got none"
        assert self.token.response['option'],"expected key 'option' in self.token.response"

        if self.token.response['option']=='fold':
            self.token.adress.fold_count+=1
            cards=self.token.adress.get_cards()
            for c in cards :
                self.muck.append(c)
            self.token.adress.muck_cards()
            self.token.adress.had_option=True
            self.current_hand.remove_live_player(self.token.adress.player.player_name)
            seat_event_text="Seat "+str(self.token.adress.seat_id)+"["+self.token.adress.player.player_name+"]"+" folds"
            seat_event_data={
                "SEAT_EVENT_TYPE":"FOLD",
                "SEAT_ID":self.token.adress.seat_id,
                "SEAT_EVENT_TEXT": seat_event_text
                }
            self.table.observer.handle_table_event(table_event_type="SEAT_EVENT",table_event_data=seat_event_data)
            time.sleep(0.5)

            seat_id=token.adress.seat_id
            for pot in self.pots :
                assert seat_id in pot.seat_ids,"seat folded, but was not listed in pot.seat_ids. thats really bad"
                pot.seat_ids.remove(seat_id)
                pr1nt("DEBUG : [dealer] removing seat_id : ",seat_id," from pot, pot_id ",pot.pot_id)

        elif self.token.response['option']=='call':
            self.token.adress.call_count+=1
            chips=self.token.get_chips()
            self.token.adress.move_chips_inline(chips)
            self.token.adress.had_option=True
            seat_event_text="Seat "+str(self.token.adress.seat_id)+"["+self.token.adress.player.player_name+"]"+" calls "+str(chips)
            seat_event_data={
                "SEAT_EVENT_TYPE":"CALL",
                "SEAT_ID":self.token.adress.seat_id,
                "AMOUNT": chips,
                "SEAT_EVENT_TEXT": seat_event_text,
                }
            self.table.observer.handle_table_event(table_event_type="SEAT_EVENT",table_event_data=seat_event_data)
            time.sleep(0.5)

        elif self.token.response['option']=='check':
            self.token.adress.check_count+=1
            self.token.adress.had_option=True
            seat_event_text="Seat "+str(self.token.adress.seat_id)+"["+self.token.adress.player.player_name+"]"+" checks"
            seat_event_data={
                "SEAT_EVENT_TYPE":"CHECK",
                "SEAT_ID":self.token.adress.seat_id,
                "SEAT_EVENT_TEXT": seat_event_text
                }
            self.table.observer.handle_table_event(table_event_type="SEAT_EVENT",table_event_data=seat_event_data)
            time.sleep(0.5)

            seat_id=token.adress.seat_id
            for pot in self.pots :
                assert seat_id in pot.seat_ids,"seat checked, but was not listed in pot.seat_ids. thats really bad"

        elif self.token.response['option']=='raise':
            self.token.adress.raise_count+=1
            chips=self.token.get_chips()
            for seat in self.table.seats :
                if seat.has_cards() :
                    seat.had_option=False
                else :
                    seat.had_option=True
            self.token.adress.move_chips_inline(chips)
            self.token.adress.had_option=True

            self.action_is_up_to=self.token.adress.chips_inline
            seat_event_text="Seat "+str(self.token.adress.seat_id)+"["+self.token.adress.player.player_name+"]"+" raises to ("+str(self.token.adress.chips_inline)+"+"+str(chips)+")"
            seat_event_data={
                "SEAT_EVENT_TYPE":"RAISE",
                "SEAT_ID":self.token.adress.seat_id,
                "AMOUNT":chips,
                "SEAT_EVENT_TEXT": seat_event_text
                }
            self.table.observer.handle_table_event(table_event_type="SEAT_EVENT",table_event_data=seat_event_data)
            time.sleep(0.5)
            self.limit_raises-=1 #debug, to not have "them" raise all over the place
            self.to_raise*=2 #debug, to enforce "fixed-limit-type" contraints

            seat_id=token.adress.seat_id
            for pot in self.pots :
                assert seat_id in pot.seat_ids,"seat raised, but was not listed in pot.seat_ids. thats really bad"
                #pot.seat_ids.remove(seat_id)

        else :
            token_response_option=self.token.response['option']
            e="unreachable, invalid token.option : "+token_response_option
            assert False,e
        self.token.response.clear()
        self.token.request.clear()

    def action_should_close(self):
        if len(self.current_hand.live_players)==1 :
            return True
        for seat in self.table.seats :
            if seat.player_name in self.current_hand.live_players and seat.had_option==False :
                return False
        return True

    def prepare_token(self):
        to_call=self.action_is_up_to-self.table.seats[self.token.seat_id].chips_inline
        assert to_call>=0,"to_call>=0"
        to_raise=self.to_raise #TODO : dynamically determine raise size limits
        options={'fold':0,'call':to_call,'check':0,'raise':to_raise}
        if to_call==0 :
            options.pop('call')
            options.pop('fold') #TODO implassert False,eement "checking is free" warning
        else :
            options.pop('check')
        if self.limit_raises==0:
            options.pop('raise')
        self.token.request=options

    def set_first_to_act(self,seat_number):
        self.token.seat_id=seat_number


    def deal_holdcards(self):
        dealer_event_data={
            "DEALER_EVENT_TYPE": "DEAL_HOLDCARDS",
            "DEALER_EVENT_TEXT": "dealing holdcards"
        }
        self.table.observer.handle_table_event(table_event_type="DEALER_EVENT",table_event_data=dealer_event_data)

        next_to_deal=self.current_hand.sb_index
        next_to_deal%=len(self.table.seats)

        not_finished_dealing=True
        bu_seat=self.table.seats[self.current_hand.bu_index]
        while not bu_seat.has_cards() :

            card=self.deck.deal()
            card_receiver=self.table.seats[next_to_deal]
            card_receiver.receive_card(card)

            seat_event_text=card_receiver.player_name+"(Seat "+str(card_receiver.seat_id)+") : "+card.__repr__()
            seat_event_data={
                "SEAT_EVENT_TYPE": "RECEIVE_CARD",
                #"SEAT_EVENT_VISIBILITY":"PRIVATE"
                "SEAT_ID":card_receiver.seat_id,
                "CARD_ID":card.card_id,
                "CARD_REPR":card.__repr__(),
                "SEAT_EVENT_TEXT": seat_event_text
                }
            #self.table.observer.handle_seat_event(seat_event_data)

            next_to_deal+=5
            next_to_deal%=len(self.table.seats)
            while self.table.seats[next_to_deal].player_name not in self.current_hand.live_players :
                next_to_deal+=5
                next_to_deal%=len(self.table.seats)

        for s in self.table.seats :
            if s.player and s.player_name in self.current_hand.live_players :
                if s.holdcards[0] and s.holdcards[1] and s.player.holdcards[0] and s.player.holdcards[1] :
                    pr1nt("DEBUG : [deal_holdcards] seat",s.seat_id," ",s.holdcards)
                    pr1nt("DEBUG : [deal_holdcards] name",s.player.player_name," ",s.player.holdcards)
                else :
                    assert False,"DealerError,len(s.player.holdcards)!=2"
                    return False
        pr1nt("DEBUG : [deal_holdcards] finished dealing")
        return True
    def r3port(self):
        for seat in self.table.seats :
                    #pot+=seat.chips_inline
                    if seat.player :
                        pad_len=12-len(seat.player.player_name)
                        state="folded"
                        if seat.player.holdcards and len(seat.player.holdcards)==2:
                            state="live"
                        s="Seat "+str(seat.seat_id)+":"+padl(seat.player.player_name,12)+'behind : '+padl(seat.chips_behind,4)+" inline : "+padl(seat.chips_inline,4)+" "+state
                        pr1nt("DEBUG : [deal_street]: ",s)

    def deal_street(self):
        #pr1nt("DEBUG : [deal_street] current_street=",self.current_hand.current_street)
        hand=self.current_hand
        if hand.current_street=="street_preflop":
            deal_holdcards_success=self.deal_holdcards()
            assert deal_holdcards_success,"Error : [table.advance_hand(hand)] failed to deal holdcards, "
            #assert new_state=="state_await_dealer_open","Error [deal_street] new_state is invalid"
            #hand.state_assign(new_state)
        elif hand.current_street=="street_flop":
            assert len(self.board)==0,"Error : [deal_street(self,hand) failed to deal street_flop, len(self.board)!=0"
            c0=self.deck.deal()
            self.board.append(c0)
            self.board_card_ids[0]=c0.card_id
            c1=self.deck.deal()
            self.board.append(c1)
            self.board_card_ids[1]=c1.card_id
            c2=self.deck.deal()
            self.board.append(c2)
            self.board_card_ids[2]=c2.card_id
            #str_flop="flop"+str(self.board)
            dealer_event_text="dealing flop : "+c0.__repr__()+", "+c1.__repr__()+", "+c2.__repr__()
            dealer_event_data={
                "DEALER_EVENT_TYPE" : "DEAL_FLOP",
                "FLOP_CARD_IDS" : [c0.card_id,c1.card_id,c2.card_id],
                #"FLOP_CARD_REPR" : [c0.__repr__(),c1.__repr__(),c2.__repr__()],
                "DEALER_EVENT_TEXT" : dealer_event_text
            }
            #print("---------",dealer_event_data)
            self.table.observer.handle_table_event(table_event_type="DEALER_EVENT",table_event_data=dealer_event_data)
            #s="DEBUG :[deal_street(self,hand) ]: "+str(self.board)
            #pr1nt(s)
        elif hand.current_street=="street_turn":
            assert len(self.board)==3,"Error : [deal_street(self,hand) failed to deal street_turn, len(self.board)!=3"
            turn_card=self.deck.deal()
            self.board.append(turn_card)
            self.board_card_ids[3]=turn_card.card_id

            dealer_event_text="dealing turn : "+turn_card.__repr__()
            dealer_event_data={
                "DEALER_EVENT_TYPE" : "DEAL_TURN",
                "TURN_CARD_ID" : turn_card.card_id,
                #"TURN_CARD_REPR" : turn_card.__repr__(),
                "DEALER_EVENT_TEXT" : dealer_event_text
                }
            self.table.observer.handle_table_event(table_event_type="DEALER_EVENT",table_event_data=dealer_event_data)
                        #s="DEBUG :[deal_street(self,hand) ]: "+str(self.board)
        elif hand.current_street=="street_river":
            assert len(self.board)==4,"Error : [deal_street(self,hand) failed to deal street_turn, len(self.board)!=4"
            river_card=self.deck.deal()
            self.board.append(river_card)
            self.board_card_ids[4]=river_card.card_id

            dealer_event_text="dealing river : "+river_card.__repr__()
            dealer_event_data={
                "DEALER_EVENT_TYPE" : "DEAL_RIVER",
                "RIVER_CARD_ID" : river_card.card_id,
                #"RIVER_CARD_REPR" : river_card.__repr__(),
                "DEALER_EVENT_TEXT" : dealer_event_text
                }
            self.table.observer.handle_table_event(table_event_type="DEALER_EVENT",table_event_data=dealer_event_data)
        else :
            e="Error : [dealer.deal_street] unreachable, "+hand.current_street
            assert False,e

    def get_target_pot(self):
        if len(self.pots)==0 :
            new_pot_id=len(self.pots)
            new_pot=Pot(new_pot_id)
            pr1nt("DEBUG : [dealer.get_target_pot] creating first pot")
            return new_pot
        else :
            last_pot=self.pots.pop()
            pr1nt("DEBUG : [dealer.get_target_pot] popping pot from self.pots")
            if last_pot.is_closed :
                pr1nt("DEBUG : [dealer.get_target_pot] pot.is_closed==True, pushing back")
                self.pots.append(last_pot)
                new_pot_id=len(self.pots)
                new_pot=Pot(new_pot_id)
                pr1nt("DEBUG : [dealer.get_target_pot] creating new side_pot")
                return new_pot
            else :
                return last_pot
        assert False,"unreachable"

    def assign_pot(self):

        assert len(self.pots)>0,"oops"
        pot_to_assign=self.pots.pop(0)

        self.sum_pots_assigned+=pot_to_assign.total_amount
        self.num_pots_assigned+=1
        pr1nt("DEBUG : [assign_pot] pot_id : ",pot_to_assign.pot_id," total : ",pot_to_assign.total_amount)

        assert len(pot_to_assign.seat_ids)>0,"can not assign, pot.seat_ids is empty"
        if len(pot_to_assign.winner_results)==0 :
            assert len(pot_to_assign.seat_ids)==1,"logic fail"
        if len(pot_to_assign.winner_results)>0 :
            assert len(pot_to_assign.winner_results)==len(pot_to_assign.seat_ids),"integrity error, len(evaluation_results) > len(assignment_seat_ids)"

        #TODO : handle the odd chip ruling properly. this is somewhat random atm.
        #if len(pot_to_assign.seat_ids)>1 :
        #    print("split pot ! seat_ids : ",pot_to_assign.seat_ids," results : ",pot_to_assign.winner_results)
        #    time.sleep(3)

        transactions={}
        for seat_id in pot_to_assign.seat_ids :
            transactions.setdefault(seat_id)
        share=pot_to_assign.total_amount//len(pot_to_assign.seat_ids)
        for seat_id in pot_to_assign.seat_ids :
            transactions[seat_id]=share
            pot_to_assign.total_amount-=share
        #odd chip handling
        for seat_id in pot_to_assign.seat_ids :
            if pot_to_assign.total_amount>0 :
                pot_to_assign.total_amount-=1
                transactions[seat_id]+=1
            else :
                break

        if len(pot_to_assign.winner_results)==0:
            self.table.seats[pot_to_assign.seat_ids[0]].won_without_showdown+=1
        elif len(pot_to_assign.winner_results)==1 :
            self.table.seats[pot_to_assign.seat_ids[0]].won_at_showdown+=1
        elif len(pot_to_assign.winner_results)>1 :
            for seat_id in pot_to_assign.seat_ids :
                self.table.seats[seat_id].split_pots+=1
        else :
            assert False,"logic fail 3"

        assignment_summary=[]
        pot_id_copy=pot_to_assign.pot_id
        for seat_id in pot_to_assign.seat_ids :
            self.table.seats[seat_id].chips_behind+=transactions[seat_id]
            self.table.seats[seat_id].pot_assign_count+=1
            player_name=self.table.seats[seat_id].player_name
            pot_id=pot_to_assign.pot_id
            evaluation_result="no_showdown"
            for result in pot_to_assign.winner_results :
                id,category_text,five_card_hand,score=result
                if seat_id==id :
                    evaluation_result=result
                    break
            seat_summary={"seat_id":seat_id,"player_name":player_name,"pot_id":pot_id,"award":transactions[seat_id],"result":str(evaluation_result)}
            assignment_summary.append(seat_summary)
        assert pot_to_assign.total_amount==0,"integrity error"
        del pot_to_assign

        #NOTE : it might be a better approach to handle this with multiple seat_events.
        #       i feel like doing it as a single batch event to unpack clientside
        #       makes synchronous animation of split pot assignment easier.
        #       that said, its debatable if that yields visual benefits in the first place.

        pot_event_data={
            "POT_EVENT_TYPE" : "POT_ASSIGN",
            "POT_ID": pot_id_copy,
            "DETAILS": assignment_summary,
            "POT_EVENT_TEXT": ""
        }
        self.table.observer.handle_table_event(table_event_type="POT_EVENT",table_event_data=pot_event_data)
        time.sleep(0.5)

    def perform_transactions(self,transaction_list):
        target_pot=self.get_target_pot()
        assert target_pot,"target_pot is None"
        pr1nt("DEBUG : [dealer] perform_transactions")

        pot_event_data={
            "POT_EVENT_TYPE" : "POT_COLLECT",
            "TARGET_POT_ID" : target_pot.pot_id,
            "TRANSACTION_LIST" : transaction_list.copy()
        }
        #pr1nt("DEBUG : [dealer.perform_transactions] created pot_event_data")

        for transaction_id,transaction in enumerate(transaction_list) :
            pr1nt("")
            pr1nt("DEBUG : [perform_transactions] transaction_id : ",transaction_id)
            seat_id=transaction["seat_id"]
            assert transaction["is_live"]==True or transaction["is_live"]==False, "transaction invalid, field 'is_live' is not a boolean value"
            if seat_id not in target_pot.seat_ids and transaction["is_live"]==True :
                    target_pot.seat_ids.append(seat_id)
                    pr1nt("DEBUG : [perform_transactions] registering  [POT_ID :",target_pot.pot_id," , SEAT_ID : ",seat_id,"]")

            is_live=""
            if transaction["is_live"]==True :
                is_live="live"
            elif transaction["is_live"]==False :
                is_live="dead"
            else :
                assert False,"field 'is_live' is not a boolean"


            pr1nt("DEBUG : [perform_transactions] target_pot.total_amount : ",target_pot.total_amount)
            pr1nt("DEBUG : [perform_transactions] seat_id : ",seat_id," ,chips_inline == ",self.table.seats[seat_id].chips_inline)
            pr1nt("DEBUG : [perform_transactions] seat_id : ",seat_id,", ",is_live,", chips_inline -= ",transaction["amount"])
            self.table.seats[seat_id].chips_inline-=transaction["amount"]



            pr1nt("DEBUG : [perform_transactions] total_amount += ",transaction["amount"])
            target_pot.total_amount+=transaction["amount"]
            pr1nt("DEBUG : [perform_transactions] total_amount == ",target_pot.total_amount)
            pr1nt("DEBUG : [perform_transactions] seat_id : ",seat_id," ,chips_inline == ",self.table.seats[seat_id].chips_inline)




        self.pots.append(target_pot)
        return pot_event_data

    def all_pots_have_assigment_seat_ids(self):
        for pot in self.pots :
            if len(pot.assignment_seat_ids)==0 :
                return False
        return True

    def advance_hand(self):

        if self.current_hand.current_state=="state_uninitialized":
            init_success=self.initialize_hand(hand)
            assert init_success,"Error : [table.advance_hand(hand)] failed to initialized hand"
            self.current_hand.state_assign("state_initialized")

        elif self.current_hand.current_state=="state_initialized":
            self.current_hand.state_assign("state_await_dealer_cards")

        elif self.current_hand.current_state=="state_await_dealer_cards":
            self.current_hand.street_advance()
            self.deal_street()
            self.current_hand.state_assign("state_await_dealer_open")

        elif self.current_hand.current_state=="state_await_dealer_open":
            e="Error : [dealer.advance_hand] valueError,hand.current_street["+self.current_hand.current_street+"] is invalid"
            assert self.current_hand.current_street not in self.current_hand.streets_pending,e
            for seat in self.table.seats :
                seat.had_option=False
            if self.current_hand.current_street=="street_preflop" :
                self.action_is_up_to=2
                self.to_raise=4
            else :
                self.to_raise=8
                self.action_is_up_to=0
            self.limit_raises=2
            self.set_first_to_act(self.current_hand.bb_index) #off by one cause of reasons
            self.token.advance()
            self.action_is_opened=False
            self.current_hand.state_assign("state_betting_open")

        elif self.current_hand.current_state=="state_betting_open":
            self.prepare_token()
            adress=self.table.seats[self.token.seat_id]


            seat_event_data={
                "SEAT_EVENT_TYPE" : "SET_FOCUS_SEAT",
                "SEAT_ID" : adress.seat_id
                }

            self.table.observer.handle_table_event(table_event_type="SEAT_EVENT",table_event_data=seat_event_data)
            time.sleep(1.0)
            adress.receive_token(self.token)

            self.receive_token(self.token)

            if self.action_should_close():
                self.action_is_closed=True
                self.current_hand.state_assign("state_betting_closed")
                self.table.observer.handle_table_event(table_event_type="SEAT_EVENT",table_event_data=seat_event_data)
            else :
                self.token.advance()

        elif self.current_hand.current_state=="state_betting_closed":

            #this is intentionally not specified as a seat event because of reasons.
            dealer_event_data={
                "DEALER_EVENT_TYPE" : "UNSET_FOCUS_ALL",
                "DEALER_EVENT_INFO" : "if you can read this then you should at least remove the focus seat flags"
            }
            self.table.observer.handle_table_event(table_event_type="DEALER_EVENT",table_event_data=dealer_event_data)
            #s="Betting round ["+hand.current_street+"] Finished"
            #inline_sum=0
            #for seat in self.table.seats :
            #    inline_sum+=seat.chips_inline
            #if inline_sum>0 :
            self.current_hand.state_assign("state_await_pot_consolidation")
            #else :
            #   self.current_hand.state_assign("state_pot_consolidation_done")

        elif self.current_hand.current_state=="state_await_pot_consolidation":

            #################################################################################################################
            #                                                                                                               #
            #              due to the complexity of the transaction logic i went for a comment block.                       #
            #              sorry for the inconvenience.  the actual "beef"-lines_of_code are very few                       #
            #                                                                                                               #
            #################################################################################################################
            #                                                                                                               #
            #       apparently even commercial poker sites provide incorrect and/or flawed information on the sidepot rules #
            #       though in production software their implementations are done correctly, (compliance_with(rules)==true)  #
            #       wikipedia is not incorrect, but doesnt cover the rules sufficiently                                     #
            #       TODO : link to proper, comprehensive ruling resource                                                    #
            #                                                                                                               #
            #################################################################################################################
            #                                                                                                               #
            # this codeblock will be reached multiple times per betting round. it iterates as long as theres a chip inline  #
            # possible outcomes : "state_await_pot_consolidation" (unchanged) , "state_pot_consolidation_done"              #                                     #
            #                                                                                                               #
            # each time it will :                                                                                           #
            #                                                                                                               #
            #       EITHER : merge the inline chips to the "target pot" (see below)                                         #
            #       OR : return inline chips, if theres nothing to merge                                                    #
            #                                                                                                               #
            # the "target pot" will be  :                                                                                   #
            #                                                                                                               #
            #       EITHER : created, if pots[] is empty     (usually after the preflop betting round)                      #
            #       OR : popped from pots[] if not empty     (usually on the flop, unless there was no action)              #
            #           if the popped pot.is_closed          (sidepotting is required, logic lives @PotManager)             #
            #               ->  push back                                                                                   #
            #               ->  create pot, use as target                                                                   #
            #           if the popped pot is not closed                                                                     #
            #               ->  use as target_pot                                                                           #
            #                                                                                                               #
            # after transactions are done the target pot :                                                                  #
            #       SOMETIMES : must beclosed immediatly,   (if theres >1 seats with chips inline left at the table)        #
            #       ALWAYS : pushed back into pots[],       (close if needed, then push back)                               #
            #                                                                                                               #
            # if theres exactly 1 seat left at the table with chips inline :                                                #
            #       -inline return.                         (thats either a "no showdown winner",                           #
            #                                                or all other players are all_in and have been covered)         #
            #                                                                                                               #
            #################################################################################################################

            inline_sum=0
            for seat in self.table.seats :
                inline_sum+=seat.chips_inline
            pr1nt("DEBUG : [dealer] pot_consolidation, inline_sum : ",inline_sum)
            if inline_sum==0 :
                self.current_hand.state_assign("state_pot_consolidation_done")
                pr1nt("DEBUG : [dealer] state_pot_consolidation_done")
            elif inline_sum<0:
                assert False,"epic pot_man fail, inline_sum<0"
            else :
                pr1nt("DEBUG : [dealer] managing inline chips for potting/inline_return")
                pot_man=PotManager()
                pot_man.read_seats(self.table.seats)

                action_name=pot_man.get_required_action_name()
                pr1nt("DEBUG : [dealer] action_name=='",action_name,"'")
                if action_name=="pot_collect":

                    list_transactions=pot_man.get_transaction_list()
                    #pr1nt("DEBUG : [dealer] list_transactions : ")
                    #ppr1nt("DEBUG : [dealer]",list_transactions)
                    pot_event_data=self.perform_transactions(list_transactions)
                    self.table.observer.handle_table_event(table_event_type="POT_EVENT",table_event_data=pot_event_data)
                    time.sleep(0.75)
                    #as players have a million chips ... the side_potting rule is not the probem.
                    #
                    #num_all_in_players_with_chips=0
                    #for seat in self.table.seats :
                    #    if seat.chips_inline>0 and seat.has_cards() and seat.is_all_in==True:
                    #        pot=self.pots.pop()
                    #        pot.is_closed=True
                    #        self.pots.append(pot)



                elif action_name=="inline_return":
                    #TODO : extract inline booking away from here
                    assert len(pot_man.seats_with_chips_inline)==1,"inline return fail"
                    seat=pot_man.seats_with_chips_inline.pop()
                    amount=seat.chips_inline

                    pr1nt("DEBUG : [dealer] inline return")
                    pr1nt("DEBUG : [inline_return] seat_id : ",seat.seat_id,", inline : ",seat.chips_inline,", behind : ",seat.chips_behind)
                    seat.chips_behind+=amount
                    seat.chips_inline-=amount
                    pr1nt("DEBUG : [inline_return] inline -= ",amount,", behind += : ",amount)
                    pr1nt("DEBUG : [inline_return] seat_id : ",seat.seat_id,", inline : ",seat.chips_inline,", behind : ",seat.chips_behind)
                    self.table.seats[seat.seat_id].inline_return_count+=1

                    seat_event_data={
                        "SEAT_EVENT_TYPE" : "INLINE_RETURN",
                        "SEAT_ID": seat.seat_id,
                        "AMOUNT": amount,
                        }
                    self.table.observer.handle_table_event(table_event_type="SEAT_EVENT",table_event_data=seat_event_data)
                    time.sleep(0.5)

                else :
                    e="invalid action_name : "+str(action_name)
                    assert False,e
                del pot_man

        elif self.current_hand.current_state=="state_pot_consolidation_done":
            #this has 3 possible outcomes :
                    #"state_await_pot_assignment", foldymoldy all around, won before showdown
                    #"state_await_dealer_cards", keep going, we are not done playing the last street.
                    #"state_await_showdown" , we are done. showtime
            seats_with_cards=[]
            for seat in self.table.seats :
                if seat.has_cards() :
                    seats_with_cards.append(seat)
            assert len(self.current_hand.live_players)==len(seats_with_cards),"integrity error, mismatch : len(seats_with_cards) != len(hand.live_players)"
            assert len(self.current_hand.live_players)>0,"integrity error"
            if len(self.current_hand.live_players)==1 :
                assert len(self.pots)==1,"integrity error"
                seats_with_cards=[]
                for seat in self.table.seats :
                    if seat.has_cards() :
                        seats_with_cards.append(seat)
                assert len(seats_with_cards)==1,"integrity_error"

                #self.pots[0].seat_ids.append(seats_with_cards[0].seat_id)

                self.current_hand.state_assign("state_await_pot_assignment")
            elif self.current_hand.current_street=="street_river":
                self.current_hand.state_assign("state_await_showdown")
            else :
                #i was about to put the line below, which should error out. TODO : test it
                #hand.state_assign("state_await_dealer_open")
                self.current_hand.state_assign("state_await_dealer_cards")

        elif self.current_hand.current_state=="state_await_pot_assignment" :
            pr1nt("DEBUG : [dealer] pot assignment")
            if len(self.pots)>0 :
                self.assign_pot()
                time.sleep(0.75)
            elif len(self.pots)==0:
                self.current_hand.state_assign("state_hand_completed")
                self.num_hands_played+=1
            else :
                assert False,"oops, unreachable"

        elif self.current_hand.current_state=="state_await_showdown":
            seats_with_cards=[]
            seat_ids_with_cards=[]
            for seat in self.table.seats :
                if seat.has_cards() :
                    seats_with_cards.append(seat)
                    seat_ids_with_cards.append(seat.seat_id)
                #else :
                #    for pot in self.pots :
                #        #assert seat_id in pot.seat_ids,"seat folded, but was not listed in pot.seat_ids. thats really bad"
                #        if seat.seat_id in pot.seat_ids :
                #            pot.seat_ids.remove(seat_id)
            for seat_id in seat_ids_with_cards :
                self.table.seats[seat_id].went_to_showdown+=1
            for pot in self.pots :
                for seat_id in pot.seat_ids:
                    assert seat_id in seat_ids_with_cards,"integrity error - seat_id in pot that should not be there"

            #sanity check
            for pot in self.pots :
                for seat_id in pot.seat_ids :
                    assert self.table.seats[seat_id].has_cards(),"integrity error"

            evaluation_results=[]
            flop=self.board[0],self.board[1],self.board[2]
            turn=self.board[3]
            river=self.board[4]
            #scores=[]
            #for seat_with_cards in seats_with_cards :
            #    holdcards=[]
            #    holdcards.append(seat_with_cards.holdcards[0])
            #    holdcards.append(seat_with_cards.holdcards[1])
            #    category_text,score,five_card_hand=determine_best_combination(flop,turn,river,holdcards)
            #    result_set=(seat_with_cards.seat_id,score,category_text,five_card_hand)
            #    evaluation_results.append(result_set)
            #    scores.append(score)

            #print("evaluation_results : ",evaluation_results)
            #time.sleep(3)
            #scores.sort()
            #TODO : rewrite this using "izip()".

            for pot in self.pots :
                best_score=0
                for seat_id in pot.seat_ids :
                    holdcards=[self.table.seats[seat_id].holdcards[0],self.table.seats[seat_id].holdcards[1]]
                    category_text,five_card_hand,score=determine_best_combination(flop,turn,river,holdcards)
                    if score>=best_score :
                        best_score=score

                looser_seat_ids=[]
                for seat_id in pot.seat_ids :
                    holdcards=[self.table.seats[seat_id].holdcards[0],self.table.seats[seat_id].holdcards[1]]
                    category_text,five_card_hand,score=determine_best_combination(flop,turn,river,holdcards)
                    result=seat_id,category_text,five_card_hand,score
                    if score<best_score :
                        looser_seat_ids.append(seat_id)
                    else :
                        pot.winner_results.append(result)
                for looser_seat_id in looser_seat_ids :
                    pot.seat_ids.remove(looser_seat_id)


            #while self.all_pots_have_assigment_seat_ids()==False :
            #    matching_score=scores.pop()
            #    matched_evaluation_results=[]
            #    matched_seat_ids=[]
            #    for result in evaluation_results :
            #        seat_id,score,categoy_text,five_card_hand=result
            #        if score==matching_score :
            #            matched_evaluation_results.append(result)
            #            matched_seat_ids.append(seat_id)
            #    for pot in self.pots :
            #        if len(pot.assignment_seat_ids)==0 :
            #            assert len(pot.assignment_evaluation_results)==0,"fail"
            #            for r in matched_evaluation_results :
            #                pot.assignment_evaluation_results.append(r)
            #            for seat_id in matched_seat_ids:
            #                pot.assignment_seat_ids.append(seat_id)
            #                assert seat_id in pot.seat_ids,"fail"
            self.current_hand.state_assign("state_await_pot_assignment")



        elif self.current_hand.current_state=='state_hand_completed':
            self.last_hand==self.current_hand
            for card in self.board:
                self.muck.append(card)
            self.board.clear()
            for board_card_id in self.board_card_ids :
                board_card_id=-1
            for seat in self.table.seats :
                if seat.has_cards() :
                    cards=seat.get_cards()
                    seat.muck_cards()
                    for card in cards :
                        self.muck.append(card)
            self.table_report()
            self.initialize_hand()
            #assert False,"self.initialize_hand() done"

        else :
            e="Error : [dealer.advance_hand] unhandled case["+hand.current_state+"]"
            assert False,e
