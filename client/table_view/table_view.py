import sys; sys.dont_write_bytecode = True
import os
sys.path.append(os.getcwd() + '/..')
from common.common import *
assert COMMON_IMPORTS,"ERROR : [__main__] missing import"
import pyray
from math import sin,cos
import random
from common.debug_department import DONK_WARNING,DONK_ERROR,DONK_DEBUG
from common.view_model_factory import *
from pprint import pprint
from table_view.seat_widget import SeatWidget
from table_view.option_widget import OptionWidget
from table_view.chat_widget import ChatWidget
from table_view.pot_widget import PotWidget
from table_view.card_widget import CardWidget
from table_view.player_info_widget import PlayerInfoWidget
from table_view.table_avatars import TableAvatars
from table_view.animation_seat_chips_inline_put import AnimationSeatChipsInlinePut
from table_view.animation_seat_chips_inline_return import AnimationSeatChipsInlineReturn
from table_view.animation_pot_collect_transfer import AnimationPotCollectTransfer
from table_view.animation_pot_assign_transfer import AnimationPotAssignTransfer


class TableView():
    def __init__(self,renderer,avatar_set,test_mode=False,window_title="",debug_info=""):
        self.test_mode=test_mode
        self.renderer=renderer

        self.table_window_title_debug_info=debug_info
        self.table_window_title=window_title
        self.avatars=TableAvatars()
        self.animations_seat_chips_inline_put=[]
        self.animations_seat_chips_inline_return=[]
        self.animations_pot_collect_transfer=[]
        self.animations_pot_assign_transfer=[]
        #self.inline_return_animations=[]

        self.table_view_data=None#=ViewModelFactory.create_table_view_model()
        self.table_meta=None
        self.seat_components=None
        self.player_components=None
        self.hand_components=None
        self.pot_components=None
        self.dealer_components=None

        self.num_seats=None
        self.stakes=None
        self.table_id=None
        self.table_name=None
        self.game_type=None
        self.focus_seat_highlight=False
        self.focus_seat_timer_t0=time.time()
        self.focus_seat_timer_t1=time.time()+1.5

        self.window_title_base=""

        self.pot_widgets=[]
        self.seat_widgets=[]
        self.player_info_widgets=[]
        self.board_card_widgets=[]
        seat_open_avatar=self.avatars.get_overlay("overlay_seat_open")
        for i in range(5) :
            self.board_card_widgets.append(CardWidget(i))
        for i in range(6):
            card0=CardWidget(5+i*2)
            card1=CardWidget(5+i*2+1)
            self.seat_widgets.append(SeatWidget(i,card0,card1))
        for seat_widget in self.seat_widgets :
            seat_widget.default_avatar=seat_open_avatar

        for i in range(6):
            self.player_info_widgets.append(PlayerInfoWidget(i))
        for i in range(5) :
            self.pot_widgets.append(PotWidget(i))



        self.board_card_ids=[-1,-1,-1,-1,-1]
        self.option_widget=OptionWidget(self.renderer.option_button_font)

        self.chat_widget=ChatWidget(self.renderer.chat_font)
        self.reset_flag=False
        if self.test_mode==True:
            self.test_table_reset()


    def update_inline_put_animations(self):
        delete_list=[]
        for anim in self.animations_seat_chips_inline_put :
            if anim.is_running() and anim.is_pending()==False:
                anim.update_self()
            if anim.is_finished() :
                delete_list.append(anim)
        while len(delete_list)>0 :
            a=delete_list.pop()
            self.animations_seat_chips_inline_put.remove(a)
            del a

    def update_inline_return_animations(self):
        delete_list=[]
        for anim in self.animations_seat_chips_inline_return :
            if anim.is_running() and anim.is_pending()==False:
                anim.update_self()
            if anim.is_finished() :
                delete_list.append(anim)
        while len(delete_list)>0 :
            a=delete_list.pop()
            self.animations_seat_chips_inline_return.remove(a)
            del a

    def update_pot_collect_transfer_animations(self):
        delete_list=[]
        moment_of_time=time.time()
        for anim in self.animations_pot_collect_transfer :
            if anim.is_running() and anim.is_pending()==False:
                anim.update_self(moment_of_time)
            if anim.is_finished() :
                delete_list.append(anim)
        while len(delete_list)>0 :
            a=delete_list.pop()
            self.animations_pot_collect_transfer.remove(a)
            del a

    def update_pot_assign_transfer_animations(self):
        delete_list=[]
        moment_of_time=time.time()
        for anim in self.animations_pot_assign_transfer :
            if anim.is_running() and anim.is_pending()==False:
                anim.update_self(moment_of_time)
            if anim.is_finished() :
                delete_list.append(anim)

        while len(delete_list)>0 :
            a=delete_list.pop()
            self.animations_pot_assign_transfer.remove(a)
            del a


    def update_animations(self):
        self.update_inline_put_animations()
        self.update_inline_return_animations()
        self.update_pot_collect_transfer_animations()
        self.update_pot_assign_transfer_animations()

    def draw_animations(self):

        for index,anim in enumerate(self.animations_seat_chips_inline_put) :

            rel_x,rel_y,value=anim.get_render_params()
            if value>0 :
                self.renderer.draw_chip_stack(rel_x,rel_y,value,sort_by_value=False)

        for index,anim in enumerate(self.animations_seat_chips_inline_return) :

            rel_x,rel_y,value=anim.get_render_params()
            if value>0 :
                self.renderer.draw_chip_stack(rel_x,rel_y,value,sort_by_value=False)

        for index,anim in enumerate(self.animations_pot_collect_transfer) :

            rel_x,rel_y,value=anim.get_render_params()
            if value>0 :
                self.renderer.draw_chip_stack(rel_x,rel_y,value,sort_by_value=False)

        for index,anim in enumerate(self.animations_pot_assign_transfer) :

            rel_x,rel_y,value=anim.get_render_params()
            if value>0 :
                self.renderer.draw_chip_stack(rel_x,rel_y,value,sort_by_value=True)
        #end_of draw_animiations()

    def push_pot_collect_transfer_animations(self,anims):
        moment_of_time=time.time()
        for anim in anims :
            anim.set_duration(0.5)
            anim.start_at(moment_of_time)
            self.animations_pot_collect_transfer.append(anim)

    def push_pot_assign_transfer_animations(self,anims):
        moment_of_time=time.time()
        for anim in anims :
            anim.set_duration(0.5)
            anim.start_at(moment_of_time)
            self.animations_pot_assign_transfer.append(anim)

    def push_seat_chips_inline_put_animation(self,anim):
        anim.set_duration(0.5)
        anim.start_now()
        self.animations_seat_chips_inline_put.append(anim)

    def push_seat_chips_inline_return_animation(self,anim):
        anim.set_duration(0.5)
        anim.start_now()
        self.animations_seat_chips_inline_return.append(anim)


    def create_test_seat_chips_inline_put_animation(self,seat_id,value):
        anim=AnimationSeatChipsInlinePut(self.player_info_widgets[seat_id],self.seat_widgets[seat_id],value)
        return anim

    def create_test_seat_chips_inline_return_animation(self,seat_id,value):
        anim=AnimationSeatChipsInlineReturn(self.player_info_widgets[seat_id],self.seat_widgets[seat_id],value)
        return anim

    def create_test_pot_collect_animation(self,pot_widget,value):
        list_transfer_animations=[]
        for seat_widget in self.seat_widgets :
            if seat_widget.chips_inline>=value :
                transfer_animation=AnimationPotCollectTransfer(pot_widget,seat_widget,value)
                list_transfer_animations.append(transfer_animation)
        self.push_pot_collect_transfer_animations(list_transfer_animations)

    def create_test_pot_assign_animation(self,pot_widget,player_info_widgets,seat_widgets,value):
        list_transfer_animations=[]
        assert pot_widget.value==value,"pot assign fail, value mismatch"
        for i in range(len(seat_widgets)):
            seat_widget=seat_widgets[i]
            player_info_widget=player_info_widgets[i]
            transfer_animation=AnimationPotAssignTransfer(pot_widget,player_info_widget,seat_widget,value)
            list_transfer_animations.append(transfer_animation)
            print("DEBUG : [table_view.create_test_pot_assign_animation] seat_id=",seat_widget.seat_id,", value=",value)
        self.push_pot_assign_transfer_animations(list_transfer_animations)

    def handle_table_event(self,table_event_type,table_event_data):
        assert table_event_type is not None,"cant handle table_event_type : None"
        assert table_event_data is not None,"cant handle table_event_data : None"
        if table_event_type=="DEALER_EVENT":
            self.handle_dealer_event_data(table_event_data)
        elif table_event_type=="POT_EVENT":
            self.handle_pot_event_data(table_event_data)
        elif table_event_type=="SEAT_EVENT":
            self.handle_seat_event_data(table_event_data)
        else :
            e="unexpected table_event_type '"+str(table_event_type)+"'"
            assert False,e

    def handle_dealer_event_data(self,dealer_event_data):
        dealer_event_type=dealer_event_data.get("DEALER_EVENT_TYPE")
        #TODO : implement implicit event side effects
        if dealer_event_type=="UNSET_FOCUS_ALL":
            self.set_focus_seat_position(-1)
        elif dealer_event_type=="DEAL_HOLDCARDS" :
            print("TODO : handle dealer_event_text, ",dealer_event_data.get("DEALER_EVENT_TEXT"))
            self.board_card_ids[0]=-1
            self.board_card_ids[1]=-1
            self.board_card_ids[2]=-1
            self.board_card_ids[3]=-1
            self.board_card_ids[4]=-1
            for seat_widget in self.seat_widgets :
                seat_widget.holdcard_ids[0]=-1
                seat_widget.holdcard_ids[1]=-1

        elif dealer_event_type=="DEAL_FLOP" :
            flop_card_ids=dealer_event_data.get("FLOP_CARD_IDS")
            self.board_card_ids[0]=flop_card_ids[0]
            self.board_card_ids[1]=flop_card_ids[1]
            self.board_card_ids[2]=flop_card_ids[2]
            print("TODO : handle dealer_event_text, ",dealer_event_data.get("DEALER_EVENT_TEXT"))
        elif dealer_event_type=="DEAL_TURN" :
            turn_card_id=dealer_event_data.get("TURN_CARD_ID")
            #TODO : handle field "DEALER_EVENT_TEXT"
            print("TODO : handle dealer_event_text, ",dealer_event_data.get("DEALER_EVENT_TEXT"))
            self.board_card_ids[3]=turn_card_id
        elif dealer_event_type=="DEAL_RIVER" :
            river_card_id=dealer_event_data.get("RIVER_CARD_ID")
            #TODO : handle field "DEALER_EVENT_TEXT"
            print("TODO : handle dealer_event_text, ",dealer_event_data.get("DEALER_EVENT_TEXT"))
            self.board_card_ids[4]=river_card_id
        else :
            print("DEBUG : [dealer_event_data] : ",dealer_event_data)
            assert False,"NOT_IMPLEMENTED, dealer_event_type"



    def handle_pot_event_data(self,pot_event_data):

        if pot_event_data["POT_EVENT_TYPE"]=="POT_COLLECT" :#
            pot_id=pot_event_data["TARGET_POT_ID"]
            transaction_list=pot_event_data["TRANSACTION_LIST"]

            print(pot_event_data)
            list_transfer_animations=[]
            for transaction in transaction_list :
                target_seat_id=transaction.get("seat_id")
                value=transaction.get("amount")
                pot_widget=self.pot_widgets[pot_id]
                seat_widget=self.seat_widgets[target_seat_id]
                transfer_animation=AnimationPotCollectTransfer(pot_widget,seat_widget,value)
                list_transfer_animations.append(transfer_animation)
            self.push_pot_collect_transfer_animations(list_transfer_animations)

        elif pot_event_data["POT_EVENT_TYPE"]=="POT_ASSIGN" :
            pot_id=pot_event_data.get("POT_ID")
            assignments=pot_event_data.get("DETAILS")

            list_transfer_animations=[]
            for assignment in assignments :
                seat_id=assignment.get("seat_id")
                value=assignment.get("award")
                #TODO : handle field 'result'
                #TODO : handle field 'player_name'
                #TODO : handle parent field 'POT_EVENT_TEXT'
                pot_widget=self.pot_widgets[pot_id]#
                seat_widget=self.seat_widgets[seat_id]
                player_info_widget=self.player_info_widgets[seat_id]
                transfer_animation=AnimationPotAssignTransfer(pot_widget,player_info_widget,seat_widget,value)
                list_transfer_animations.append(transfer_animation)
            self.push_pot_assign_transfer_animations(list_transfer_animations)

        else :
            print("DEBUG : [pot_event_data] ",pot_event_data)
            assert False,"NOT_IMPLEMENTED"
        #{
        #'POT_EVENT_TYPE': 'POT_COLLECT',
        #'TARGET_POT_ID': 0,
        #'TRANSACTION_LIST': [
        #    {'is_live': True, 'seat_id': 1, 'amount': 8},
        #    {'is_live': True, 'seat_id': 2, 'amount': 8},
        #    {'is_live': True, 'seat_id': 4, 'amount': 8}]
        #    }


    def handle_seat_event_data(self,seat_event_data):
        seat_event_type=seat_event_data.get("SEAT_EVENT_TYPE")
        seat_id=seat_event_data.get("SEAT_ID")
        seat_widget=self.seat_widgets[seat_id]
        player_info_widget=self.player_info_widgets[seat_id]
        if seat_event_type=="SET_FOCUS_SEAT" :
            self.set_focus_seat_position(seat_id)
        elif seat_event_type=="PLAYER_JOIN":
            print("DEBUG : [table.handle_seat_event_data] NOT_IMPLEMENTED, PLAYER_JOIN")
        elif seat_event_type=="FOLD":
            fold_overlay=self.avatars.get_overlay("overlay_fold")
            seat_widget.set_temporary_overlay(fold_overlay)
            seat_widget.holdcard_ids[0]=-1
            seat_widget.holdcard_ids[1]=-1
        elif seat_event_type=="CHECK":
            check_overlay=self.avatars.get_overlay("overlay_check")
            seat_widget.set_temporary_overlay(check_overlay)
        elif seat_event_type=="CALL":
            call_overlay=self.avatars.get_overlay("overlay_call")
            seat_widget.set_temporary_overlay(call_overlay)
            value=seat_event_data.get("AMOUNT")
            anim=AnimationSeatChipsInlinePut(player_info_widget,seat_widget,value)
            self.push_seat_chips_inline_put_animation(anim)
        elif seat_event_type=="RAISE":
            raise_overlay=self.avatars.get_overlay("overlay_raise")
            seat_widget.set_temporary_overlay(raise_overlay)
            value=seat_event_data.get("AMOUNT")
            anim=AnimationSeatChipsInlinePut(player_info_widget,seat_widget,value)
            self.push_seat_chips_inline_put_animation(anim)
        elif seat_event_type=="POST":
            post_overlay=self.avatars.get_overlay("overlay_post")
            seat_widget.set_temporary_overlay(post_overlay)
            value=seat_event_data.get("AMOUNT")
            anim=AnimationSeatChipsInlinePut(player_info_widget,seat_widget,value)
            self.push_seat_chips_inline_put_animation(anim)
        elif seat_event_type=="INLINE_RETURN" :
            value=seat_event_data.get("AMOUNT")
            anim=AnimationSeatChipsInlineReturn(player_info_widget,seat_widget,value)
            self.push_seat_chips_inline_return_animation(anim)
        #elif seat_event_type=="RECEIVE_CARD" :
            #card_id=seat_event_data.get("CARD_ID")
            #if seat_widget.holdcard_ids[0]==-1 or seat_widget.holdcard_ids[0]==card_id :
            #    seat_widget.holdcard_ids[0]=card_id
            #elif seat_widget.holdcard_ids[1]==-1 or seat_widget.holdcard_ids[1]==card_id :
            #    seat_widget.holdcard_ids[1]=card_id
            #else :
            #    assert False,"receive card to non empty slot"
        else :
            assert False,"NOT_IMPLEMENTED"
        #seat_event_mes#from draw_chip_stack import *
#class Table():
#    def __init__(self):
#        self.seats=[]
#        for i in range(6):
#            self.seats.append(Seat(i))
#        #self.deck52=Deck52()
#        self.card_ids=[-1,-1,-1,-1,-1]
#
#        self.horizontal_stretch=1.8
#    def get_horizontal_stretch(self):
#        return self.horizontal_stretch
#
#    def draw_parameters(self,font):
#        str_param_0="Tbl.w ="+str(self.horizontal_stretch)
#        pyray.draw_text_ex(font,str_param_0, (30,20) , 20, 0, DEBUG_TEXT_COLOR)
#


        #    print(seat_event_data)
        #    if seat_event_data.

    def slurp(self,table_view_data):
        self.table_view_data=table_view_data
        #pprint(table_view_data)
        self.table_meta=self.table_view_data.get("table_view_meta")
        table_view_components=table_view_data.get("table_view_components")
        self.seat_components=table_view_components.get("seat_components")
        self.hand_components=table_view_components.get("hand_components")
        self.dealer_components=table_view_components.get("dealer_components")
        self.pot_components=table_view_components.get("pot_components")
        self.token_components=table_view_components.get("token_components")
        self.update_seats()
        self.update_dealer()
        self.update_players()
        self.update_token()
        self.update_meta()
        self.update_hand()
        self.update_pots()
        #pprint(self.table_view_data)
    def update_meta(self):
        for attrib in list(self.table_meta.keys()):
            #print("DEBUG : [update_meta] attrib=",attrib," table_meta[attrib]=",self.table_meta[attrib])
            setattr(self,attrib,self.table_meta[attrib])
        table_window_title=self.table_window_title+" "
        table_window_title=self.window_title_base+" "
        table_window_title+="Table : "+self.table_name+" - "+self.game_type+", "+str(self.num_seats)+"max, "+str(self.stakes)
        table_window_title+=" "+self.table_window_title_debug_info

        pyray.set_window_title(table_window_title)
    def update_token(self):
        pass
    def update_hand(self):
        button_seat_id=self.hand_components["bu_index"]
        self.set_dealer_button_position(button_seat_id)

        #pprint(self.hand_components)_

    def update_seats(self):
        for seat_component_index in self.seat_components:
            seat_view_data=self.seat_components[seat_component_index]
            seat_id=seat_view_data["seat_id"]
            seat_widget=self.seat_widgets[seat_id]
            player_id=seat_view_data["player_id"]
            assert player_id is not None,"missing 'player_id' in seat_component"
            if player_id!=seat_widget.player_id :
            #    seat_widget.player_avatar_filename=seat_view_data["player_avatar_filename"]
                seat_widget.player_id=player_id
                new_avatar=self.avatars.get_avatar_by_player_id(player_id)
                seat_widget.set_avatar(new_avatar)
            #assert seat_widget.player_avatar_filename is not None,"missing 'player_avatar_filename' in seat_component"
            player_info_widget=self.player_info_widgets[seat_id]
            seat_widget.chips_inline=seat_view_data["chips_inline"]
            player_info_widget.chips_behind=seat_view_data["chips_behind"]
            #is_occupied
            #"is_sitting_out"=seat_view_data["is_sitting_out"]
            #seat_widget.is_open=seat_view_data["is_open"]
            #"player_id"=seat_view_data["player_id"]
            #"all_in_flag"=seat_view_data["all_in_flag"]
            holdcard_ids=seat_view_data["holdcard_ids"]
            seat_widget.holdcard_ids[0]=holdcard_ids[0]
            seat_widget.holdcard_ids[1]=holdcard_ids[1]
            player_info_widget.player_name=seat_view_data["player_name"]

            #self.player_info_widgets[seat_id].player_name=self.seat_widgets[seat_id].player_name
            #self.player_info_widgets[seat_id].chips_behind=self.seat_widgets[seat_id].chips_behind
            #print(seat_view_data)pot

            #list(self.seat_components.keys()):
            #print("DEBUG : [update_meta] attrib=",attrib," table_meta[attrib]=",self.table_meta[attrib])
            #setattr(self.seats,attrib,self.seat_components[attrib])
    def update_players(self):
        pass
    def update_dealer(self):
        board_card_ids=self.dealer_components["board_card_ids"]
        for idx,board_card_id in enumerate(board_card_ids):
            self.board_card_ids[idx]=board_card_id

    def update_pots(self):
        for pot_widget in self.pot_widgets :
            pot_widget.value=0
        for index,key in enumerate(list(self.pot_components.keys())):
            pot_component=self.pot_components[key]
            pot_id=pot_component["pot_id"]
            assert pot_id is not None
            assert pot_id<=5
            assert pot_id>=int(0)
            #pprint(pot_component)
            pot_value=pot_component["total_amount"]
            assert pot_value is not None
            self.pot_widgets[pot_id].value=pot_value



    def update_self(self):
        if self.test_mode==False :
            if not self.table_view_data :
                return
        if self.test_mode==True :
            names=["Sir Limpalot","Doc. Brown","HAL9001","BetGPT","Bender","TheRealData"]
            for index,player_info_widget in enumerate(self.player_info_widgets) :
                player_info_widget.player_name=names[index]
                #player_info_widget.chips_behind=5000
        for index,board_card_widget in enumerate(self.board_card_widgets) :
            board_card_widget.card_id=self.board_card_ids[index]
        for index,seat_widget in enumerate(self.seat_widgets) :
            seat_widget.card_widgets[0].card_id=seat_widget.holdcard_ids[0]
            seat_widget.card_widgets[1].card_id=seat_widget.holdcard_ids[1]
        self.update_focus_seat_timer()
    def draw_self(self):

        self.renderer.draw_table_shape()
        for board_card_widget in self.board_card_widgets :
            self.renderer.draw_board_card_widget(board_card_widget)
        for seat_widget in self.seat_widgets :
            self.renderer.update_seat_widget_params(seat_widget)
            self.renderer.draw_seat_widget_cards(seat_widget)
        self.update_animations()
        self.draw_animations()
        for player_info_widget in self.player_info_widgets :
            self.renderer.draw_player_info_widget(player_info_widget,self.focus_seat_highlight)
        for seat_widget in self.seat_widgets :
            self.renderer.draw_seat_widget(seat_widget)
            self.renderer.draw_chip_stack(
                seat_widget.chips_inline_rel_x,
                seat_widget.chips_inline_rel_y,
                seat_widget.get_chips_inline(),
                sort_by_value=False
                )
        for pot_widget in self.pot_widgets :
            self.renderer.draw_pot_widget(pot_widget)

        if self.test_mode==True :
            test_items=[
            "test mode hot keys :",
            " ",
            "F1 table reset",
            "F2 button advance",
            "F3 focus seat advance",
            "F4 inline put($42)/return",
            "F5 match(all)/return(all)/collect(all,pot0)/assign(pot0,focus_seat) ",
            "F6 overlay post(focus seat)",
            "F7 overlay fold(focus seat)",
            "F8 overlay check(focus seat)",
            "F9 overlay call(focus seat)",
            "F10 overlay raise(focus seat)"
            ]
            for index,test_item in enumerate(test_items) :
                pyray.draw_text_ex(self.renderer.player_info_font,test_item,(20,14*(1+index)),12,0,pyray.Color(192,172,168,204))
            #pyray.draw_text_ex(self.renderer.player_info_font,test_item,20,20*(1+index),14,pyray.Color(192,172,168,204))

    def set_dealer_button_position(self,seat_id):
        self.dealer_button_position=seat_id
        for seat_widget in self.seat_widgets :
            seat_widget.show_dealer_button=False
            if seat_widget.seat_id==self.dealer_button_position :
                seat_widget.show_dealer_button=True
    def dealer_button_position_advance(self):
        self.dealer_button_position+=5
        self.dealer_button_position%=6
        for seat_widget in self.seat_widgets :
            seat_widget.show_dealer_button=False
            if seat_widget.seat_id==self.dealer_button_position :
                seat_widget.show_dealer_button=True
    def update_focus_seat_timer(self):
        if time.time()>self.focus_seat_timer_t1 :
            if self.focus_seat_highlight==True :
                self.focus_seat_highlight=False
            elif self.focus_seat_highlight==False :
                self.focus_seat_highlight=True
            self.focus_seat_timer_t0=time.time()
            self.focus_seat_timer_t1=time.time()+1.5
    def set_focus_seat_position(self,seat_id):
        self.focus_seat_position=seat_id
        self.focus_seat_highlight=True
        self.focus_seat_timer_t0=time.time()
        self.focus_seat_timer_t1=time.time()+1.5
        for seat_widget in self.seat_widgets :
            seat_widget.has_focus=False
            if seat_widget.seat_id==self.focus_seat_position:
                seat_widget.has_focus=True
        for player_info_widget in self.player_info_widgets :
            player_info_widget.has_focus=False
            if player_info_widget.seat_id==self.focus_seat_position:
                player_info_widget.has_focus=True
    def focus_seat_advance(self):
        self.focus_seat_position+=5
        self.focus_seat_position%=6
        self.set_focus_seat_position(self.focus_seat_position)
        #for seat_widget in self.seat_widgets :
        #    seat_widget.has_focus=False
        #    if seat_widget.seat_id==self.focus_seat_position :
        #        seat_widget.has_focus=True
        #for player_info_widget in self.player_info_widgets :
        #    player_info_widget.has_focus=False
        #    if player_info_widget.seat_id==self.focus_seat_position :
        #        player_info_widget.has_focus=True
    def clear_table(self):
        for pot_widget in self.pot_widgets :
            pot_widget.chip_count=0
        for seat_widget in self.seat_widgets :
            seat_widget.chips_inline=0
            seat_widget.holdcard_ids[0]=-1
            seat_widget.holdcard_ids[1]=-1
        for index,board_card_id in enumerate(self.board_card_ids) :
            self.board_card_ids[index]=-1

    def test_table_reset(self):
        card_ids=[]
        for i in range(52):
            card_ids.append(i)
        random.shuffle(card_ids)
        for index,board_card_id in enumerate(self.board_card_ids) :
            self.board_card_ids[index]=card_ids.pop()
        for player_info_widget in self.player_info_widgets :
            player_info_widget.chips_behind=5000
        for seat_widget in self.seat_widgets :
            seat_widget.holdcard_ids[0]=card_ids.pop()
            seat_widget.holdcard_ids[1]=card_ids.pop()
            seat_widget.chips_inline=0
        for pot_widget in self.pot_widgets :
            pot_widget.chip_count=0#69*(1+pot_widget.pot_id)+(3*pot_widget.pot_id)
        for seat_widget in self.seat_widgets :
            seat_widget.chips_inline=0#42*(1+seat_widget.seat_id)+(3*(1+seat_widget.seat_id))
        self.set_dealer_button_position(0)
        self.set_focus_seat_position(0)
        if self.reset_flag==True :
            self.reset_flag=False
            self.clear_table()
        else :
            self.reset_flag=True


    def test_button_advance(self):
        self.dealer_button_position_advance()
    def test_focus_seat_advance(self):
        self.focus_seat_advance()
    def test_inline_put_return(self):
        seat_id=self.focus_seat_position
        seat_widget=self.seat_widgets[seat_id]
        if seat_widget.chips_inline>0 :
            anim=self.create_test_seat_chips_inline_return_animation(seat_id,seat_widget.chips_inline)
            self.push_seat_chips_inline_return_animation(anim)
            seat_widget.chips_inline=0
        else :
            seat_widget.chips_inline=42
            anim=self.create_test_seat_chips_inline_put_animation(seat_id,seat_widget.chips_inline)
            self.push_seat_chips_inline_put_animation(anim)
    def test_match_return_collect_assign(self):
        test_sum=69*6
        inline_sum=0
        for seat_widget in self.seat_widgets :
            inline_sum+=seat_widget.chips_inline
        #if theres a test_pot -> assign it to the focus seat
        if self.pot_widgets[0].value>0:
            seat_widget=self.seat_widgets[self.focus_seat_position]
            pot_widget=self.pot_widgets[0]
            player_info_widget=self.player_info_widgets[self.focus_seat_position]
            value=pot_widget.value
            print("DEBUG : [table_view.test_match_return_collect_assign] creating_test_pot_assign_animation")
            self.create_test_pot_assign_animation(pot_widget,[player_info_widget],[seat_widget],value)
            player_info_widget.chips_behind+=value
            pot_widget.value=0
        #if all seats.chips_inline are equal -> pot_pollect
        elif inline_sum==test_sum :
            self.pot_widgets[0].value=test_sum

            self.create_test_pot_collect_animation(self.pot_widgets[0],test_sum//6)
            for seat_widget in self.seat_widgets :
                seat_widget.chips_inline=0
            print("DEBUG : [table_view.test_match_return_collect_assing] created test_pot_collect_animation")
            print("DEBUG : [table_view.test_match_return_collect_assing] pot_widget[0].value==",self.pot_widgets[0].value)

        #if all seats.chips inline == 0 -> all seats inline put 69
        elif inline_sum==0 :
            for seat_widget in self.seat_widgets :
                seat_widget.chips_inline=69
                self.player_info_widgets[seat_widget.seat_id].chips_behind-=69
                anim=self.create_test_seat_chips_inline_put_animation(seat_widget.seat_id,69)
                self.push_seat_chips_inline_put_animation(anim)
        #if all seats.chips_inline NOT equal -> all seats inline return
        else :
            for seat_widget in self.seat_widgets :
                anim=self.create_test_seat_chips_inline_return_animation(seat_widget.seat_id,seat_widget.chips_inline)
                seat_widget.chips_inline=0
                self.push_seat_chips_inline_return_animation(anim)


        pass
    def test_overlay_post(self):
        post_overlay=self.avatars.get_overlay("overlay_post")
        self.seat_widgets[self.focus_seat_position].set_temporary_overlay(post_overlay)
    def test_overlay_fold(self):
        fold_overlay=self.avatars.get_overlay("overlay_fold")
        self.seat_widgets[self.focus_seat_position].set_temporary_overlay(fold_overlay)
    def test_overlay_check(self):
        check_overlay=self.avatars.get_overlay("overlay_check")
        self.seat_widgets[self.focus_seat_position].set_temporary_overlay(check_overlay)
    def test_overlay_raise(self):
        raise_overlay=self.avatars.get_overlay("overlay_raise")
        self.seat_widgets[self.focus_seat_position].set_temporary_overlay(raise_overlay)
    def test_overlay_call(self):
        call_overlay=self.avatars.get_overlay("overlay_call")
        self.seat_widgets[self.focus_seat_position].set_temporary_overlay(call_overlay)
