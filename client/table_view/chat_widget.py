import pyray
import os
import sys; sys.dont_write_bytecode = True
import socket
import random


def create_log_socket():
    ip = "127.0.0.1"
    port = 6969
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = (ip, port)
    s.bind(server_address)
    s.setblocking(0)
    return s

class ChatLog():
    def __init__(self,line_wrap):
        self.entries=[]
        self.log_sock=create_log_socket()
        self.header="##### Monitor listening on 127.0.0.1:6969 #####"
        self.clear_log()
        self.packet_counter=0
    #    self.line_wrap=line_wrap

    def push(self,entry):
        self.entries.append(entry)


    def clear_log(self):
        self.packet_counter=0
        self.entries.clear()
        self.entries.append(self.header)
        line="random nr : "+str(random.randint(0,10000))
        self.entries.append(line)

    def get_entries(self):
        list_entries=[]
        for index,entry in enumerate(self.entries):
            list_entries.append((index,entry))
        return list_entries

    def poll(self):
        try :
            data, address = self.log_sock.recvfrom(4096)
            if data :

            #print(data.decode('utf-8'), end='')
                msg=str(data.decode())
                if msg=='clear' :
                    self.clear_log()
                    #self.packet_counter+=1
                    #print(self.packet_counter)
                else :
                    msgs=msg.split('\n')#
                    ms=[]
                    for m in msgs :
                        m.strip()
                        #m.trim()
                        if len(m)>2 :
                            self.push(m)
                            #self.packet_counter+=1
                            #print(self.packet_counter)

                        #    print(m)
                            #self.push(l)
                #print(msg,end='')
        except :
        #    print(e)
            pass
            #print("oops")
            #exit(69)
        #    pass
                #assert False,str(data)


class ChatWidget():
    def __init__(self,font):
        self.bg=pyray.Color(42,39,35,255)
        self.x=0
        self.y=0.73#0.775
        self.w=0.4825#45#0.41
        self.h=1-self.y
        self.border_w=0.005
        self.line_wrap=88
        self.chat_log=ChatLog(self.line_wrap)
        self.font=font
        self.font_size=10
        self.font_color=pyray.Color(255,224,192,192)

    def draw(self,w,h):
        self.chat_log.poll()
        border=int(w*self.border_w)
        rx=int(self.x*w)
        ry=int(self.y*h)
        rw=int(self.w*w)
        rh=int(h*self.h)
        pyray.draw_rectangle(rx,ry,rw,rh,pyray.Color(127,127,127,255))
        pyray.draw_rectangle(rx+border,ry+border,rw-2*border,rh-2*border,self.bg)
        indexed_lines=self.chat_log.get_entries()
        wrapped_lines=[]
        for idx,line in indexed_lines :
            s=""
            chars_left=self.line_wrap
            for char in line:
                s+=char
                chars_left-=1
                if chars_left==0 :
                    wrapped_lines.append(s)
                    s=""
                    chars_left=self.line_wrap
            if len(s)>0 :
                wrapped_lines.append(s)

        cursor_x=int(rx+2*border)
        cursor_y=int(ry+2*border)
        self.font_size=rh*0.05
        char_height=int(self.font_size)
        max_lines_count=20#rh//(se)



        while len(wrapped_lines)>=max_lines_count :
            l=wrapped_lines[0]
            wrapped_lines.remove(l)

        for line in wrapped_lines :
            #s=""
            #if idx<10 :
            #    s+="  "
            #elif idx<100 :
            #    s+=" "
            #s+=str(idx)+":"+line
            pyray.draw_text_ex(self.font,line,(cursor_x,cursor_y),self.font_size,0,self.font_color)
            cursor_y+=char_height

    #def poll_log(self):
