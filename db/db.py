import json
from pprint import pprint
import sys; sys.dont_write_bytecode = True
import os
sys.path.append(os.getcwd() + '/..')
from common.common import *
assert COMMON_IMPORTS,"ERROR : [__main__] missing import"
import sqlite3
class ServerDatabase():
    def __init__(self,cfg):
        self.cfg=cfg
        path=cfg.get("db_scripts_filename")
        file=open(path,'r')
        data=file.read()
        file.close()
        self.scripts=json.loads(data)
        self.con = sqlite3.connect(cfg.get("db_sqlite_filename"))
        self.cur=self.con.cursor()
        print("connected to sqlite db")
        self.has_done_changes=False

    def run_cmd(self,cmd,verbose=True):
        if cmd.startswith("SELECT")!=True :
            self.has_done_changes=True
        print(cmd)
        try :
            res=self.cur.execute(cmd)
            for r in res.fetchall() :
                print(r)
        except Exception as e:
            print(e)
    def run_script(self,script_name):
        for cmd in self.scripts.get(script_name):
            self.run_cmd(cmd)
        if script_name!="show":
            print("Don't forget to commit!")
    def has_committed(self):
        if self.has_done_changes==True:
            return False
        return True
    def commit(self):
        self.con.commit()
        print("done")
        self.has_done_changes=False
