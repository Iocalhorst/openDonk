import sys; sys.dont_write_bytecode = True
import os
sys.path.append(os.getcwd() + '/..')
from common.common import * #PokerMessageProtocol,PokerMessage and stuff
assert COMMON_IMPORTS,"ERROR : [__main__] missing import"

from debug_params import server_debug_params as debug_params
import socket
import time
from threading import Lock
mutex = Lock()
mutex2 = Lock()

class PokerConnection(): # aka "client_endpoint", pokermessageprotocol<->tcp_socket_handling
    def __init__(self,server_handle,socket_handle,client_addr,client_rfile,client_wfile):
        self.client_id=server_handle.get_client_id()
        self.server_id=server_handle.get_server_id()
        self.socket_handle=socket_handle
        self.client_rfile=client_rfile
        self.client_wfile=client_wfile
        self.client_addr=client_addr
        self.message_inbox=[]
        self.message_outbox=[]
        self.server_handle=server_handle

        self.alive=True
        self.frozen=False

    def is_frozen(self):
        return self.frozen
    def is_alive(self):
        return self.alive

    def message_outbox_push_tail(self,m):
        e="Error : [PokerConnection] message_outbox_push_tail"#== "+str(poker_message)
        assert m,e
        #print("DEBUG : [PokerConnection] message_outbox_push_tail")#.outbox_append] ",poker_message.head)
        self.message_outbox.append(m)

    def message_outbox_push_head(self,m):
        e="Error : [PokerConnection] message_outbox_push_head"#== "+str(poker_message)
        assert m,e
        #print("DEBUG : [PokerConnection] message_outbox_push_head")#.outbox_append] ",poker_message.head)
        self.message_outbox.insert(0,m)

    def message_outbox_pop_head(self):
        e="Error : [PokerConnection] message_outbox_pop_head"
        m=self.message_outbox.pop(0)
        assert m,e
        #print("DEBUG : [PokerConnection] message_outbox_pop_head")
        return m

    def message_outbox_pop_tail(self):
        e="Error : [PokerConnection] message_outbox_pop_tail"# == "+str(poker_message)
        m=self.message_outbox.pop()
        assert m,e
        #print("DEBUG : [PokerConnection] message_outbox_pop_tail")
        return m

    def message_inbox_push_head(self,m):
        e="Error : [PokerConnection] message_inbox_push_head"#== "+str(poker_message)
        assert m,e
        #print("DEBUG : [PokerConnection] message_inbox_push_head")#.outbox_append] ",poker_message.head)
        self.message_inbox.insert(0,m)

    def message_inbox_push_tail(self,m):
        e="Error : [PokerConnection] message_inbox_push_tail"# == "+str(poker_message)
        assert m,e
        #print("DEBUG : [PokerConnection] message_inbox_push_tail")#_message.head)
        self.message_inbox.append(m)

    def message_inbox_pop_head(self):
        e="Error : [PokerConnection] message_inbox_pop_head"# == "+str(poker_message)
        m=self.message_inbox.pop(0)
        assert m,e
        #print("DEBUG : [PokerConnection] message_inbox_pop_head")#_message.head)
        return m


    def message_inbox_pop_tail(self):
        e="Error : [PokerConnection] message_inbox_pop_tail"# == "+str(poker_message)
        m=self.message_inbox.pop()
        assert m,e
        #print("DEBUG : [PokerConnection] message_inbox_pop_tail")#_message.head)
        return m



    def message_inbox_is_not_empty(self):
        if len(self.message_inbox)>0 :
            return True
        else :
            return False
    def message_outbox_is_not_empty(self):
        if len(self.message_outbox)>0 :
            return True
        else :
            return False

    def kill(self):
        while self.message_inbox_is_not_empty() :
            m=self.message_inbox_pop_head()
            del m
        while self.message_outbox_is_not_empty() :
            m=self.message_outbox_pop_head()
            del m
        assert self.is_frozen()==True,"can not kill, con.is_frozen() != True "
        self.alive=False


    #TODO : review this. the namespace is also occupied/primed to dataclass decorator and friends.
    def freeze(self):
        self.frozen=True


    def __repr__(self):
        d={
          "type":"PokerConnection",
          "client_id":self.client_id,
          "server_id":self.server_id,
          "client_addr":str(self.client_addr),

        }
        return str(d)
    def handle_message_outbox(self):
        assert self.is_frozen()==False,"Error : [PokerConnection] handle_message_outbox() denied, con.is_frozen()"
        mutex2.acquire()

        m=self.message_outbox_pop_head()

        #print("DEBUG : [PokerConnection.handle_outbox] ",m.head)

        #self.mutex.acquire()
        time.sleep(0.01)
        if self.is_frozen()==True :
            self.message_outbox_push_head(m)
        else :

            self.send_message(m)
            time.sleep(0.015)
        mutex2.release()

    #def poll_rfile(self):
    #    data=self.client_rfile.read()
    #    print(data)
    #    print("poll")
    def send_message(self,m):
        mutex.acquire()
        assert self.is_frozen()==False,"attempted to send_message() on frozen connection. send_message is private and should not be called directly. could also be some other bug/race condition"

        try :

            debug_param=debug_params.get("debug_poker_connection_send_message")
            assert debug_param is not None,"debug_param nameError"
            if debug_param==True :
                print("DEBUG : [PokerConnection.send_message] sending : ",m.serialize().decode())
            #if poker_message.head["MESSAGE_TYPE"]=="PUSH_SEAT_EVENT":
                #print("DEBUG : [PokerConnection.send_message] SEAT_EVENT_TYPE : ",poker_message.body["SEAT_EVENT_TYPead)

            #time.sleep(0.015)
            self.client_wfile.write(m.serialize())
            time.sleep(0.01)
        except BlockingIOError: #socket.error:
            self.message_outbox_push_head(m)
            time.sleep(0.01)
        except ConnectionError :
            self.message_outbox_push_head(m)
            self.freeze()
            self.server_handle.disconnect_me(self.client_id)
        finally :
            mutex.release()
            #time.sleep(0.01)
            #self.server_handle.handle_error("ERROR_CONNECTION_SEND_MESSAGE_SOCKET_ERROR",self,poker_message)


            #self.server_handle.handle_error("ERROR_CONNECTION_SEND_MESSAGE",self,poker_message)

            #self.server_handle.bounce(self,message)
