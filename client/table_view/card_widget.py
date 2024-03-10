import pyray
import random
values=["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
suites=["c","s","h","d"]

card_img_filenames=[
"2_of_clubs.png",
"2_of_spades.png",
"2_of_hearts.png",
#"2d_v5_a.png",
"2_of_diamonds.png",
"3_of_clubs.png",
"3_of_spades.png",
"3_of_hearts.png",
#"3d_v5_a.png",
"3_of_diamonds.png",
"4_of_clubs.png",
"4_of_spades.png",
"4_of_hearts.png",
#"4d_v5_a.png",
"4_of_diamonds.png",
"5_of_clubs.png",
"5_of_spades.png",
"5_of_hearts.png",
"5_of_diamonds.png",
#"5d_v5_a.png",
"6_of_clubs.png",
"6_of_spades.png",
"6_of_hearts.png",
"6_of_diamonds.png",
#"6d_v5_a.png",
"7_of_clubs.png",
"7_of_spades.png",
"7_of_hearts.png",
"7_of_diamonds.png",
#"7d_v5_a.png",
"8_of_clubs.png",
"8_of_spades.png",
"8_of_hearts.png",
"8_of_diamonds.png",
#"8d_v5_a.png",
"9_of_clubs.png",
"9_of_spades.png",
"9_of_hearts.png",
"9_of_diamonds.png",
#"9d_v5_a.png",
"10_of_clubs.png",
"10_of_spades.png",
"10_of_hearts.png",
"10_of_diamonds.png",
#"10d_v5_a.png",
"jack_of_clubs2.png",
"jack_of_spades2.png",
"jack_of_hearts2.png",
"jack_of_diamonds2.png",
"queen_of_clubs2.png",
"queen_of_spades2.png",
"queen_of_hearts2.png",
"queen_of_diamonds2.png",
"king_of_clubs2.png",
"king_of_spades2.png",
"king_of_hearts2.png",
"king_of_diamonds2.png",
"ace_of_clubs.png",
"ace_of_spades.png",
"ace_of_hearts.png",
"ace_of_diamonds.png"
]

class CardIMG():
    def __init__(self,url):
        self.id=id
        img=pyray.load_image(url)
        #pyray.image_resize(img, int(img.width*0.9),int(img.height*0.85))
        card_aspect_ratio=(9/5.5)
        #pyray.image_resize(img, int(img.height),int(img.width*card_aspect_ratio))
        pyray.image_resize(img, 224*2,2*308)

        self.texture = pyray.load_texture_from_image(img)
        #pyray.gen_texture_mipmaps(self.texture)
        #pyray.set_texture_filter(self.texture, 2)
        pyray.unload_image(img)
        #self.texture=pyray.load_texture_from_image(self.img)
    def get_texture(self):
        assert pyray.is_texture_ready(self.texture),"ERROR : [CardPNG] pyray.is_texture_texture_ready(self.texture)==False "

        return self.texture
#
#class Deck52():
#    cards=[]
#    def __init__(self):
#            full_path=cards_img_path+img_filename
#            #print("Loading : ",full_path)
#            card_png=CardPNG(id,full_path)
#            self.cards.append(card_png)
#        #for v in values:
#        #    for s in suites:
#        #        i+=1
#        #        c=CardPNG(i,v,s)
#        #        #l0g(c)
#        #        self.stack.append(c)
#
#    def get_card(self,id):
#        return self.cards[id]
#
#    def clean_up(self):
#        for card in self.cards :
#            if pyray.is_texture_ready(card.tx):
#                pyray.unload_texture(card.tx)
#
#
#
class CardWidget():
    def __init__(self,id):
        self.id=id
        self.rel_x=0.1
        self.rel_y=0.1
        self.card_id=-1
