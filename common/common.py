COMMON_IMPORTS=True

SERVER_ID_ADDRESS_SPACE=10000
server_ip = '127.0.0.1'
server_port = 5555
CONNECTION_TIMEOUT_THRESHOLD=5.0
import json
import time
from common.tools_for_fools import *
from pprint import pprint



class PokerMessage():
    def __init__(self,head,body):
        self.id_from=head.get("SRC_ID")
        self.id_to=head.get("DST_ID")
        self.head=head
        self.body=body
        self.typ=head.get("MESSAGE_TYPE")
        self.req=body.get("REQUIRE")
        self.src=head.get("SRC_ID")
        self.dst=head.get("DST_ID")

        #print("DEBUG : [PokerMessage.__init__] head : ",head)
        #print("DEBUG : [PokerMessage.__init__] body : ",body)
    def is_from(self,id=None):
        if id :
            if self.id_from==id :
                #print("DEBUG : [PokerMessage.is_from] param[id]==",id," ,self.id_from==",self.id_from," ,returning True")
                return True
            else :
                #print("DEBUG : [PokerMessage.is_from] param[id]==",id," ,self.id_from==",self.id_from," ,returning False")
                return False
        else :
            #print("DEBUG : [PokerMessage.is_from] param[id]==None, returning ",self.id_from)
            return self.id_from
    def is_for(self,id=None):
        if id :
            if self.id_to==id :
                #print("DEBUG : [PokerMessage.is_for] param[id]==",id," ,self.id_to==",self.id_to," ,returning True")
                return True
            else :
                #print("DEBUG : [PokerMessage.is_for] param[id]==",id," ,self.id_to==",self.id_to," ,returning False")
                return False
        else :
            return self.id_to
    def serialize(self):
        data={
            "id_from":self.id_from,
            "is_from":self.is_from(),
            "id_to":self.id_to,
            "is_for":self.is_for(),
            "head":self.head,
            "body":self.body
        }
        #print("DEBUG : [PokerMessage.serialize] ",data)
        #data={self.id_from,self.id_to,self.head,self.body}
        s=""
        try :
            s=json.dumps(data)
            return s.encode()
        except Exception as e:
            print("serialization failed, data : ")
            pprint(str(data))
            print(e)

    def deserialize(json_string):
        #data=json_string

        data=json.loads(json_string)
        #except:
        #    e="Error : [PokerMessage.deserialize] json error, invalid message"
        #    print("json_string : ",json_string)
        #    assert False,e
        #    raise
        #    exit(69)

        #e="Error : [PokerMessage.deserialize] verification failed"
        #assert PokerMessage.verify(data),e
        return PokerMessage(data.get("head"),data.get("body"))


class PokerMessageProtocol():
    def create(message_type,id_from,id_to,payload=None):
        head={"MESSAGE_TYPE":message_type,
              "SRC_ID":id_from,
              "DST_ID":id_to,
              "TIME_STAMP":time.time()
              }
        body=None
        #print(head,payload)
        if message_type=="SERVER_HELLO":
            body={
                "REQUIRE":"CLIENT_HELLO",
                "SERVER_ID":id_from,
                "CLIENT_ID":id_to,
                 }
        elif message_type=="CLIENT_GOODBYE":
            body={
                "REQUIRE":"NOTHING",
                "CLIENT_ID":id_from
                }
        elif message_type=="CLIENT_HELLO":
            body={
                "REQUIRE":"TABLE_POOL_VIEW",
            }
        elif message_type=="PUSH_TABLE_POOL_VIEW":
            body={
                "REQUIRE":"NOTHING",
                "TABLE_POOL_VIEW":payload
                }
        elif message_type=="PING":
            body={
                "REQUIRE":"PONG",
                "TIME_STAMP_PING":time.time(),
                }
        elif message_type=="PONG":
            body={
                "REQUIRE":"NOTHING",
                "TIME_STAMP_PING":payload.get("TIME_STAMP_PING"),
                "TIME_STAMP_PONG":time.time(),
                }
        elif message_type=="PUSH_TABLE_VIEW":
            #pprint(payload)
            #assert False
            body={
                "REQUIRE":"NOTHING",
                "TABLE_ID":payload.get("TABLE_ID"),
                "TABLE_VIEW_DATA":payload.get("TABLE_VIEW_DATA"),
                }
        elif message_type=="PUSH_TABLE_EVENT":
                #pprint(payload)
                #assert False
                #print("DEBUG : [PokerMessageProtocol.create] payload = ",payload)
                table_id=payload.get("TABLE_ID")
                assert table_id is not None
                table_event_type=payload.get("TABLE_EVENT_TYPE")
                assert table_event_type is not None
                table_event_data=payload.get("TABLE_EVENT_DATA")
                assert table_event_data is not None

                body={
                    "REQUIRE":"NOTHING",
                    "TABLE_ID":table_id,
                    "TABLE_EVENT_TYPE":table_event_type,
                    "TABLE_EVENT_DATA":table_event_data,
                    }
        elif message_type=="SUBSCRIBE_TABLE_VIEW":
            body={
                "TABLE_ID":payload.get("TABLE_ID"),
                "TABLE_NAME":payload.get("TABLE_NAME"),
                "REQUIRE":"PUSH_TABLE_VIEW"
            }
        elif message_type=="UNSUBSCRIBE_TABLE_VIEW":
            body={
                "TABLE_ID":payload.get("TABLE_ID"),
                "TABLE_NAME":payload.get("TABLE_NAME"),
                "REQUIRE":"NOTHING"
            }
            #print(
            #print(body)
            #assert False
        #elif message_type=="PUSH_SEAT_EVENT":
        #    body={
        #        #"TABLE_ID":payload.get("TABLE_ID"),
        #        #"TABLE_NAME":payload.get("TABLE_NAME"),
        #        "SEAT_EVENT_DATA":payload.get("SEAT_EVENT_DATA"),
        #        "REQUIRE":"NOTHING"
        #    }
        #    print("DEBUG : [PokerMessageProtocol.create_message()] SEAT_EVENT : ",payload)
        #    #print(body)
        #    #assert False
        #elif message_type=="PUSH_POT_EVENT":
        #    body={
        #        #"TABLE_ID":payload.get("TABLE_ID"),
        #        #"TABLE_NAME":payload.get("TABLE_NAME"),
        #        "POT_EVENT_DATA":payload.get("POT_EVENT_DATA"),
        #        "REQUIRE":"NOTHING"
        #    }
        #    #print("DEBUG : [PokerMessageProtocol.create_message()] SEAT_EVENT : ",payload)
        #    #print(body)
        #    #assert False,"NOT IMPLEMENTED"
        #elif message_type=="PUSH_DEALER_EVENT":
        #    body={
        #        #"TABLE_ID":payload.get("TABLE_ID"),
        #        #"TABLE_NAME":payload.get("TABLE_NAME"),
        #        "DEALER_EVENT_DATA":payload.get("DEALER_EVENT_DATA"),
        #        "REQUIRE":"NOTHING"
        #    }
        #    #print("DEBUG : [PokerMessageProtocol.create_message()] SEAT_EVENT : ",payload)
        #    #print(body)
        #    #assert False,"NOT IMPLEMENTED"

        else :
            e="ERROR : [PokerMessageProtocol.create] invalid message_type : '"+message_type+"'"
            assert False,e
            exit(69)
        poker_message=PokerMessage(head,body)
        return poker_message
