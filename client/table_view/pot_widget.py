#import chips
import pyray


#a potwidget represents a pot_view_model object from the table.dealer.closed_pots[] list, where index==0 always is the "main", >0 always is "side" pot
class PotWidget():
    def __init__(self,pot_id):
          self.value=0
          self.pot_id=pot_id
          self.rel_x=0.1
          self.rel_y=0.1
          self.pending_value=0
    def get_render_params(self):
          chip_count=self.value-self.pending_value
          if chip_count<=0 :
                chip_count=0
          return self.rel_x,self.rel_y,chip_count

    #
    # anyone?
    #
    #def update(self,params):
    #    valid_keys={"pos_x","pos_y","chip_count"}
    #    for key in params :
    #        e="ERROR : [PotWidget] .update - invalid key["+str(key)+"] in params"
    #        assert key in valid_keys,e
    #        value=params.get(key)
    #        if key=="pos_x" :
    #            self.pos_x=value
    #        elif key=="pos_y" :
    #            self.pos_y=value
    #        elif key=="chip_count" :
    #            self.chip_count=value
    #        else :
    #            e="ERROR : [PotWidget.update] : UNREACHABLE, "+str(key)+" : "+str(value)
    #            assert False,e
    #def create_pot_transfer_animation(self,seat_widget,chip_count):
    #      new_pot_transfer_animation=PotTransferAnimation(seat_widget,chip_count)
    #      new_pot_transfer_animation.set_duration(self.default_transfer_animation_duration)
    #      self.pot_transfer_animations.append(new_pot_transfer_animation)
    #def start_pending_transfer_animations(self):
    #    moment_of_time=time.time()
    #    for pot_transfer_animation in self.pot_transfer_animations:
    #        if pot_transfer_animation.is_pending():
    #            pot_transfer_animation.start_at(moment_of_time)


                #set_origin(self,src_x,src_y)
                #set_target(self,dst_x,dst_y)
                #update_dimensions(self,width,height)
                #set_duration(self,duration):
                #start_animation(self):


    #def update_transfer_tanimations(self):
    #    moment_of_time=time.time()
    #    for pot_transfer_animation in self.pot_transfer_animations:
    #        pot_transfer_animation.update_self(moment_of_time)

    #def update_table_dimensions(self,table_x,table_y,table_size,color_theme):
    #    self.table_x=table_x
    #    self.table_y=table_y
    #    self.color_theme=color_theme
    #    self.table_size=table_size

    #    self.scale=self.table_size*0.1
    #    self.base_x=int(self.table_x+table_size*self.pos_x)#*w-((tex.width*scale)//2)
    #    self.base_y=int(self.table_y+table_size*self.pos_y)

    ##@params
    #
    #         base_x     : absolute position in pixelspace the "bottom"-chips for each type.
    #         base_y     : absolute position in pixelspace of the "bottom"-chip
    #         chip_count :


    #def draw_self(self):

    #    #print(base_x," ",base_y)
    #    #exit(60)
    #    if debug_params.get("show_pot_overlay")==True :
    #        pyray.draw_circle(self.base_x,self.base_y,1.5*self.scale,self.color_theme.get("pot_border"))
    #        pyray.draw_circle(self.base_x,self.base_y,1.5*self.scale*0.9,pyray.Color(0,0,0,32))#color_theme.get("table_surface"))
    #    else :
    #        assert False,"Error [PotWidget] draw_self, debug_params.show_pot_overlay != True"

    #    #real means the amount that is specified and
    #    real_chip_count=self.chip_count
    #    for pot_transfer_animation in self.pot_transfer_animations :
    #        real_chip_count-=pot_transfer_animation.chip_count
    #    self.draw_chip_stack(self.base_x,self.base_y,self.chip_count,self.chip_set)
