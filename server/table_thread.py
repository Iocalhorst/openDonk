import os
import sys; sys.dont_write_bytecode = True
sys.path.append(os.getcwd() + '/..')
from common.common import *
assert COMMON_IMPORTS,"ERROR : [__main__] missing import"

from threading import Thread,Event





class TableThread(Thread):
    def __init__(self, table,args=None, kwargs=None):
        Thread.__init__(self,group=None,daemon=False)
        self.daemon=False
        self.table=table
        self.finished=Event()

        #self.server_id=PokerServer.server_id
    #    self.proxy=proxy

        self.proxy=None
        self.speed_factor=5
    def set_table_speed(self,factor):
        if factor>=1 and factor <=100 :
            self.speed_factor = factor
    def set_proxy(self,proxy):
        self.proxy=proxy
    def cancel(self):
        self.finished.set()

    def initialize_table(self):
    #    self.table.observer.set_proxy(self.proxy)
        self.table.initialize_view()
        #pprint(self.table.get_view())
        self.table.observer.set_proxy(self.proxy)

    def run(self):
        assert self.proxy,"table_thread proxy uninitialized"
        print("DEBUG : [table_thread] table_id : ",self.table.table_id," started")
        self.initialize_table()

        #self.s3tup()
#        for player in players:
#	        self.table.get_seat(player)
#
#        self.table.start()

        while not self.finished.is_set():
            time.sleep(0.05*self.speed_factor)
            if self.table.has_nothing_to_do() :
                if self.table.has_enough_players():
                    if self.table.dealer.has_not_announced_to_start_soon():
                        self.table.dealer.announce_to_start_in(5.0)
                    elif self.table.dealer.time_has_come_to_start():
                        if self.table.has_enough_players():
                            self.table.dealer.initialize_hand()
                            #self.table.dealer.commit_players()
                        else :
                            self.table.dealer.cancel_announcement()
                else :
                    #l0g("table_thread","not enough players")
                    time.sleep(0.05)
            else :
                self.table.advance_dealer()

                #l0g("table_thread","nothing to do or not enough players")
            #    time.sleep(0.005*self.speed_factor)

    #    for table in TablePool.tables :
