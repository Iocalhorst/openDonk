class PlayerInfoWidget():
    def __init__(self,seat_id):
        self.rel_x=None
        self.rel_y=None
        self.rel_h=None
        self.rel_w=None
        self.player_name="test"
        self.chips_behind=0
        self.pending_chips_behind=0
        self.seat_id=seat_id
        self.has_focus=False
