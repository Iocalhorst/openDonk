import sys; sys.dont_write_bytecode = True
import os
sys.path.append(os.getcwd() + '/..')
from common.common import *
assert COMMON_IMPORTS,"ERROR : [__main__] missing import"

class TableObserver():
    def __init__(self):
        self.subscribers=[]
        self.subject=None
        self.proxy=None
    def set_proxy(self,proxy):
        #print("set proxy")
        self.proxy=proxy

    def has_subscription_from_client_id(self,client_id):
        if client_id in self.subscribers :
            return True
        else :
            return False
    def unregister_subscription(self,client_id):
        if client_id in self.subscribers :
            self.subscribers.remove(client_id)
            print("DEBUG : [TableObserver] unregistering CLIENT_ID ",client_id," from TABLE ",self.subject.table_name," TABLE_ID ",self.subject.table_id)
    def register_subscription(self,client_id):
        assert self.subject,"ERROR [TableObserver.register_subsciber] self.table==None"
        assert client_id not in self.subscribers,"duplicate subscription, verboden!"
        self.subscribers.append(client_id)
        table_view_data=self.subject.get_view()
        payload={
            "TABLE_ID":self.subject.table_id,
            "TABLE_NAME":self.subject.table_name,
            "TABLE_VIEW_DATA":table_view_data
        }
        m=PokerMessageProtocol.create("PUSH_TABLE_VIEW",self.proxy.server_id,client_id,payload)
        e="Error : [TableObserver.handle_push_table_view] PokerMessageProtocol.create() returned : "+str(m)
        assert m,e
        self.proxy.message_outbox_push_tail(m)


            #con.handle_message_outbox()

    def observe(self,subject):
        self.subject=subject
        self.subject.set_observer(self)
        #self.view_model=subject.view_model
        #self.view_model_controller=subject.view_model_controller
        #self.view_model_controller.initialize(self.view_model,subject)
    def handle_table_event(self,table_event_type=None,table_event_data=None):



        assert table_event_type is not None,"invalid table_event_type : None"
        assert table_event_data is not None,"invalid table_event_data : None"
        #time.sleep(0.1)
        table_id=self.subject.table_id
        assert table_id is not None,"uhm ... "
        payload={
            "TABLE_ID":table_id,
            "TABLE_EVENT_TYPE":table_event_type,
            "TABLE_EVENT_DATA":table_event_data,
        }

        for subscriber in self.subscribers :
            m=PokerMessageProtocol.create("PUSH_TABLE_EVENT",self.proxy.server_id,subscriber,payload)
            e="Error : [TableObserver.handle_pot_event] PokerMessageProtocol.create() returned : "+str(m)
            assert m,e
            #con=self.proxy.get_con(subscriber)
            #con.message_outbox_push_tail(m)
            self.proxy.message_outbox_push_tail(m)
        pr1nt("DEBUG : [observer] handle_table_event")
        
        self.handle_push_table_view()


    def handle_push_table_view(self):
        table_view_data=self.subject.get_view()
        payload={
            "TABLE_ID":self.subject.table_id,
            "TABLE_NAME":self.subject.table_name,
            "TABLE_VIEW_DATA":table_view_data
        }
        for subscriber in self.subscribers :
            m=PokerMessageProtocol.create("PUSH_TABLE_VIEW",self.proxy.server_id,subscriber,payload)
            e="Error : [TableObserver.handle_push_table_view] PokerMessageProtocol.create() returned : "+str(m)
            assert m,e
            #con=self.proxy.get_con(subscriber)
            #con.message_outbox_push_tail(m)
            #con.handle_message_outbox()
            self.proxy.message_outbox_push_tail(m)
