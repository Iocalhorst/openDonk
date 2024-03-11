import pyray
import time
from ascii_matrix import AsciiMatrix
#from debug_params import debug_params
from table_pool_view import TablePoolView
from table_pool_view_renderer import TablePoolViewRenderer
#from debug_params import debug_params
from common.debug_department import DONK_WARNING,DONK_DEBUG,DONK_ERROR
from ipc_messaging import WindowMessenger


def create_user_event_message(user_event):
    m={
        "MESSAGE_TYPE" : "USER_EVENT",
        "MESSAGE_DATA" : user_event
    }
    return m

def lobby_window_launch(cfg,child_con):
    local_domain="lobby_window"
    local_user="lobby_window_launch"
    con=child_con
    window_id=0
    pyray.set_trace_log_level(pyray.LOG_WARNING)
    pyray.set_config_flags(pyray.FLAG_WINDOW_ALWAYS_RUN)
    assert cfg.get("lobby_window_title") is not None,"missing field 'lobby_window_title' in cfg"
    pyray.init_window(cfg.get("lobby_window_width"),cfg.get("lobby_window_height"),cfg.get("lobby_window_title"))
    pyray.set_target_fps(cfg.get("lobby_window_target_fps"))
    exit_condition=False
    background_animation=AsciiMatrix(width=45,height=45,num_streamers=44)
    #connection_thread=ConnectionThread()
    #connection_thread.start()


    table_pool_view_renderer=TablePoolViewRenderer()
    table_pool_font=pyray.load_font(cfg.get("font_path_table_pool_view"))
    table_pool_view_renderer.set_table_pool_font(table_pool_font)

    if table_pool_view_renderer.is_happy() :
        table_pool_view_renderer.clap_your_hands()
    else :
        assert False,"HappyObjectNotHappyException"

    table_pool_view=TablePoolView(table_pool_view_renderer)

    client_is_connected=False
    shutdown_flag=False
    while exit_condition==False and shutdown_flag==False:
        background_animation.update_self()

        if con.poll(0) :
            m=con.recv()
            m_typ=m.get("MESSAGE_TYPE")
            assert m_typ is not None,"e_msg_invalid"
            if m_typ=="BROADCAST_EVENT" :
                e_typ=m.get("EVENT_TYPE")
                if e_typ=="DISCONNECTED" :
                    client_is_connected=False
                    table_pool_view.clear()
                elif e_typ=="CONNECTED" :
                    client_is_connected=True
                elif e_typ=="SHUTDOWN":
                    exit_condition=True
                    shutdown_flag=True
                    DONK_DEBUG(local_domain,local_user,"message_receive","received SHUTDOWN message")
                else :
                    e="unknown event type : "+str(e_typ)
                    assert False,e
            elif m_typ=="TABLE_POOL_VIEW_DATA_UPDATE":
                table_pool_view_data=m.get("TABLE_POOL_VIEW_DATA")
                DONK_DEBUG(local_domain,local_user,"receive_table_pool_data")
                table_pool_view.slurp(table_pool_view_data)
            else :
                e="unknown message type : "+str(m_typ)
                assert False,e

        #connection_thread.handle_all_the_things()
        if exit_condition==False :
            pyray.begin_drawing()
            pyray.clear_background(pyray.Color(0,0,0,255))
            background_animation.draw_self()
            table_pool_view.update_self()
            if client_is_connected==False :
                pyray.draw_text("disconnected",50,40,14,pyray.Color(200,212,182,255))#pyray.Color(255,255,255,255))
            elif client_is_connected==True :
                pyray.draw_text("connected",50,40,14,pyray.Color(200,212,182,255))#pyray.Color(255,255,255,255))
                table_pool_view.draw_self()
            if table_pool_view.has_user_events()==True:
                user_event=table_pool_view.pop_user_event()
                #debug_param=debug_params.get("debug_lobby_window_user_event_pop_from_table_pool_view")
                #assert debug_param is not None,"debug_param nameError"
                #if debug_param==True :
                #    print("DEBUG : [lobby_window_launch] user event pop from table_pool_view : ",user_event)
                #print("DEBUG : [lobby_window_launch] forwarding user event to con[main_client] ",user_event)
                m=create_user_event_message(user_event)
                #print("DEBUG : [lobby_window_launch] create_user_event_message m==",m)
                con.send(m)
                #print("DEBUG : [lobby_window_launch] con.send(m)")
            time.sleep(0.01)
            pyray.end_drawing()
            if pyray.window_should_close() :
                #print("INFO : [lobby_window] window_id ",window_id," exiting, reason : pyray.window_should_close")
                m=WindowMessenger.create_ipc_lobby_window_should_close_message(window_id)
                #print("INFO : [lobby_window] window_id ",window_id," sending lobby_window_should_close exiting to main_client")
                con.send(m)
                exit_condition=True
                time.sleep(1)

if __name__=="__main__" :
    print("Error : [lobby_window] to run the client application use 'main_client.py' as entry point")
    exit(69)
