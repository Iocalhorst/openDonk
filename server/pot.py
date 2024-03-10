import os
import sys; sys.dont_write_bytecode = True
sys.path.append(os.getcwd() + '/..')
from common.common import *
assert COMMON_IMPORTS,"ERROR : [__main__] missing import"


from common.tools_for_fools import *
from common.view_model_factory import *
from common.view_model_controller import *



class Pot():
    def __init__(self,pot_id):
        self.total_amount=0
        self.pot_id=pot_id
        self.seat_ids=[]
        self.is_closed=False
        self.view_model=ViewModelFactory.create_pot_view_model()
        self.view_model_controller=PotViewModelController()
        # this is the seat were the pot will be shipped to,
        #it has to be set either in the show_down code block
        #or if its a non_showdown winner then it has to be set to the particular seat that was the only one with cards left after pot_consolidation
        self.winner_results=[]
    def initialize_view(self):
        self.view_model_controller.initialize(self)
    def get_view(self):
        self.initialize_view()
        return self.view_model.copy()
