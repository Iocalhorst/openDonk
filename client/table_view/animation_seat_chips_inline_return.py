import time
class AnimationSeatChipsInlineReturn():
      def __init__(self,player_info_widget,seat_widget,value):
          self.seat_widget=seat_widget
          self.player_info_widget=player_info_widget
          self.value=value
          #self.player_info.pending_chips_inline+=self.chip_count
          self.t0=0
          self.t1=0
          self.t=0
          self.duration=1.0
          self.runtime=0
          self.running=False
          self.finished=False
          self.pending=True
          self.target_rel_x=seat_widget.rel_x
          self.target_rel_y=seat_widget.rel_y
          self.origin_rel_x=seat_widget.chips_inline_rel_x
          self.origin_rel_y=seat_widget.chips_inline_rel_y

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
      def set_duration(self,duration=1.0):
          self.duration=duration
      def start_now(self):
          assert self.is_pending()==True,"failed to start inline return animation, reson self.is_pending() != True"
          self.set_t0(time.time())
          self.pending=False
          self.runtime=0.0
          self.t=0.001 #dont want to div0 accidently
          self.running=True
          self.finished=False
          self.player_info_widget.pending_chips_behind+=self.value

          #print("DEBUG : [inline_put_anim] : t0 : ",round(self.t0,3),", d : ",round(self.duration,3),", t1 : ",round(self.t1,3))
      def update_self(self):
          if self.is_pending()==True or self.is_running()==False:
              return
          self.runtime=time.time()-self.t0
          #print("DEBUG : [anim] runtime == ",round(self.runtime,3))
          if self.runtime>=self.duration :
              self.t=1.0
              self.finished=True
              self.running=False
              self.runtime=self.duration
              self.player_info_widget.pending_chips_behind-=self.value
              self.value=0
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

      def get_render_params(self):
          return self.rel_x,self.rel_y,self.value
          #pyray.draw_line(int(x0),int(y0),int(x1),int(y1),pyray.Color(192,182,162,255))
          #pyray.draw_circle(int(t_x),int(t_y),5.0,pyray.Color(180,120,54,128))
