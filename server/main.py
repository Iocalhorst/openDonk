import sys; sys.dont_write_bytecode = True
import os
sys.path.append(os.getcwd() + '/..')
from common.common import *
assert COMMON_IMPORTS,"ERROR : [__main__] missing import"

import logging
import random
#random.seed(9002) leads to strange dealer error on seat 2 after hand 41750
random.seed(9001) #hangs at "hands played :  63250"
from time import sleep
import json

from common.tools_for_fools import *
from command_thread import CommandThread
from server_thread import ServerThread
from table_thread import TableThread
from table_pool import TablePool,TableThreadPool
from player_pool import PlayerPool
from player import Player

from table_factory import *
from pprint import pprint
from common.player_database import player_database
NUM_TABLES=15


def main():
    print("openDonk(Server) v.0.0.0.43")

    cmd_thread=CommandThread()
    srv_thread=ServerThread()
    cmd_thread.start()
    srv_thread.start()

    TableThreadPool.proxy=srv_thread.server
    for i in range(NUM_TABLES):
        table=TableFactory.create_table_nlhe_6max()
        table.verify_integrity(silent=True)
        TablePool.register_table(table)
        TableThreadPool.register_table(table)

    TableThreadPool.start_all_tables()

    for player_id,player_name,player_avatar_filename in player_database :
        player=Player(player_id,player_name,player_avatar_filename)
        PlayerPool.register_player(player)
    PlayerPool.quick_start()


    exit_condition=False
    while exit_condition==False :
        if cmd_thread.has_command() :
            cmd=cmd_thread.get_command()
            if cmd=="start" :
                #if srv_thread.is_alive() :
                PlayerPool.quick_start()
                #print("server_thread is already running.")
                #lse :
                    #print("starting server_thread")
                    #srv_thread.start()
            elif cmd=="create table":
                table=TableFactory.create_table_nlhe_6max()
            elif cmd=="stop" :
                if srv_thread.is_alive() :
                    print("stopping server_thread")
                    srv_thread.cancel()
                    srv_thread.join(1)
                    print("done")
                    srv_thread=ServerThread()
                    print("ready to start again")
                else :
                    print("server_thread is not running.")
            elif cmd=="exit":
                cmd_thread.cancel()
                cmd_thread.join()
                print("ciao")
                exit_condition=True
            else :
                print(help_msg)
        else :
            if srv_thread :
                if srv_thread.is_alive() :
                    if srv_thread.is_happy():
                        srv_thread.handle_server()
                    else :
                        print("DEBUG : [main.srv_thread] PokerServer is not happy.")
                        cmd_thread.cancel()
                        cmd_thread.join()
                        srv_thread.cancel()
                        srv_thread.join()
                        assert False
                else :
                    print("DEBUG : [main.srv_thread] is dead")
                    cmd_thread.cancel()
                    cmd_thread.join()
                    srv_thread.cancel()
                    srv_thread.join()
                    assert False
                time.sleep(0.01) #breathing pause





    #print("INFO : creating Table")

if __name__=="__main__" :
    #for i in range(10000):
    main()
