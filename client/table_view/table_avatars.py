import pyray
import random
from common.player_database import player_database

avatar_path="./assets/avatars/"
overlay_path="./assets/seats/"
overlay_filenames=[
"overlay_fold.png",
"overlay_call.png",
"overlay_raise.png",
"overlay_check.png",
"overlay_seat_open.png",
"overlay_post.png",
]


class AvatarIMG():
    def __init__(self,url):
        img=pyray.load_image(url)
        pyray.image_resize(img, 212,212)

        self.texture = pyray.load_texture_from_image(img)
        pyray.unload_image(img)
        #self.texture=pyray.load_texture_from_image(self.img)
    def get_texture(self):
        assert pyray.is_texture_ready(self.texture),"ERROR : [AvatarPNG] pyray.is_texture_texture_ready(self.texture)==False "
        return self.texture


class OverlayIMG():
    def __init__(self,id,url):
        self.id=id
        img=pyray.load_image(url)
        pyray.image_resize(img, 212,212)

        self.texture = pyray.load_texture_from_image(img)
        pyray.unload_image(img)
        #self.texture=pyray.load_texture_from_image(self.img)
    def get_texture(self):
        assert pyray.is_texture_ready(self.texture),"ERROR : [OverlayPNG] pyray.is_texture_texture_ready(self.texture)==False "
        return self.texture

class TableAvatars():

    def __init__(self):
        self.table_avatars={}
        self.table_avatar_overlays=[]
        for player_id,player_name,player_avatar_filename in player_database :
            self.table_avatars.setdefault(player_id)
            full_path=avatar_path+player_avatar_filename
            print("Loading : ",full_path)
            avatar_img=AvatarIMG(full_path)
            self.table_avatars[player_id]=avatar_img
        for id,f_name in enumerate(overlay_filenames):
            full_path=overlay_path+f_name
            print("Loading : ",full_path)
            overlay_img=OverlayIMG(id,full_path)
            self.table_avatar_overlays.append(overlay_img)

    def get_avatar_by_player_id(self,player_id):
        avatar=self.table_avatars.get(player_id)
        e="player_id '"+str(player_id)+"'"+" not found"
        assert avatar is not None,e
        return avatar

    def get_overlay(self,overlay_name):
        list_names=["overlay_fold","overlay_call","overlay_raise","overlay_check","overlay_seat_open","overlay_post"]
        assert overlay_name in list_names,"overlay nameError"
        for id,name in enumerate(list_names) :
            if name==overlay_name :
                return self.table_avatar_overlays[id]
        raise

    def clean_up(self):
        for a in self.table_avatars :
            if pyray.is_texture_ready(a.tx):
                pyray.unload_texture(a.tx)
        for o_name in list(self.table_avatar_overlays.keys()):
            o=self.table_avatar_overlays[key]
            if pyray.is_texture_ready(o.tx):
                pyray.unload_texture(o.tx)
