import json
from pprint import pprint
import sys; sys.dont_write_bytecode = True
import os
sys.path.append(os.getcwd() + '/..')
from common.common import *
assert COMMON_IMPORTS,"ERROR : [__main__] missing import"
import sqlite3
from db import ServerDatabase
from common.tools_for_fools import *

#from db_bootstrap import db_bootstrap_json_string
db_path="/home/localhorst/Documents/dev/openDonk/latest/db/"
#db_bootstrap_filename="db_bootstrap.json"
#db_dump_filename="db_dump.json"
db_cfg_filename="db_cfg.json"#db_sqlite_filename=path_db+"db.sqlite"


if __name__=="__main__" :

    #db=ServerDatabase()
    #exit_condition=False
#    if os.path.exists(db_sqlite_filename):
#        s=db_sqlite_filename+" exists"+"\n"+"overwrite? 'yes' to confirm.\n"+">"
#        cmd=input(s)
#        if cmd=="yes":
#            os.remove(db_sqlite_filename)
#            bootstrap_flag=True
#        s="run bootstrap script? 'no' to leave the new file empty.\n"+">"
#        cmd=input(s)
    db_cfg_filepath=db_path+db_cfg_filename
    cfg_file=open(db_cfg_filepath,'r')
    db_cfg=json.loads(cfg_file.read())
    cfg_file.close()
    print(db_cfg)
    db=ServerDatabase(db_cfg)
    usage="available commands : show bootstrap commit exit"
    print(usage)
    while True :
        cmd=input(">")
        if cmd=="exit":
            if db.has_committed()==False :
                print("You didnt commit the changes! type 'commit' or hit enter to exit without saving")
                cmd=input(">")
                if cmd=="commit" :
                    db.commit()
                    exit(0)
                elif cmd=="":
                    print("ciao")
                    exit(0)
            else :
                print("ciao")
                exit(0)
        elif cmd=="show":
            db.run_script("show")
        elif cmd=="commit":
            db.commit()
        elif cmd=="bootstrap":
            db.run_script("bootstrap")
        else :
            print(usage)
        #try :
        #    res=cur.execute(cmd)
        #    a=res.fetchone()
        #    print(a)
        #except Excepten as E:
        #    print(E)


    #db.show()
    #out_file_path=path_db+db_dump_filename
    #db.dump(out_file_path)
