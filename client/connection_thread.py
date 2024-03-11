import sys; sys.dont_write_bytecode = True
import os
sys.path.append(os.getcwd() + '/..')
from common.common import *
assert COMMON_IMPORTS,"ERROR : [__main__] missing import"
import json
from threading import Thread,Event,Lock
import time
from pprint import pprint
import random
from common.debug_department import DONK_ERROR,DONK_DEBUG,DONK_WARNING
import socket
local_domain="connection_thread"
local_user=None
mutex=Lock()
class ConnectionThread(Thread):
    def __init__(self, args=None, kwargs=None):
        Thread.__init__(self,group=None,daemon=True)
        #self.interval = interval
        #self.function = function
        #self.args = args if args is not None else []
        #self.kwargs = kwargs if kwargs is not None else {}
        self.daemon=True
        self.name="client_thread"
        self.finished=Event()
        self.con=None
        self.message_inbox=[]
        self.message_outbox=[]
        self.server_id=0
        self.client_id=0
        self.failed_send_attempts=0
        self.time_of_last_attempt_to_connect=time.time()-5.0
        self.max_table_events_count=20

        self.table_pool_view_data=None #"lobby"-representation. theres only one lobby, so its kind of a "singleton"

        #these need to be forwarded/dispatched to the actual "table_view"-window handlers.
        #TODO : implement ipc and subprocess managment.
        #i kinda like the idea of table_view_windows polling their data,
        #to leave implemention of "no connection" and "table_is_closed" exceptions to the window processes.
        #both of these ipc messages dont depend on the server.
        #if a table_view process polls view/event data with its id :
        #       if not connected to server                          : send ipc message "disconnected, sorry"
        #       elif connected and table_pool_view_data is None     : send ipc message "disconnected, sorry"
        #       elif connected and table_pool_view_data is not None :
        #                                        if id in pool_view_data        : fine, almost. TODO : subscriptions need to be synchronized.
        #                                        elif id not in pool_view_data  : send ipc message "table_is_closed"
        #                                        else                           : assert False,"UNREACHABLE"
        #       else : assert False,"UNREACHABLE"

        self.table_views={}
        self.table_events={}
        #self.seat_events_data=[]
        #self.pot_events_data=[]
        #self.dealer_events_data=[]


        #assert debug_params.get("debug_connection_thread_init") is not None,"debug namespace fail"
        #DONK_DEBUG(local_domain,"__init__","log_any")
#if debug_params.get("debug_connection_thread_init")==True :
#            print("DEBUG : [ConnectionThread.__init__()] ",self.name)

    #public method
    def register_table_id(self,table_id):
        assert self.table_views.get(table_id) is None,"duplicate table_id"
        assert self.table_events.get(table_id) is None,"duplicate table_id"
        self.table_views.setdefault(table_id)
        self.table_events.setdefault(table_id)
        self.table_events[table_id]=[]

    #public method
    def unregister_table_id(self,table_id):
        local_user="unregister_table_id"
        DONK_DEBUG(local_domain,local_user,"log_any",table_id)
        assert table_id is not None
        #assert self.table_views.get(table_id) is not None
        #assert self.table_events.get(table_id) is not None
        table_view_entry=self.table_views.pop(table_id)
        table_event_entry=self.table_events.pop(table_id)
        del table_view_entry
        del table_event_entry

    #private method
    def update_table_views(self,table_id,table_view_data):
        local_user="update_table_views"
        assert table_id is not None,"table_id is None"
        meta=table_view_data.get("table_view_meta")
        assert meta is not None,"missing 'table_view_meta' in table_view_data"
        assert table_id==meta.get("table_id"),"integrity error, table_id != meta['table_id']"
        #DONK_DEBUG(local_domain,local_user,"received_table_view_data")
        #assert debug_param is not None,"debug_param nameError"
        DONK_DEBUG(local_domain,local_user,"received_table_view_data","table_id",table_id)


        if table_id not in list(self.table_views.keys()) :
            DONK_WARNING(local_domain,local_user,"warning_dropping_table_view_data"," dropping table_view data for table_id : ",table_id," - reason : table_id not in connection_thread.table_views")
        else :
           #print("DEBUG : [connection_thread.update_table_views] updated table_view_data for table_id : ",table_id)
            self.table_views[table_id]=table_view_data

    #private method
    def update_table_events(self,table_id,table_event_type,table_event_data):
        local_user="update_table_events"
        assert table_id is not None,"table_id is None"
        DONK_DEBUG(local_domain,local_user,"received_table_event"," received table_event_data for table_id : ",table_id)
        if table_id not in list(self.table_events.keys()) :
            DONK_WARNING(local_domain,local_user,"warning_dropping_table_event_data"," dropping table_view data for table_id : ",table_id," - reason : table_id not in connection_thread.table_views")
        else :
            self.table_events[table_id].append((table_event_type,table_event_data))
            if len(self.table_events[table_id])>=self.max_table_events_count :
                DONK_WARNING(local_domain,local_user,"warning_max_table_events_count"," table_id : ",table_id," exceeding max_table_events_count - dropping oldest entry")
                table_event_type,table_event_data=self.table_events[table_id].pop(0)
                del table_event_type
                del table_event_data

    #public method
    def has_table_view_data_for_table_id(self,table_id):
        e="WARNING : [connection_thread.has_table_view_data_for_table_id] requested table_id "+str(table_id)+" is not listed as key in connection_thread.table_views"
        if table_id not in list(self.table_views.keys()) :
            print(e)
            return False
        else :
            table_view_data=self.table_views.get(table_id)
            if table_view_data is None :
                #print("ERROR : []")
                return False
            else :
                return True

    #public method
    def get_table_view_data_for_table_id(self,table_id):
        e="ERROR : [connection_thread.get_table_view_data_for_table_id] table_id "+str(table_id)+"for requested table_view_data is not listed as key in connection_thread.table_views"
        assert table_id in list(self.table_views.keys()),e
        table_view_data=self.table_views[table_id].copy()
        self.table_views[table_id]=None
        return table_view_data

    #public method
    def has_table_event_for_table_id(self,table_id):
        e="WARNING : [connection_thread.has_table_event_for_table_id] requested table_id "+str(table_id)+" is not listed as key in connection_thread.table_events"
        if table_id not in list(self.table_events.keys()):
            print(e)
            return False
        else :
            if len(self.table_events[table_id])>0 :
                return True
            else :
                return False
    #public method
    def pop_table_event_for_table_id(self,table_id):
        e="table_id "+str(table_id)+"for requested table_event_data is not listed as key in connection_thread.table_events"
        assert table_id in list(self.table_events.keys()),e
        table_event_type,table_event_data=self.table_events[table_id].pop(0)#data=self.pot_events_data.pop(0)
        return table_event_type,table_event_data
    #public method
    def has_table_pool_view_data(self):
        if self.table_pool_view_data is not None :
            return True
        else :
            return False
    #public method
    def get_table_pool_view_data(self):
        data=self.table_pool_view_data.copy()
        return data
    #public method
    def forget_table_pool_view_data(self):
        self.table_pool_view_data=None

    #public method???
    def cancel(self):
        #self.con.close()
        self.finished.set()

    #private method
    def message_inbox_push_tail(self,m):
        self.message_inbox.append(m)

    #private method
    def message_inbox_push_head(self,m):
        self.message_inbox.insert(0,m)

    #private method
    def handle_connection_error(self):
        local_user="handle_connection_error"
        self.client_id=0
        self.server_id=0
        self.message_inbox.clear()
        self.message_outbox.clear()
        #self.table_pool_view_data=None
        #self.table_views_data.clear()
        #self.dealer_events_data.clear()
        #self.pot_events_data.clear()
        #self.seat_events_data.clear()
        if self.con :
            self.con.close()
            self.con=None

        DONK_DEBUG(local_domain,local_user,"graceful_disconnect")


    #public method
    def is_connected(self):
        if self.con is None :
            return False
        else :
            try:
                self.con.setblocking(0)
                buf = self.con.recv(1, socket.MSG_PEEK )
                if buf == b'':
                    self.handle_connection_error()
                    return False
            except BlockingIOError as io_e:
                #print(str(io_e))
            #print(io_e)
                pass
                #time.sleep(0.005)
        return True

    #private method
    def handle_failed_attempt_to_connect(self):
        self.time_of_last_attempt_to_connect=time.time()

    #private method
    def connect_to_server(self):
        local_user="connect_to_server"
        t_retry=self.time_of_last_attempt_to_connect+5.0
        if time.time()<t_retry :
            #time.sleep(0.1)
            return
        self.time_of_last_attempt_to_connect=time.time()

        #LOG_DEBUG(local_domain,local_userm,"reconnect","retrying to connect to server")
        ip=server_ip #common.py
        port=server_port #common.py
        try:
            DONK_DEBUG(local_domain,local_user,"connect_retry"," trying to connect to server")
            self.con=socket.create_connection((ip,port))
            DONK_DEBUG(local_domain,local_user,"connect_success"," connected to server ",str(ip),":",str(port))
        except :
            self.handle_failed_attempt_to_connect()
            DONK_DEBUG(local_domain,local_user,"connect_fail","failed to connect - retrying in 5s")


    #public method
    def disconnect_from_server(self):
        local_user="disconnect_from_server"
        if self.is_connected() :
            DONK_DEBUG(local_domain,local_user,"disconnect_on_purpose")
            m=PokerMessageProtocol.create("CLIENT_GOODBYE",self.client_id,self.server_id)
            self.con.send(m.serialize())
            #print("DEBUG : [connection_thread.disconnect_from_server] sending CLIENT_GOODBYE to server")
            self.con.close()
            #else :
            #    print("DEBUG : [connection_thread.disconnect_from_server] ignoring! reason : not connected.")


    #private method
    def read_from_connection(self):#"debug_connection_thread_table_events_data_append":True,
        #print("reading from con")
        #assert self.con is not None,"con is None"
        mutex.acquire()
        try :
            self.con.setblocking(False)
            data, address = self.con.recvfrom(4096)
            if data:
                try :
                    message=PokerMessage.deserialize(data.decode())
                    self.message_inbox_push_tail(message)
                except Exception as ex_in:
                    print("ERROR : [connection_thread.read_from_connection] Exception : ",str(ex_in))
                    pass
                #print(message.serialize().decode())

            #time.sleep(0.0051)
        except BlockingIOError as io_e:
            pass
        except Exception as ex :
            print("ERROR : [connection_thread.read_from_connection] Exception : ",str(ex))
        finally :
            time.sleep(0.005)
            mutex.release()
    #private method
    def handle_message_outbox(self):

        m=self.message_outbox_pop_head()
        try :
            self.con.send(m.serialize())
            self.failed_send_attempts=0
            #print("succeeded to send ")
        except :#"debug_connection_thread_table_events_data_append":True,
            self.message_outbox_push_head(m)
            self.failed_send_attempts+=1
            #print("failed to send")
                             #print("DEBUG : [ConnectionThread.handle_message_outbox] sending message")
            #print("DEBUG : [ConnectionThread.handle_message_outbox] ",m.serialize().decode())

    #private method
    def message_outbox_push_head(self,m):
        #print("DEBUG : [ConnectionThread] message_outbox_push_back")
        self.message_outbox.insert(0,m)

    #private method
    def message_outbox_push_tail(self,m):
        #print("DEBUG : [ConnectionThread] message_outbox_push_tail")
        self.message_outbox.append(m)

    #private method
    def message_outbox_pop_head(self):
        #print("DEBUG : [ConnectionThread] message_outbox_pop_head")
        return self.message_outbox.pop(0)
        assert m,e
        return m

    #private method#"debug_connection_thread_table_events_data_append":True,
    def message_inbox_pop_head(self):
        #print("DEBUG : [ConnectionThread] message_inbox_pop_head")
        m=self.message_inbox.pop(0)
        e="ERROR [ConnectionThread.message_inbox_pop] m is "+str(m)
        assert m,e
        return m

    #private method
    def message_inbox_is_not_empty(self):
        if len(self.message_inbox)>0:
            return True
        else :
            return False

    #private method
    def message_outbox_is_not_empty(self):
        if len(self.message_outbox)>0:
            return True
        else :
            return False

    #private method
    def handle_message_inbox(self):
        local_user="handle_message_inbox"
        m=self.message_inbox_pop_head()
        m_typ=m.head.get("MESSAGE_TYPE")
        m_src=m.head.get("SRC_ID")
        m_dst=m.head.get("DST_ID")
        m_req=m.body.get("REQUIRE")

        if self.server_id==0 and self.client_id==0 and m_typ!="SERVER_HELLO":
            e="ERROR : [ConnectionThread.handle_message_inbox] ERROR_MSG_OUT_OF_BAND['"+m_typ+"'], expected 'SERVER_HELLO'"
            assert False,e

        if m_typ=="SERVER_HELLO":
            e="ERROR : [ConnectionThread.handle_message_inbox] ERROR_MSG_OUT_OF_BAND['"+m_typ+"']"
            assert self.server_id==0,e
            assert self.client_id==0,e
            self.client_id=m.body.get("CLIENT_ID")
            self.server_id=m.body.get("SERVER_ID")
            #debug_param=debug_params.get("debug_connection_thread_handle_message_inbox_server_hello")
            #assert debug_param is not None,"debug nameError"
            #if debug_param==True:#"debug_connection_thread_table_events_data_append":True,
            #    print("DEBUG : [connection_thread.handle_message_inbox] received '",m_typ,"'")
            #    print("DEBUG : [connection_thread.handle_message_inbox] assigning client_id[",self.client_id,"]")
            #    print("DEBUG : [connection_thread.handle_message_inbox] assigning server_id[",self.server_id,"]")
            assert m_req=="CLIENT_HELLO","meh, expected field REQUIRE:CLIENT_HELLO"
            response=PokerMessageProtocol.create(m_req,self.client_id,self.server_id)
            self.message_outbox_push_tail(response)

        elif m_typ=="PING":
            #TODO("cleanup")
            e="ERROR : [ConnectionThread.handle_message_inbox] ERROR_MSG_INVALID, "
            e+="'"+m_typ+"', "
            e+="'"+"REQUIRE"+"' : "
            e+="'"+m_req+"', "
            e+="expected : "
            e+="'REQUIRE' : 'PONG'"
            assert m_req=="PONG",e
            #debug_param=debug_params.get("debug_connection_thread_handle_message_inbox_ping")
            #assert debug_param is not None,"debug nameError"
            #if debug_param==True:
            #    print("DEBUG : [connection_thread.handle_message_inbox] received '",m_typ,"'")
            response_data={"TIME_STAMP_PING":m.body.get("TIME_STAMP_PING")}
            response=PokerMessageProtocol.create(m_req,self.client_id,self.server_id,response_data)
            #debug_param=debug_params.get("debug_connection_thread_handle_message_inbox_create_response_pong")
            #assert debug_param is not None,"debug nameError"
            #if debug_param==True:
            #    print("DEBUG : [connection_thread.handle_message_inbox] created response message : ",response.head.get("MESSAGE_TYPE"))
            self.message_outbox_push_tail(response)

        elif m_typ=="PUSH_TABLE_POOL_VIEW":
            #print("DEBUG : [ConnectionThread] received ",m.head)nregister_table_i
            #pprint(m.body)
            #assert False
            table_pool_view_data=m.body.get("TABLE_POOL_VIEW")
            assert table_pool_view_data is not None,"invalid/missing message from server, field TABLE_POOL_VIEW_DATA is rubbish, local variable 'table_pool_view_data' is None"
            DONK_DEBUG(local_domain,local_user,"received_push_table_pool_view")
            self.table_pool_view_data=table_pool_view_data
        elif m_typ=="PUSH_TABLE_VIEW":
            table_view_data=m.body.get("TABLE_VIEW_DATA")
            assert table_view_data is not None,"missing field 'TABLE_VIEW_DATA'"
            table_id=m.body.get("TABLE_ID")
            assert table_id is not None,"missing field 'TABLE_ID'"
            self.update_table_views(table_id,table_view_data)
        elif m_typ=="PUSH_TABLE_EVENT":
            table_event_type=m.body.get("TABLE_EVENT_TYPE")
            assert table_event_type is not None,"missing field 'TABLE_EVENT_TYPE'"
            table_event_data=m.body.get("TABLE_EVENT_DATA")
            assert table_event_data is not None,"missing field 'TABLE_EVENT_DATA'"
            table_id=m.body.get("TABLE_ID")
            assert table_id is not None,"missing field TABLE_ID"
            self.update_table_events(table_id,table_event_type,table_event_data)
        else :
            e="ERROR : [ConnectionThread.handle_message_inbox] NOT_IMPLEMENTED, '"+m_typ+"'"
            assert False,e

    #public method - these are the voids you're looking for
    def handle_all_the_things(self):
        #print("DEBUG : [ConnectionThread] handle_all_the_things")
        if self.is_connected():
            self.read_from_connection()
        else :
            if time.time()>self.time_of_last_attempt_to_connect :
                self.connect_to_server()
        if self.message_outbox_is_not_empty() :
            self.handle_message_outbox()
        if self.message_inbox_is_not_empty():
            self.handle_message_inbox()


    def run(self):

        while not self.finished.is_set() and self.failed_send_attempts<5:
            self.handle_all_the_things()
            time.sleep(0.005)
        if self.con :
            self.con.close()
