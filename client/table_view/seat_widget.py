import time

class SeatWidget():
    def __init__(self,seat_id,card0,card1):
        self.rel_x=0.1
        self.rel_y=0.1
        self.rel_r=0.1
        self.seat_id=seat_id
        self.player_id=-1
        self.player_name=None
        self.player_avatar_filename=None

        self.alignment="uninitialized"        
        self.chips_behind=None
        self.pending_chips_inline=0
        self.chips_inline=0
        self.holdcard_ids=[None,None]
        self.chips_inline_rel_x=0
        self.chips_inline_rel_y=0
        self.button_rel_x=0
        self.button_rel_y=0
        self.avatar=None
        self.overlay=None
        self.overlay_expires_at=time.time()-1.0
        self.card_widgets=[card0,card1]
        self.show_dealer_button=False
        self.has_focus=False
        self.default_avatar=None

    def set_temporary_overlay(self,overlay,duration=1.0):
        print("temporary overlay id:",overlay.id,", duration:",duration,", seat_id : ",self.seat_id)
        assert overlay,"Error [SeatWidget.set_temporary_overlay] overlay is None "
        assert duration>0.1,"Error [SeatWidget.set_temporary_overlay] duration is not >0.1"
        assert duration<=30.0,"Error [SeatWidget.set_temporary_overlay] duration>30.0"
        self.overlay_expires_at=duration+time.time()
        self.overlay=overlay
    def set_avatar(self,avatar):
        self.avatar=avatar
    def get_avatar(self):
        #assert self.avatar,"ERROR : [SeatWidget.get_avatar] None, avatar should always be 'seat_open' when theres no player"
        if self.avatar is None or self.player_id<0 :
            return self.default_avatar
        if time.time()<self.overlay_expires_at:
        #    print(self.overlay)
            return self.overlay
        else :
            assert self.avatar,"ERROR : [SeatWidget.get_avatar] None, avatar should always be 'seat_open' when theres no player"
            return self.avatar

    def get_chips_inline(self):
        current_chip_count=self.chips_inline-self.pending_chips_inline
        if current_chip_count<0 :
            return 0
        else :
            return current_chip_count
    #def draw(self):
