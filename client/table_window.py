import pyray
import time
import os
#from debug_params import debug_params
from common.debug_department import DONK_WARNING,DONK_DEBUG,DONK_ERROR
from table_view.table_view import TableView
from table_view.table_view_renderer import TableViewRenderer
from table_view.color_theme import ColorTheme
#this doesnt belong here
from table_view.card_widget import card_img_filenames,CardIMG
from table_view.chips_widget import ChipSet
from ipc_messaging import WindowMessenger

KEY_F1=290
KEY_F2=291
KEY_F3=292
KEY_F4=293
KEY_F5=294
KEY_F6=295
KEY_F7=296
KEY_F8=297
KEY_F9=298
KEY_F10=299
KEY_ESC=256


def table_window_launch(window_id,table_id,table_name,cfg,child_con):
    con=child_con
    window_id=window_id
    table_id=table_id
    os_is_windows=False
    if os.name=='nt' :
        os_is_windows=True

    print("table_window_launched")
    assert cfg.get("table_window_width") is not None
    assert cfg.get("table_window_height") is not None
    table_window_title=cfg.get("table_window_title")
    assert table_window_title is not None

    pyray.set_trace_log_level(pyray.LOG_ERROR)


    pyray.set_config_flags(pyray.FLAG_WINDOW_RESIZABLE+pyray.FLAG_WINDOW_ALWAYS_RUN+pyray.FLAG_MSAA_4X_HINT) #enum, val=4

    table_window_debug_info="(window_id : "+str(window_id)

    test_mode_flag=False
    assert test_mode_flag is not None,"debug_param nameError"
    if test_mode_flag==True :
        table_window_debug_info+=", table_id : "+str(table_id)+", test_mode=True)"
    elif test_mode_flag==False :
        table_window_debug_info+=", table_id : "+str(table_id)+")"
    else :
        assert False,"test_mode is None or not a boolean"
    pyray.init_window(cfg.get("table_window_width"),cfg.get("table_window_height"),str(table_window_title+table_window_debug_info))
    pyray.set_target_fps(cfg.get("table_window_target_fps"))
    pyray.set_window_min_size(cfg.get("table_window_width_min"),cfg.get("table_window_height_min"))


    if os_is_windows==False :
        table_window_handle=pyray.get_window_handle()
        pyray.glfw_set_window_aspect_ratio(table_window_handle, cfg.get("table_window_width"),cfg.get("table_window_height"))



    exit_condition=False


    color_theme_dict=cfg.get("color_theme")
    color_theme=ColorTheme(color_theme_dict)
    player_info_font=pyray.load_font(cfg.get("font_path_player_info"))
    chat_font=player_info_font
    option_button_font=pyray.load_font(cfg.get("font_option_button"))
    table_asset_urls=cfg.get("table_asset_urls")
    assert table_asset_urls is not None
    cards_path=table_asset_urls.get("cards_path")
    assert cards_path is not None
    avatars_path=table_asset_urls.get("avatars_path")
    assert avatars_path is not None
    seats_path=table_asset_urls.get("seats_path")
    assert seats_path is not None
    chips_path=table_asset_urls.get("chips_path")
    assert chips_path is not None

    #this doesnt belong here
    cards=[]
    card_ids=[]
    for card_id,card_img_filename in enumerate(card_img_filenames) :
        full_path=cards_path+card_img_filename
        card=CardIMG(full_path)
        cards.append(card)
        card_ids.append(card_id)
        #print(card_id)

    chip_set=ChipSet(chips_path)
    table_asset_urls=cfg.get("table_asset_urls")

    table_view_renderer=TableViewRenderer()
    table_view_renderer.set_player_info_font(player_info_font)
    table_view_renderer.set_option_button_font(option_button_font)
    table_view_renderer.set_chat_font(chat_font)
    table_view_renderer.set_table_asset_urls(table_asset_urls)
    table_view_renderer.set_chip_set(chip_set)
    table_view_renderer.set_color_theme(color_theme)
    #cards dont belong here
    table_view_renderer.set_cards(cards)
    table_view_renderer.set_window_width(cfg.get("table_window_width"))
    table_view_renderer.set_window_height(cfg.get("table_window_height"))


    if table_view_renderer.is_happy() :
        table_view_renderer.clap_your_hands()
    else :
        assert False,"HappyObjectNotHappyException"
    avatar_set_index=table_id%10
    table_view=TableView(table_view_renderer,avatar_set=avatar_set_index,test_mode=test_mode_flag,window_title=table_window_title,debug_info=table_window_debug_info)

    client_is_connected=True
    shutdown_flag=False
    current_window_width=pyray.get_screen_width()
    current_window_height=pyray.get_screen_height()
    print("get_screen_width : ",str(pyray.get_screen_width()))
    print("get_screen_height : ",str(pyray.get_screen_height()))
    while exit_condition==False and shutdown_flag==False:

        #ghetto fix for maintaining window aspect ratio. to me it seems like intel hd drivers on windows platform result in crashes when calling glfw functions.
        #the pyray.is_window_resized() return value also doesnt work as expected on my win11/hd5500 machine. see line 60.
        if pyray.get_screen_height()==current_window_height and pyray.get_screen_width()!=current_window_width :
            new_window_width=pyray.get_screen_width()
            new_window_height=int(new_window_width*0.75)
            pyray.set_window_size(new_window_width,new_window_height)
            current_window_width=new_window_width
            current_window_height=new_window_height
        elif pyray.get_screen_width()==current_window_width and pyray.get_screen_height()!=current_window_height :
            new_window_height=pyray.get_screen_height()
            new_window_width=int(new_window_height/0.75)
            pyray.set_window_size(new_window_width,new_window_height)
            current_window_width=new_window_width
            current_window_height=new_window_height
        elif pyray.get_screen_height()!=current_window_height and pyray.get_screen_width()!=current_window_width :
            new_window_width=pyray.get_screen_width()
            new_window_height=int(new_window_width*0.75)
            pyray.set_window_size(new_window_width,new_window_height)
            current_window_width=new_window_width
            current_window_height=new_window_height
        #ghetto fix end

        if con.poll(0) :
            m=con.recv()
            #DONK_DEBUG(local_domain,local_user,"message_receive_any")
            #if debug_param==True :
            #    print("DEBUG : [table_window] message_receive_any : ",m)
            m_typ=m.get("MESSAGE_TYPE")
            assert m_typ is not None
            if m_typ=="BROADCAST_EVENT" :
                e_typ=m.get("EVENT_TYPE")
                if e_typ=="SHUTDOWN":
                    exit_condition=True
                    shutdown_flag=True
                    print("DEBUG : [table_window] window_id ",window_id," received SHUTDOWN message")
                elif e_typ=="DISCONNECTED" :
                    client_is_connected=False
                    #table_view.clear()
                elif e_typ=="CONNECTED" :
                    client_is_connected=True
                else :
                    e="unknown event type : "+str(e_typ)
                    assert False,e
            elif m_typ=="TABLE_WINDOW_UPDATE":
                m_window_id=m.get("WINDOW_ID")
                assert m_window_id is not None,"missing field 'WINDOW_ID' in message of type 'TABLE_WINDOW_UPDATE'"
                assert window_id==m_window_id,"'WINDOW_ID' in message of type 'TABLE_WINDOW_UPDATE' does not match local table_window.window_id! this is most likely caused by a malformed ipc message or a routing error."
                m_dat=m.get("MESSAGE_DATA")
                assert m_dat is not None,"missing field 'MESSAGE_DATA' in message of type 'TABLE_WINDOW_UPDATE'"
                m_table_id=m_dat.get("TABLE_ID")
                assert m_table_id is not None,"missing field 'TABLE_ID' in message_data of message_type 'TABLE_WINDOW_UPDATE'"
                assert m_table_id==table_id,"'TABLE_ID' in message_data of type 'TABLE_WINDOW_UPDATE' does not match local table_window.table_id! this is most likely caused by a malformed ipc message or a routing error."
                #debug_param=debug_params.get("debug_table_window_receive_message_type_table_window_update")
                #assert debug_param is not None,"debug_param nameError"
                #if debug_param==True :
                #    print("DEBUG : [table_window] received : ",m_typ)
                table_view_data=m_dat.get("TABLE_VIEW_DATA")
                assert table_view_data is not None,"missing field 'TABLE_VIEW_DATA' in message_data of message_type 'TABLE_WINDOW_UPDATE'"
                table_view.slurp(table_view_data)
            elif m_typ=="TABLE_WINDOW_EVENT":
                m_window_id=m.get("WINDOW_ID")
                assert m_window_id is not None,"missing field 'WINDOW_ID' in message of type 'TABLE_WINDOW_EVENT'"
                assert window_id==m_window_id,"'WINDOW_ID' in message of type 'TABLE_WINDOW_EVENT' does not match local table_window.window_id! this is most likely caused by a malformed ipc message or a routing error."
                m_dat=m.get("MESSAGE_DATA")
                assert m_dat is not None,"missing field 'MESSAGE_DATA' in message of type 'TABLE_WINDOW_EVENT'"
                m_table_id=m_dat.get("TABLE_ID")
                assert m_table_id is not None,"missing field 'TABLE_ID' in message_data of message_type 'TABLE_WINDOW_EVENT'"
                assert m_table_id==table_id,"'TABLE_ID' in message_data of type 'TABLE_WINDOW_EVENT' does not match local table_window.table_id! this is most likely caused by a malformed ipc message or a routing error."
                #debug_param=debug_params.get("debug_table_window_receive_message_type_table_window_event")
                #assert debug_param is not None,"debug_param nameError"
                #if debug_param==True :
                #    print("DEBUG : [table_window] received : ",m_typ)
                table_event_type=m_dat.get("TABLE_EVENT_TYPE")
                assert table_event_type is not None,"missing field 'TABLE_EVENT_TYPE' in message_data of message_type 'TABLE_WINDOW_EVENT'"
                table_event_data=m_dat.get("TABLE_EVENT_DATA")
                assert table_event_data is not None,"missing field 'TABLE_EVENT_DATA' in message_data of message_type 'TABLE_WINDOW_EVENT'"
                table_view.handle_table_event(table_event_type,table_event_data)
            else :
                e="unknown message type : "+str(m_typ)
                assert debug_param is not None,"debug_param nameError"

        if shutdown_flag==False :
            #connection_thread.handle_all_the_things()
            key=pyray.get_key_pressed()
            if key:
                print("key : ",key)
                if key==KEY_ESC or pyray.is_key_pressed(pyray.KEY_ESCAPE) :
                    exit_condition=True
                if test_mode_flag==True :
                    if key==KEY_F1: #F5
                        table_view.test_table_reset()
                    elif key==KEY_F2 : #F5
                        table_view.test_button_advance()
                    elif key==KEY_F3 : #F5
                        table_view.test_focus_seat_advance()
                    elif key==KEY_F4 : #F5
                        table_view.test_inline_put_return()
                    elif key==KEY_F5 : #F5
                        table_view.test_match_return_collect_assign()
                    elif key==KEY_F6 : #F5
                        table_view.test_overlay_post()
                    elif key==KEY_F7 : #F5
                        table_view.test_overlay_fold()
                    elif key==KEY_F8 : #F5
                        table_view.test_overlay_check()
                    elif key==KEY_F9 : #F5
                        table_view.test_overlay_call()
                    elif key==KEY_F10 : #F5
                        table_view.test_overlay_raise()


            pyray.begin_drawing()
            pyray.clear_background(pyray.Color(0,0,0,255))
            table_view.update_self()
            window_width,window_height=(pyray.get_screen_width(),pyray.get_screen_height())
            table_view.renderer.update_window_dimensions(window_width,window_height)
            table_view.update_self()
            table_view.draw_self()
            if client_is_connected==False :
                pyray.draw_text("disconnected",20,20,12,pyray.Color(255,255,255,255))
            elif client_is_connected==True  :
                pyray.draw_text("connected",20,20,12,pyray.Color(255,255,255,255))
            else :
                assert False,"oops"



            time.sleep(0.01)
            pyray.end_drawing()
        if pyray.window_should_close() :
            exit_condition=True
            reason="pyray.window_should_close()==True"
            print("INFO : [table_window] window_id ",window_id," exiting , reason : ",reason)
            m=WindowMessenger.create_ipc_table_window_should_close_message(window_id,table_id)
            print("INFO : [table_window] window_id ",window_id," sending window_should_close_message to main process")
            assert m is not None
            #print(m)
            con.send(m)
            time.sleep(1)
        if shutdown_flag==True :
            exit_condition=True
            reason="shutdown_flag==True"
            print("INFO : [table_window] window_id ",window_id," exiting, reason : ",reason)

if __name__=="__main__":
    print("Error : [table_window] to run the client application use 'main_client.py' as entry point")
