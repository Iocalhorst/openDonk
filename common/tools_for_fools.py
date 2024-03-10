import socket
import sys; sys.dont_write_bytecode = True
import logging
import time
import inspect
import pprint
from common.common import *



def pr1nt(*args):
    no_debug=True
    if no_debug==True :
        return
    else :
        for arg in args :
            print(arg,end="")
        print("")

def padl(s,p):

    str_s=str(s)
    if len(str_s)>p :
        l0g("padding fail")
        exit(69)
    else :
        str_s+=" "*(p-len(str_s))
        return str_s

ip = '127.0.0.1'
port = 6969
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
packet_count=0
def l0g(tag,payload):
    return
    msg=tag+" : "+payload
    #msg.strip("\n")
    global packet_count
    for m in msg.split("\n") :
        if len(m)>2 :
            sock.sendto(m.encode(), (ip, int(port)))
            sock.sendto(b'\x0a', (ip, int(port)))
            packet_count+=1
            #print(packet_count)
            time.sleep(0.0001)



TODO_COUNT=0
def TODO(s):
    global TODO_COUNT
    #package,module,klass,caller,line=get_caller_info()
    #m="TODO : "+"["+klass+caller+" LINE "+line+"]"+s

    m="TODO"+TODO_COUNT*"O"+" : "+s
    TODO_COUNT+=1

    print(m)

def NOT_IMPLEMENTED(message):
#    package,module,klass,caller,line=get_caller_info()

    s="ERROR : [?] "+"NOT_IMPLEMENTED"+" "+message
    assert False,s


    #if public :
    #    print(msg)
