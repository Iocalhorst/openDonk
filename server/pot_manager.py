class PotManager():
    def __init__(self):
          self.seats_with_cards=[]
          self.seats_with_chips_inline=[]

    def read_seats(self,seats):
        for seat in seats :
            if seat.has_cards() :
                self.seats_with_cards.append(seat)
            if seat.has_chips_inline() :
                self.seats_with_chips_inline.append(seat)
    def verify_state(self):
        e="len(seats_with_cards)<=0', should be unreachble, cause of pot_managment not_required "
        assert len(self.seats_with_cards)>0,e
        e="len(seats_with_chips_inline)==0' should be unreachable cause of pot_managment not_required"
        assert len(self.seats_with_chips_inline)>0,e
    def get_required_action_name(self):
        if len(self.seats_with_chips_inline)>1 :
            return "pot_collect"
        elif len(self.seats_with_cards)==1 :
            return "inline_return"
        else :
            assert False,"failiure, unreachable"
    def get_transaction_list(self):
        smallest_inline_live_amount=99999999999
        transaction_list=[]
        for seat in self.seats_with_cards :
            if seat.chips_inline>0 and seat.chips_inline<smallest_inline_live_amount:
                smallest_inline_live_amount=seat.chips_inline

        limit=smallest_inline_live_amount

        for seat in self.seats_with_chips_inline:
            if seat in self.seats_with_cards:
                transaction={
                    "is_live":True,
                    "seat_id":seat.seat_id,
                    "amount":limit
                }
                transaction_list.append(transaction)
            elif seat.chips_inline>=limit :
                transaction={
                    "is_live":False,
                    "seat_id":seat.seat_id,
                    "amount":limit
                    }
                transactions_list.append(transaction)
            elif seat.chips_inline<limit :
                transaction={
                    "is_live":False,
                    "seat_id":seat.seat_id,
                    "amount":seat.chips_inline
                }
                transaction_list.append(transaction)
            else :
                assert False,"Failure, Unreachable"
        return transaction_list
