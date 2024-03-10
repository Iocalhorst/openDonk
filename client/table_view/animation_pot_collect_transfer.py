class AnimationPotCollectTransfer():
      def __init__(self,pot_widget,seat_widget,value):
          self.pot_widget=pot_widget
          self.seat_widget=seat_widget
          self.value=value
          self.t0=0
          self.t1=0
          self.t=0
          self.duration=1.5
          self.runtime=0
          self.running=False
          self.pending=True
          self.finished=False
          self.origin_rel_x=seat_widget.chips_inline_rel_x
          self.origin_rel_y=seat_widget.chips_inline_rel_y
          self.target_rel_x=pot_widget.rel_x
          self.target_rel_y=pot_widget.rel_y
          self.rel_x=self.origin_rel_x
          self.rel_y=self.origin_rel_y

      def is_pending(self):
          return self.pending
      def is_running(self):
          return self.running
      def is_finished(self):
          return self.finished
      def set_t0(self,t0):
          self.t0=t0
          assert self.duration,"duration is None"
          assert self.duration>0.01,"duration is too small(<=0.01 seconds)"
          assert self.duration<10.0,"duration is too big (>=10.0 seconds)"
          self.t1=t0+self.duration
      def set_duration(self,duration):
          self.duration=duration
      def start_at(self,moment_of_time):
          assert self.is_pending()==True,"failed to start pot collect transfer animation, self.is_pending() != False"
          self.set_t0(moment_of_time)
          self.runtime=0.0
          self.t=0.001 #dont want to div0 accidently
          self.pending=False
          self.running=True
          self.finished=False
          self.pot_widget.pending_value+=self.value

      def update_self(self,moment_of_time):
          if self.is_pending()==True or self.is_running()==False:
              return
          self.runtime=moment_of_time-self.t0
          #print("DEBUG : [anim] runtime == ",round(self.runtime,3))
          if self.runtime>=self.duration :
              self.t=1.0
              self.finished=True
              self.pot_widget.pending_value-=self.value
              self.value=0
              self.running=False
              self.runtime=self.duration
              #print("DEBUG : [anim] runtime == ",round(self.runtime,3))
              #print("DEBUG : [anim] t == ",round(self.t,3))
          else :
              assert self.runtime>0.0,"animation runtime below 0"
              assert self.runtime<=self.duration,"animation runtime above duration"
              self.t=self.runtime/self.duration
              #print("DEBUG : [anim] t == ",round(self.t,3))


          x0=self.origin_rel_x
          y0=self.origin_rel_y
          x1=self.target_rel_x
          y1=self.target_rel_y
          dx=x1-x0
          dy=y1-y0
          self.rel_x=x0+dx*self.t
          self.rel_y=y0+dy*self.t
          #print("DEBUG : [anim] rel_x == ",round(self.rel_x,3),", rel_y == ",round(self.rel_y,3),", chip_count : ",self.chip_count)
          #print("DEBUG : [anim] self.seat_widget.chips_inline == ",self.seat_widget.chips_inline)
          #print("DEBUG : [anim] self.seat_widget.pending_chips_inline == ",self.seat_widget.pending_chips_inline)
          #print("DEBUG : [anim] self.seat_widget.get_chips_inline() == ",self.seat_widget.get_chips_inline())
      def get_render_params(self):
          return self.rel_x,self.rel_y,self.value
