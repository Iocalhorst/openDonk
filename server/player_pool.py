import time
class PlayerPool():
    players=[]
    def register_player(player):
        PlayerPool.players.append(player)
    #just a debug/dev thingy
    def quick_start():
        #print("DEBUG : [PlayerPool.quick_start]")
        for player in PlayerPool.players :
            player.quick_start()
            time.sleep(0.05)
        print("DEBUG : [PlayerPool.quick_start] finished! ")
