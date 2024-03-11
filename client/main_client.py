import sys; sys.dont_write_bytecode = True
import os
sys.path.append(os.getcwd() + '/..')
from common.common import *
assert COMMON_IMPORTS,"ERROR : [__main__] missing import"
import json
from threading import Thread,Event
import time
from default_config_json import default_config_json_str
from pprint import pprint
import random
from common.debug_department import DONK_WARNING,DONK_DEBUG,DONK_ERROR
local_domain="main_client"
local_user=None
#from table_pool_view import TablePoolView
#from table_pool_view_renderer import TablePoolViewRenderer
#import sockets
from connection_thread import ConnectionThread
#from ascii_matrix import *
from multiprocessing import Process,Pipe
from lobby_window import lobby_window_launch
from table_window import table_window_launch
from ipc_messaging import WindowMessenger
#from common.tools_for_fools import *
client_config={}

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





def str_error(where,error_msg):
    s="ERROR : "
    s+="["+str(where)+"] "+error_msg
    #        s+="unknown error_type <"+error_type+">"
    return s


def create_table_window(table_window_id,table_view_request,cfg):
    local_user="create_table_window"
    DONK_DEBUG(local_domain,local_user,"show_table_view_request",table_view_request)
    assert cfg is not None,"cfg is None"
    assert table_view_request is not None,"table_view_request is None"
    table_id=table_view_request.get("table_id")
    assert table_id is not None,"invalid request, missing field 'table_id'"
    table_name=table_view_request.get("table_name")
    assert table_name is not None,"invalid request, missing field 'table_name'"

    table_window_parent_con,table_window_child_con=Pipe()
    table_window_process=Process(target=table_window_launch,args=(table_window_id,table_id,table_name,cfg,table_window_child_con))
    table_window_process.start()

    table_window={
        "is_connected":True,
        "message_inbox"     :   [],
        "message_outbox"    :   [],
        "process_handle"    :   table_window_process,
        "parent_con_handle" :   table_window_parent_con,
        "table_window_id"   :   table_window_id,
        "table_id"          :   table_id
    }
    return table_window


def is_table_id_in_requests(table_id,requests):
    for r in requests :
        if r.get("table_id")==table_id :
            return True
    return False


if __name__=="__main__" :
    local_user="__main__"

    print("loading default config")
    cfg=None
    try :
        cfg=json.loads(default_config_json_str)
    except :
        print("FatalError : could not load default_config_json")
    print(cfg.get("version"))
    print("initializing lobby_window")
    assert cfg.get("lobby_window_title") is not None,"missing field 'lobby_window_title' in cfg"
    lobby_window_parent_con,lobby_window_child_con=Pipe()
    lobby_window_process=Process(target=lobby_window_launch,args=(cfg,lobby_window_child_con))
    lobby_window_process.start()

    lobby_window_state={
        "is_connected":False,
        "message_inbox":[],
        "message_outbox":[],
    }

    table_windows={}
    pending_table_view_requests=[]
    active_table_view_requests=[]
    connection_thread=ConnectionThread()
    connection_thread.start()
    exit_condition=False
    table_window_id_counter=0
    window_messenger=WindowMessenger()

    while exit_condition==False :
        try :
            #connection_thread.handle_all_the_things()
            client_connected=connection_thread.is_connected()
            open_table_window_ids=list(table_windows.keys())
            for open_table_window_id in open_table_window_ids :
                table_window=table_windows.get(open_table_window_id)
                if is_table_id_in_requests(table_window.get("table_id"),active_table_view_requests)==True :
                    parent_con=table_window.get("parent_con_handle")
                    if parent_con.poll(0) :
                        m=parent_con.recv()
                        table_window["message_inbox"].append(m)
                    table_window_connection_state=table_window.get("is_connected")
                    assert table_window_connection_state is not None,"table_window_connection_state is None"
                    if table_window_connection_state==True and client_connected==False :
                        m=window_messenger.create_ipc_disconnected_message()
                        parent_con.send(m)
                        table_window["is_connected"]=False
                    elif table_window_connection_state==False and client_connected==True:
                        m=window_messenger.create_ipc_connected_message()
                        parent_con.send(m)
                        table_window["is_connected"]=True
                else :
                    DONK_WARNING(local_domain,local_user,"log_any","table_window which is not listed in active table_view_requests fell through for polling")


            if lobby_window_parent_con.poll(0) :
                #print("DEBUG : [lobby_window_parent_con.poll] True")
                m=lobby_window_parent_con.recv()
                lobby_window_state["message_inbox"].append(m)

            if lobby_window_state.get("is_connected")==False and client_connected==True :
                m=window_messenger.create_ipc_connected_message()
                lobby_window_state["message_outbox"].append(m)
                lobby_window_state["is_connected"]=True
            elif lobby_window_state.get("is_connected")==True and client_connected==False :
                m=window_messenger.create_ipc_disconnected_message()
                lobby_window_state["message_outbox"].append(m)
                lobby_window_parent_con.send(m)
                lobby_window_state["is_connected"]=False

            if len(lobby_window_state["message_outbox"])>0 :
                m=lobby_window_state["message_outbox"].pop(0)
                lobby_window_parent_con.send(m)

            if len(lobby_window_state["message_inbox"])>0 :
                m=lobby_window_state["message_inbox"].pop(0)
                #print("DEBUG : [main_client] lobby_window_inbox message : ",m)
                m_typ=m.get("MESSAGE_TYPE")
                e="invalid ipc message in lobby_window inbox, field 'MESSAGE_TYPE' is not present"
                assert m_typ is not None,e
                m_dat=m.get("MESSAGE_DATA")
                e="invalid ipc message in lobby_window inbox, field 'MESSAGE_DATA' is not present"
                assert m_dat is not None,e
                if m_typ=="WINDOW_EVENT":
                    window_id=m_dat.get("WINDOW_ID")
                    assert window_id is not None,"missing key 'WINDOW_ID' in message_data in message with message_type 'WINDOW_EVENT'"
                    window_event_type=m_dat.get("WINDOW_EVENT_TYPE")
                    assert window_event_type is not None,"missing key 'WINDOW_EVENT_TYPE' in message_data in message with message_type 'WINDOW_EVENT'"
                    if window_event_type=="LOBBY_WINDOW_SHOULD_CLOSE":
                        DONK_DEBUG(local_domain,local_user,"handle_message_inbox"," received ",str(m))
                        exit_condition=True
                        DONK_DEBUG(local_domain,local_user,"handle_message_inbox","setting exit_condition=True")
                        connection_thread.disconnect_from_server()
                        #m=window_messenger.create_ipc_shutdown_message()
                        m=window_messenger.create_ipc_shutdown_message()
                        table_window_ids=list(table_windows.keys())
                        for table_window_id in table_window_ids :
                            table_window_dict=table_windows.get(table_window_id)
                            table_window_con=table_window_dict.get("parent_con_handle")
                            table_window_process=table_window_dict.get("process_handle")
                            DONK_DEBUG(local_domain,local_user,"handle_message_inbox","sending SHUTDOWN to window_id ",table_window_id," m = ",m)
                            table_window_con.send(m)
                            DONK_DEBUG(local_domain,local_user,"handle_message_inbox","waiting for window_id ",table_window_id," process to 'join'")
                            table_window_process.join()
                            time.sleep(0.01)

                    else :
                        assert False,"UNREACHABLE"
                elif m_typ=="USER_EVENT":
                    user_event_type=m_dat.get("USER_EVENT_TYPE")
                    e="user_event_type in user_event message from lobby_window_inbox is None"
                    assert user_event_type is not None,e
                    if user_event_type=="REQUEST_TABLE_VIEW" :
                        user_event_data=m_dat.get("REQUEST_DATA")
                        e="user event '"+user_event_type+"'"+" missing field 'REQUEST_DATA'"
                        assert user_event_data is not None,e
                        pending_table_view_requests.append(user_event_data)
                        DONK_DEBUG(local_domain,local_user,"pending_table_view_requests_append","appending table_view_request to pending_list: ",user_event_data)#,user_event_data)
                    else :
                        e="NOT_IMPLEMENTED : user_event_type['"+str(user_event_type)+"']"
                        assert False,e
                else :
                    e="NOT_IMPLEMENTED lobby_window.inbox.message.message_type['"+str(m_typ)+"']"
                    assert False,e

            #handle table_view_pending requests
            if len(pending_table_view_requests)>0 :
                pending_table_view_request=pending_table_view_requests.pop(0)
                DONK_DEBUG(local_domain,local_user,"handle_pending_table_view_request","handling pending_table_view_request : ",pending_table_view_request)
                if pending_table_view_request in active_table_view_requests :
                    DONK_DEBUG(local_domain,local_user,"pending_table_view_request_duplicate"," bringing window to front and focus ... not implemented")
                else :
                    table_window_id_counter+=1
                    table_window_id=table_window_id_counter
                    table_window_dict=create_table_window(table_window_id,pending_table_view_request,cfg)
                    table_id=pending_table_view_request.get("table_id")
                    table_name=pending_table_view_request.get("table_name")

                    id_to=connection_thread.server_id
                    id_from=connection_thread.client_id
                    payload={
                        "TABLE_ID":table_id,
                        "TABLE_NAME":table_name
                        }
                    m=PokerMessageProtocol.create("SUBSCRIBE_TABLE_VIEW",id_from,id_to,payload)
                    connection_thread.message_outbox_push_tail(m)
                    #assert False,"TODO : send subsciption"
                    table_windows.setdefault(table_window_id)
                    table_windows[table_window_id]=table_window_dict
                    active_table_view_requests.append(pending_table_view_request)
                    connection_thread.register_table_id(table_id)

            if connection_thread.has_table_pool_view_data():
                table_pool_view_data=connection_thread.get_table_pool_view_data()
                m=window_messenger.create_ipc_table_pool_view_update_message(table_pool_view_data)
                lobby_window_state["message_outbox"].append(m)
                lobby_window_parent_con.send(m)
                connection_thread.forget_table_pool_view_data()


            table_window_ids=list(table_windows.keys())
            for table_window_id in table_window_ids :
                assert table_window_id>0,"invalid table_window_id"
                table_window_dict=table_windows.get(table_window_id)
                assert table_window_dict is not None,"table_window lookup error"
                table_id=table_window_dict.get("table_id")

                assert table_id is not None,"missing 'table_id' in table_window_dict"
                if connection_thread.has_table_event_for_table_id(table_id):
                    table_event_type,table_event_data=connection_thread.pop_table_event_for_table_id(table_id)
                    m=window_messenger.create_ipc_table_window_event_message(table_window_id,table_id,table_event_type,table_event_data)
                #print("DEBUG : [main_client] ipc_table_window_event_message : ",m)
                    table_window_con=table_window_dict.get("parent_con_handle")
                    table_window_con.send(m)
                    #time.sleep(0.005)
                elif connection_thread.has_table_view_data_for_table_id(table_id):
                    table_view_data=connection_thread.get_table_view_data_for_table_id(table_id)
                    m=window_messenger.create_ipc_table_window_update_message(table_window_id,table_id,table_view_data)
                    table_window_con=table_window_dict.get("parent_con_handle")
                    #print("INFO  : [main_client] sending 'ipc_table_window_update_message' window_id ",table_window_id," m = ",m)
                    table_window_con.send(m)
                    #time.sleep(0.005)



            table_window_ids=list(table_windows.keys())
            for table_window_id in table_window_ids:
                assert table_window_id>0,"invalid table_window_id"
                table_window_dict=table_windows.get(table_window_id)
                assert table_window_dict is not None,"table_window lookup error"
                table_id=table_window_dict.get("table_id")
                assert table_id is not None,"missing 'table_id' in table_window_dict"
                if len(table_window_dict["message_inbox"])>0 :
                    m=table_window_dict["message_inbox"].pop(0)
                #while len(table_window_dict["message_inbox"])>0 :
                #    m=table_window_dict["message_inbox"].pop(0)
                    assert m is not None
                    m_typ=m.get("MESSAGE_TYPE")
                    assert m_typ=="WINDOW_EVENT","ipc integrity error"
                    m_dat=m.get("MESSAGE_DATA")
                    assert m_dat is not None
                    if m_typ=="WINDOW_EVENT":
                        window_event_type=m_dat.get("WINDOW_EVENT_TYPE")
                        assert window_event_type is not None
                        assert m_dat.get("WINDOW_ID")==table_window_id
                        assert m_dat.get("WINDOW_ID")==table_window_dict.get("table_window_id")
                        assert window_event_type=="TABLE_WINDOW_SHOULD_CLOSE"
                        if window_event_type=="TABLE_WINDOW_SHOULD_CLOSE":
                            DONK_DEBUG(local_domain,local_user,"handle_table_window_message_inbox","handling TABLE_WINDOW_SHOULD_CLOSE")
                            request_to_remove=None
                            for active_request in active_table_view_requests :
                                table_id_in_request=active_request.get("table_id")
                                assert table_id_in_request is not None
                                if table_id_in_request==table_id :
                                    DONK_DEBUG(local_domain,local_user,"remove_table_request_found")
                                    request_to_remove=active_request
                                    break
                            if request_to_remove is None :
                                DONK_ERROR(local_domain,local_user,"error_remove_table_request_not_found")
                                assert False,"table_view_request not found"
                            #TODO : move this into connection_thread
                            payload={
                                "TABLE_ID":request_to_remove.get("table_id"),
                                "TABLE_NAME":request_to_remove.get("table_name")
                                }
                            m=PokerMessageProtocol.create("UNSUBSCRIBE_TABLE_VIEW",connection_thread.client_id,connection_thread.server_id,payload)
                            #print("DEBUG : [main_client] unsub m:",m.serialize().decode())
                            connection_thread.message_outbox_push_tail(m)
                            connection_thread.handle_message_outbox()
                            connection_thread.unregister_table_id(request_to_remove.get("table_id"))
                            assert request_to_remove in active_table_view_requests
                            active_table_view_requests.remove(request_to_remove)

            for key in list(table_windows.keys()):
                table_window_dict=table_windows.get(key)
                e="integrity error, key=="+str(key)+" but table_window_dict.get('table_window_id')=="+str(table_window_dict.get("table_window_id"))
                assert key==table_window_dict.get("table_window_id"),e
                table_id=table_window_dict.get("table_id")
                assert table_id is not None
                if is_table_id_in_requests(table_id,active_table_view_requests)==False :
                    #DONK_DEBUG(local_domain,local_user,"table_window_delete","table_windows : ",str(table_windows))
                    DONK_DEBUG(local_domain,local_user,"table_window_delete","deleting table_window_dict : ",str(table_window_dict))
                    con=table_window_dict.get("parent_con_handle")
                    if con is not None :
                        try :
                            con.close()
                        except :
                            pass
                    table_windows[key]=None
                    table_windows.pop(key)
                    del table_window_dict
                    break


            time.sleep(0.01) #main_client event loop cpu usage chiller
        except KeyboardInterrupt:
            DONK_DEBUG(local_domain,local_user,"broadcast_send_shutdown")
            #local_shutdown_of_all_child_processes
            connection_thread.disconnect_from_server()
            m=window_messenger.create_ipc_shutdown_message()#m=window_messenger.create_ipc_shutdown_message()
            lobby_window_parent_con.send(m)
            lobby_window_process.join()
            table_window_ids=list(table_windows.keys())
            for table_window_id in table_window_ids :
                table_window_dict=table_windows.get(table_window_id)
                table_window_con=table_window_dict.get("parent_con_handle")
                table_window_process=table_window_dict.get("process_handle")
                DONK_DEBUG(local_domain,local_user,"broadcast_send_shutdown","sending SHUTDOWN to window_id ",table_window_id)
                table_window_con.send(m)
                DONK_DEBUG(local_domain,local_user,"broadcast_send_shutdown","waiting for window_id ",table_window_id," process to 'join'")
                table_window_process.join()
                time.sleep(0.5)


            time.sleep(1)
            exit_condition=True
