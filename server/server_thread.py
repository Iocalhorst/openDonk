import sys; sys.dont_write_bytecode = True
import os
sys.path.append(os.getcwd() + '/..')
from common.common import * #PokerMessageProtocol,PokerMessage and stuff
assert COMMON_IMPORTS,"ERROR : [__main__] missing import"

from socketserver import *
from threading import Thread,Event,Lock
from table_pool import TablePool
from poker_connection import PokerConnection
import socket
import time
from debug_params import server_debug_params as debug_params


mutex3 = Lock()

class PokerRequestHandler(StreamRequestHandler):
    list_client_adresses=[]
    def handle(self):

        self.socket=self.request
        self.socket.setblocking(False)

        con=PokerConnection(self.server,self.socket,self.client_address,self.rfile,self.wfile)
        self.server.register_connection(con)
        while con.is_alive()==True :
            if con.is_frozen()==False:
                mutex3.acquire()
                self.socket.setblocking(False)
                try :
                    data=con.client_rfile.read()
                    if data :
                    #print(data)
                    #if data :": 42, "TIME_STAMP": 1707515611.9300644}, "body": {"REQUIRE": "TABLE_POOL_VIEW"}}

                    #print(data.decode())
                        msg=PokerMessage.deserialize(data.decode())
                        con.message_inbox_push_tail(msg)
                    time.sleep(0.02)
                except BlockingIOError:
                    time.sleep(0.005)
                except ConnectionError :
                    con.freeze()
                    con.server_handle.disconnect_me(con.client_id)
                except Exception as e:
                    print(str(e))
                    assert False,"ExceptionalExceptionError : not expected. bummer!"
                finally :
                    mutex3.release()
            time.sleep(0.005) #thread breathing pause

        #self.server.disconnect_me(con.client_id)
        print("DEBUG : [PokerRequestHandler] disconnecting ",con)



    def finish(self):
        if not self.wfile.closed:
            try:
                self.wfile.flush()
            except socket.error:
                # A final socket error may have occurred here, such as
                # the local error ECONNABORTED.
                print("ERROR : [PokerRequestHandler] self.finish() socket.error ",socket.error)
                self.wfile.close()
                self.rfile.close()


class PokerServer(ThreadingMixIn,TCPServer):
    allow_reuse_address = 1
    daemon_threads = True
    message_inbox=[]
    message_outbox=[]
    message_queue=[]
    #list_client_adresses=[]
    list_connections=[]
    list_id_con_pairs={}
    list_id_keepalive_pairs={}
    list_pinged_ids=[]
    list_dead_ids=[]
    server_id=42
    last_id=SERVER_ID_ADDRESS_SPACE
    server_instance=None
    is_happy_flag=False
    def is_happy():
        return PokerServer.is_happy_flag
    def disconnect_me(self,client_id):
        TablePool.unscubscribe_from_all_observers(client_id)
        if client_id not in PokerServer.list_dead_ids :
            PokerServer.list_dead_ids.append(client_id)
    def get_con(self,id):
        con=PokerServer.list_id_con_pairs[id]
        assert con,"no such id,con pair"
        return con
    def get_host(self):
        host,port=PokerServer.server_instance.socket.getsockname()[:2]
        return host,port
    def is_happy(self):
        return PokerServer.is_happy_flag
    def get_instance():
        if PokerServer.server_instance :
            return PokerServer.server_instance
        allow_reuse_address = 1
        bind=None
        port=server_port #common.py
        infos=socket.getaddrinfo(bind,port,type=socket.SOCK_STREAM,flags=socket.AI_PASSIVE,)
        family,type,proto,canonname,sockaddr=next(iter(infos))
        #TCP_Listener.address_family, addr = get_best_family(self.bind, self.port)
        PokerServer.adress_family=family
        PokerServer.server_instance=PokerServer(sockaddr,PokerRequestHandler)
        PokerServer.is_happy_flag=True
        return PokerServer.server_instance
    def get_info(self):
        assert False,"not implemented"
    def say_hi_to(self,client_adress):
        PokerServer.list_client_adresses.append(client_adress)
        print("hi ",client_adress)
    def get_client_id(self):
        PokerServer.last_id+=1
        return PokerServer.last_id
    def get_server_id(self):
        return PokerServer.server_id
    def register_connection(self,con):
        PokerServer.list_connections.append(con)
        PokerServer.list_id_con_pairs.setdefault(con.client_id)
        PokerServer.list_id_con_pairs[con.client_id]=con
        print("DEBUG : [PokerServer] register_connection - new connection registered")
        #print("DEBUG : [PokerServer] con[",con,"]")
        hello_message=PokerMessageProtocol.create("SERVER_HELLO",PokerServer.server_id,con.client_id)
        #head={"MESSAGE_TYPE" : "SERVER_HELLO"}
        #body={"CLIENT_ID":con.client_id,
        #      "REQUIRE":"CLIENT_HELLO"}
        #hello_msg=PokerMessage(PokerServer.server_id,con.client_id,head,body)
        #print("DEBUG : [PokerServer.message_queue.append] : ",hello_message)
        self.message_queue_push_tail(hello_message)
        #print("DEBUG : [PokerServer.message_queue] print : ",PokerServer.message_queue)
        PokerServer.list_id_keepalive_pairs.setdefault(con.client_id)
        PokerServer.list_id_keepalive_pairs[con.client_id]=time.time()+CONNECTION_TIMEOUT_THRESHOLD
    def handle_connections(self):
        for con in PokerServer.list_connections :
            if con.is_frozen()==False :
                if con.message_outbox_is_not_empty():
                    con.handle_message_outbox()
                if con.message_inbox_is_not_empty():
                    m=con.message_inbox_pop_head()
                    self.message_inbox_push_tail(m)

    def handle_connection_error(self,err_type,con,msg=None):
        print("ERROR : [PokerServer] handle_connection_error")
        print("DEBUG : [PokerServer] err_type = ",err_type)
        print("DEBUG : [PokerServer] con.client_id = ",con.client_id)
        print("DEBUG : [PokerServer] con.server_id = ",con.server_id)
        self.is_happy_flag=False

    def handle_message_queue(self):
        m=self.message_queue_pop_head()
        if m.is_from(PokerServer.server_id):
            self.message_outbox_push_tail(m)
        else :
            self.message_inbox_push_tail(m)

    def handle_message_outbox(self):
        message=self.message_outbox_pop_head()
        client_id=message.is_for()
        con=PokerServer.list_id_con_pairs.get(client_id)
        if con is not None :
            if con.is_frozen()==True :
                print("WARNING : [PokerServer.handle_message_outbox] con with client_id=",str(client_id)," is frozen! - dropping message")
            else :
                con.message_outbox_push_tail(message)
        else :
            print("WARNING : [PokerServer.handle_message_outbox] unknown client id in outgoing message - dropping message to CLIENT_ID : ",str(client_id))
            del message
            TablePool.unscubscribe_from_all_observers(client_id)

    def handle_message_inbox(self):#handle inbox
        m=self.message_inbox_pop_head()
        e="ERROR : [PokerServer.handle_message_inbox] ERROR_INVALID_MSG, DST_ID["+str(m.dst)+"] != PokerServer.server_id["+str(PokerServer.server_id)+"]"
        assert m.dst==PokerServer.server_id,e
        e="ERROR : [PokerServer.handle_message_inbox] ERROR_MSG_OUT_OF_BAND['"+m.typ+"'], SRC_ID["+str(m.src)+"] INVALID"
        assert m.src in PokerServer.list_id_con_pairs,e
        PokerServer.list_id_keepalive_pairs[m.src]=time.time()+CONNECTION_TIMEOUT_THRESHOLD

        if m.typ=="PONG" :
            ping_time=m.body.get("TIME_STAMP_PONG")-m.body.get("TIME_STAMP_PING")
            pong_time=time.time()-m.body.get("TIME_STAMP_PONG")
            ping_pong_time=pong_time+ping_time
            #print("DEBUG : [PokerServer.handle_message_inbox] received PONG")
            #print("DEBUG : [PokerServer.handle_message_inbox] ping : ",ping_time,", pong : ",pong_time," ping_pong : ",ping_pong_time)
            PokerServer.list_pinged_ids.remove(m.src)

        elif m.typ=="CLIENT_HELLO":
            if m.req=="TABLE_POOL_VIEW":
                table_pool_view=TablePool.get_view()
                res=PokerMessageProtocol.create("PUSH_TABLE_POOL_VIEW",PokerServer.server_id,m.src,payload=table_pool_view)
                self.message_outbox_push_tail(res)
        elif m.typ=="CLIENT_GOODBYE":
            self.disconnect_me(m.src)
            print("DEBUG : [PokerServer.handle_message_inbox] handling CLIENT_GOODBYE from CLIENT_ID ",m.src)
        elif m.typ=="SUBSCRIBE_TABLE_VIEW":
            table=TablePool.get_table_by_id(m.body.get("TABLE_ID"))
            table.observer.register_subscription(m.src)
            #NOT_IMPLEMENTED(m.typ)
        elif m.typ=="UNSUBSCRIBE_TABLE_VIEW":
            table=TablePool.get_table_by_id(m.body.get("TABLE_ID"))
            table.observer.unregister_subscription(m.src)
        else :
            NOT_IMPLEMENTED(m.typ)


    def message_queue_is_not_empty(self):
        if len(PokerServer.message_queue)>0 :
            return True
        else :
            return False

    def message_inbox_is_not_empty(self):
        if len(PokerServer.message_inbox)>0 :
            return True
        else :
            return False
    def message_outbox_is_not_empty(self):
        if len(PokerServer.message_outbox)>0 :
            return True
        else :
            return False
    def message_queue_pop_head(self):
        return PokerServer.message_queue.pop(0)
    def message_queue_pop_tail(self):
        return PokerServer.message_queue.pop()
    def message_inbox_pop_head(self):
        return PokerServer.message_inbox.pop(0)
    def message_inbox_pop_tail(self):
        return PokerServer.message_inbox.pop()
    def message_outbox_pop_head(self):
        return PokerServer.message_outbox.pop(0)
    def message_outbox_pop_tail(self):
        return PokerServer.message_inbox.pop()

    def message_queue_push_head(self,m):
        PokerServer.message_queue.insert(0,m)
    def message_queue_push_tail(self,m):
        PokerServer.message_queue.append(m)
    def message_inbox_push_head(self,m):
        PokerServer.message_inbox.insert(0,m)
    def message_inbox_push_tail(self,m):
        PokerServer.message_inbox.append(m)
    def message_outbox_push_head(self,m):
        PokerServer.message_outbox.insert(0,m)
    def message_outbox_push_tail(self,m):
        PokerServer.message_outbox.append(m)


    def clean_dead_connections(self):
        ids_to_remove=[]
        for id in PokerServer.list_dead_ids :
            #print("DEBUG : [PokerServer.clean_dead_connections] id : ",id)#PokerServer.list_dead_ids)
            #print(PokerServer.list_id_keepalive_pairs)
            #print(PokerServer.list_id_con_pairs)
            #assert id in PokerServer.list_id_keepalive_pairs,"ERROR : [PokerServer.clean_dead_connections] attempted to pop from empty list"
            PokerServer.list_id_keepalive_pairs.pop(id)
            con=PokerServer.list_id_con_pairs.pop(id)
            PokerServer.list_connections.remove(con)
            drop_messages=[]
            for m in PokerServer.message_queue :
                if m.id_to==id :
                    drop_messages.append(m)
            for drop_message in drop_messages :
                PokerServer.message_queue.remove(m)
            con.freeze()
            con.kill()
            ids_to_remove.append(id)
        for id in ids_to_remove:
            PokerServer.list_dead_ids.remove(id)

    def check_connections_keepalive(self):
        for id in PokerServer.list_id_keepalive_pairs:
            if PokerServer.list_id_keepalive_pairs.get(id)-time.time()<=0.0:
                if id in PokerServer.list_pinged_ids :
                    #print("DEBUG : [PokerServer.check_connection_keep_alive] ping timeout warning - connection listed dead")
                    PokerServer.list_dead_ids.append(id)
                else :
                    ping_message=PokerMessageProtocol.create("PING",PokerServer.server_id,id)
                    self.message_queue_push_tail(ping_message)
                    #print("DEBUG : [PokerServer.check_connection_keep_alive] keep_alive timeout warning - connection pinged")
                    PokerServer.list_pinged_ids.append(id)
                    PokerServer.list_id_keepalive_pairs[id]=time.time()+CONNECTION_TIMEOUT_THRESHOLD

class ServerThread(Thread):
    def __init__(self, args=None, kwargs=None):
        Thread.__init__(self,group=None,daemon=True)
        self.daemon=False

        #self.interval = interval
        #self.function = function
        #self.args = args if args is not None else []
        #self.kwargs = kwargs if kwargs is not None else {}
        self.daemon=True

        self.finished=Event()
        self.is_listening=False
        self.server=PokerServer.get_instance()
        self.is_happy_flag=True
    def cancel(self):
        self.server.shutdown()
        self.finished.set()
    def handle_server(self):
        if self.server.is_happy() :

            self.server.check_connections_keepalive()

            self.server.clean_dead_connections()

            if self.server.message_queue_is_not_empty():
                self.server.handle_message_queue()

            if self.server.message_outbox_is_not_empty():
                self.server.handle_message_outbox()

            self.server.handle_connections()

            if self.server.message_inbox_is_not_empty():
                self.server.handle_message_inbox()
        else :
            self.is_happy_flag=False

    def get_info(self):
        if self.server :
            return self.server.get_info()
        else :
            assert False,"there is no server"
    def is_happy(self):
        if not self.finished.is_set() and self.is_happy_flag and self.server.is_happy():
            return True
        else :
            return False
    def run(self):
        #allow_reuse_address = 1
        #infos=socket.getaddrinfo(self.bind,self.port,type=socket.SOCK_STREAM,flags=socket.AI_PASSIVE,)
        #family,type,proto,canonname,sockaddr=next(iter(infos))
        ##TCP_Listener.address_family, addr = get_best_family(self.bind, self.port)
        #PokerServer.adress_family=family
        #sockaddr,PokerRequestHandler

        #
        #host,port=self.server.get_host()#socket.getsockname()[:2]
        try:
        #    print(f"DEBUG : [server_thread] server socket listening on {host} port {port} ")
            self.server.serve_forever()
            #print("serving...")
        except Exception as ex:
            e="ERROR : [daemon] failed to keep listening cause of "+str(ex)
            print(e)
            exit(69)
            self.is_happy_flag=False
        #self.finished.wait(self.interval)
        print("end of server_thread.run")
        #if not self.finished.is_set():
        #    if self.is_listening :
        #        self.listen()
        #    else :
        #        self.function(*self.args, **self.kwargs)
