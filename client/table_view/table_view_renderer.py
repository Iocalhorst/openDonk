import sys; sys.dont_write_bytecode = True
import os
sys.path.append(os.getcwd() + '/..')
from common.common import *
assert COMMON_IMPORTS,"ERROR : [__main__] missing import"
from common.happy_objects import HappyObject
import pyray
from math import sin,cos

def deg_to_rad(deg):
    return deg*0.0174533

class TableViewRenderer(HappyObject):

    def __init__(self):
        #print("TableWidgetRenderer.__init__(self) : __name__== ",__name__)
        #super().__init__()
        self.player_info_font=None
        self.option_button_font=None
        self.chat_font=None
        self.table_asset_urls=None
        self.chip_set=None
        self.color_theme=None
        self.cards=None
        self.window_width=None
        self.window_height=None

        self.debug_params={
                "show_board_card_overlays"                  :    False,#used
                "show_seat_widget_card_overlays"            :    False,#used
                "show_seat_widget_button_position"          :    False,#used
                "show_seat_widget_chips_inline_position"    :    False,#used
                #"show_overlay_option_widget"                :    False,#unused
                "show_pot_widget_positions"                 :    False,#used
                }

        self.table_shape_params={
                #"table_radius_to_window_height"       :    0.29,      #     t_r=int(h*0.29)
                "horizontal_stretch"                   :    0.275,     #     spread=int(t_r*stretch)
                "table_center_x_to_window_width"       :    0.500,     #     t_cx=w//2
                "table_center_y_to_window_height"      :    0.400,     #     t_cy=int(h*0.475)
                "table_height_to_window_height"        :    0.575,     #     t_h=int(h*0.475)
                "relative_table_border_width"          :    0.015,
                "seat_radius_to_table_radius"          :    0.22
            }


    #def get_table_render_params(self):


    def is_happy(self):
        reason=None
        if not self.player_info_font or self.player_info_font is None :
            reason="player_info_font"
        if not self.option_button_font or self.option_button_font is None :
            reason="option_button_font"
        if not self.table_asset_urls or self.table_asset_urls is None :
            reason="table_asset_urls"
        if not self.chip_set or self.chip_set is None :
            reason="chip_set"
        if not self.color_theme or self.color_theme is None :
            reason="color_theme"
        if not self.cards or self.cards is None :
            reason="cards"
        if not self.window_width or self.window_width is None :
            reason="window_width"
        if not self.window_height or self.window_height is None :
            reason="window_height"
        if not self.chat_font or self.chat_font is None :
            reason="chat font"
        if reason is None:
            return True
        else :
            print("TableRendererNotHappy because : ", reason)
            return False



    def clap_your_hands(self):
        print(__name__," : clap, clap")

    def set_player_info_font(self,player_info_font):
        self.player_info_font=player_info_font
    def set_chat_font(self,chat_font):
        self.chat_font=chat_font
    def set_option_button_font(self,option_button_font):
        self.option_button_font=option_button_font

    def set_window_width(self,window_width):
        self.window_width=window_width

    def set_window_height(self,window_height):
        self.window_height=window_height

    def set_table_asset_urls(self,table_asset_urls):
        self.table_asset_urls=table_asset_urls
        dealer_button_png_path=table_asset_urls.get("table_path")+table_asset_urls.get("dealer_button_filename")
        self.dealer_button_img=pyray.load_image(dealer_button_png_path)
        pyray.image_resize(self.dealer_button_img,55,38)
        self.dealer_button_tex=pyray.load_texture_from_image(self.dealer_button_img)

    def set_chip_set(self,chip_set):
        self.chip_set=chip_set

    def set_color_theme(self,color_theme):
        self.color_theme=color_theme

    def set_cards(self,cards):
        self.cards=cards

    def update_window_dimensions(self,window_width,window_height):
        self.window_width=window_width
        self.window_height=window_height
        if window_width<400 or window_height<300 :
            pyray.set_window_size(400,300)


    def draw_uv_circle(self,x,y,r,c):
        pyray.draw_circle(int(self.window_width*x+0.5),int(self.window_height*y+0.5),int(0.5+r*self.window_height),c)
    def draw_uv_ring(self,x,y,r_o,r_i,c):
        pyray.draw_ring((int(self.window_width*x+0.5),int(self.window_height*y+0.5)),int(0.5+r_i*self.window_height),int(0.5+r_o*self.window_height),0,360,32,c)
        #pyray.draw_ring(center: Vector2, innerRadius: float, outerRadius: float, startAngle: float, endAngle: float, segments: int, color: Color)

    def draw_uv_rect(self,x0,y0,x1,y1,c):
        x=x0*self.window_width
        y=y0*self.window_height
        w=(x1-x0)*self.window_width
        h=(y1-y0)*self.window_height
        pyray.draw_rectangle(int(x+0.5),int(y+0.5),int(w+0.5),int(h+0.5),c)

    def update_seat_widget_params(self,seat_widget):
        rel_circle_x=self.table_shape_params["table_center_x_to_window_width"]
        rel_circle_y=self.table_shape_params["table_center_y_to_window_height"]
        rel_outer_radius=0.5*(self.table_shape_params["table_height_to_window_height"])
        rel_inner_radius=0.5*(self.table_shape_params["table_height_to_window_height"]-self.table_shape_params["relative_table_border_width"])
        rel_offset_x=0.6*rel_outer_radius*self.table_shape_params["horizontal_stretch"]

        seat_widget.rel_x=self.table_shape_params["table_center_x_to_window_width"]
        seat_widget.rel_y=self.table_shape_params["table_center_y_to_window_height"]
        table_radius=0.5*self.table_shape_params["table_height_to_window_height"]
        seat_widget.rel_r=table_radius*self.table_shape_params["seat_radius_to_table_radius"]#185
        #offset=0.5*(self.table_shape_params["table_height_to_window_height"])*0.5*self.table_shape_params["horizontal_stretch"]
        seat_widget.chips_inline_rel_x=seat_widget.rel_x
        seat_widget.chips_inline_rel_y=seat_widget.rel_y
        if seat_widget.seat_id==0 :
            seat_widget.rel_x+=cos(deg_to_rad(110))*table_radius
            seat_widget.rel_y-=sin(deg_to_rad(110))*table_radius
            seat_widget.rel_x-=rel_offset_x#table_radius*0.5*self.table_shape_params["horizontal_stretch"]
            seat_widget.button_rel_x=seat_widget.rel_x
            seat_widget.button_rel_x+=seat_widget.rel_r*1.15
            seat_widget.button_rel_y=seat_widget.rel_y+0.2*seat_widget.rel_r
            seat_widget.chips_inline_rel_x=seat_widget.rel_x+seat_widget.rel_r*1.2#0.7
            seat_widget.chips_inline_rel_y=seat_widget.rel_y+seat_widget.rel_r*1.4
        if seat_widget.seat_id==1 :
            seat_widget.rel_x+=cos(deg_to_rad(180))*table_radius
            seat_widget.rel_y-=sin(deg_to_rad(180))*table_radius
            seat_widget.rel_x-=0.05*rel_offset_x#table_radius*0.5*self.table_shape_params["horizontal_stretch"]
            seat_widget.button_rel_x=seat_widget.rel_x
            seat_widget.button_rel_x+=seat_widget.rel_r*0.55
            seat_widget.button_rel_y=seat_widget.rel_y-seat_widget.rel_r*1.35
            seat_widget.chips_inline_rel_x=seat_widget.rel_x+seat_widget.rel_r*1.5
            seat_widget.chips_inline_rel_y=seat_widget.rel_y+seat_widget.rel_r*0.7
        if seat_widget.seat_id==2 :
            seat_widget.rel_x+=cos(deg_to_rad(250))*table_radius
            seat_widget.rel_y-=sin(deg_to_rad(250))*table_radius+0.15*seat_widget.rel_r
            seat_widget.rel_x-=rel_offset_x#table_radius*0.5*self.table_shape_params["horizontal_stretch"]
            seat_widget.button_rel_x=seat_widget.rel_x
            seat_widget.button_rel_x+=seat_widget.rel_r*1.2
            seat_widget.button_rel_y=seat_widget.rel_y-0.25*seat_widget.rel_r#*1.1
            seat_widget.chips_inline_rel_x=seat_widget.rel_x+seat_widget.rel_r*1.2
            seat_widget.chips_inline_rel_y=seat_widget.rel_y-seat_widget.rel_r*1.6
        if seat_widget.seat_id==3 :
            seat_widget.rel_x+=cos(deg_to_rad(290))*table_radius
            seat_widget.rel_y-=sin(deg_to_rad(290))*table_radius+0.15*seat_widget.rel_r
            seat_widget.rel_x+=rel_offset_x#table_radius*0.5*self.table_shape_params["horizontal_stretch"]
            seat_widget.button_rel_x=seat_widget.rel_x
            seat_widget.button_rel_x-=seat_widget.rel_r*1.2
            seat_widget.button_rel_y=seat_widget.rel_y-0.25*seat_widget.rel_r
            seat_widget.chips_inline_rel_x=seat_widget.rel_x-seat_widget.rel_r*1.2#0.65
            seat_widget.chips_inline_rel_y=seat_widget.rel_y-seat_widget.rel_r*1.6
        if seat_widget.seat_id==4 :
            seat_widget.rel_x+=cos(deg_to_rad(360))*table_radius
            seat_widget.rel_y-=sin(deg_to_rad(360))*table_radius
            seat_widget.rel_x+=0.05*rel_offset_x#table_radius*0.5*self.table_shape_params["horizontal_stretch"]
            seat_widget.button_rel_x=seat_widget.rel_x
            seat_widget.button_rel_x-=seat_widget.rel_r*0.55
            seat_widget.button_rel_y=seat_widget.rel_y+seat_widget.rel_r*1.35
            seat_widget.chips_inline_rel_x=seat_widget.rel_x-seat_widget.rel_r*1.5
            seat_widget.chips_inline_rel_y=seat_widget.rel_y+seat_widget.rel_r*0.7
        if seat_widget.seat_id==5 :
            seat_widget.rel_x+=cos(deg_to_rad(70))*table_radius
            seat_widget.rel_y-=sin(deg_to_rad(70))*table_radius
            seat_widget.rel_x+=rel_offset_x#table_radius*0.5*self.table_shape_params["horizontal_stretch"]
            seat_widget.button_rel_x=seat_widget.rel_x
            seat_widget.button_rel_x-=seat_widget.rel_r*1.15
            seat_widget.button_rel_y=seat_widget.rel_y+0.2*seat_widget.rel_r
            seat_widget.chips_inline_rel_x=seat_widget.rel_x-seat_widget.rel_r*1.2
            seat_widget.chips_inline_rel_y=seat_widget.rel_y+seat_widget.rel_r*1.4

#seat_widget.button_rel_x+=seat_widget.rel_r*1.15
#seat_widget.button_rel_y=seat_widget.rel_y+0.2*seat_widget.rel_r

        table_radius=0.5*(self.table_shape_params["table_height_to_window_height"])
        #seat_card_widget.rel_y-=table_radius*0.26
        card_width=table_radius*0.22
        card_height=card_width*1.7
        card_offset_x=card_width
        if seat_widget.seat_id<3 :
            card_offset_x*=-1
        seat_widget.card_widgets[0].height=card_height
        seat_widget.card_widgets[0].width=card_width
        seat_widget.card_widgets[0].rel_x=seat_widget.rel_x+card_offset_x*1.1
        seat_widget.card_widgets[0].rel_y=seat_widget.rel_y
        seat_widget.card_widgets[1].height=card_height
        seat_widget.card_widgets[1].width=card_width
        seat_widget.card_widgets[1].rel_x=seat_widget.rel_x+card_offset_x*1.85
        seat_widget.card_widgets[1].rel_y=seat_widget.rel_y


    def update_player_info_params(self,player_info_widget):
            rel_circle_x=self.table_shape_params["table_center_x_to_window_width"]
            rel_circle_y=self.table_shape_params["table_center_y_to_window_height"]
            rel_outer_radius=0.5*(self.table_shape_params["table_height_to_window_height"])
            rel_inner_radius=0.5*(self.table_shape_params["table_height_to_window_height"]-self.table_shape_params["relative_table_border_width"])
            rel_offset_x=0.4*rel_outer_radius*self.table_shape_params["horizontal_stretch"]

            player_info_widget.rel_x=self.table_shape_params["table_center_x_to_window_width"]
            player_info_widget.rel_y=self.table_shape_params["table_center_y_to_window_height"]
            table_radius=0.5*self.table_shape_params["table_height_to_window_height"]
            player_info_widget.height=table_radius*0.18#185
            player_info_widget.width=player_info_widget.height*3.5#2.5
                #offset=0.5*(self.table_shape_params["table_height_to_window_height"])*0.5*self.table_shape_params["horizontal_stretch"]
            if player_info_widget.seat_id==0 :
                    player_info_widget.rel_x+=cos(deg_to_rad(110))*table_radius
                    player_info_widget.rel_y-=sin(deg_to_rad(110))*table_radius
                    player_info_widget.rel_x-=rel_offset_x#table_radius*0.5*self.table_shape_params["horizontal_stretch"]
                    player_info_widget.rel_x-=player_info_widget.width*0.5
            if player_info_widget.seat_id==1 :
                    player_info_widget.rel_x+=cos(deg_to_rad(180))*table_radius
                    player_info_widget.rel_y-=sin(deg_to_rad(180))*table_radius
                    player_info_widget.rel_x+=0.5*rel_offset_x#table_radius*0.5*self.table_shape_params["horizontal_stretch"]
                    player_info_widget.rel_x-=player_info_widget.width*0.5
            if player_info_widget.seat_id==2 :
                    player_info_widget.rel_x+=cos(deg_to_rad(250))*table_radius
                    player_info_widget.rel_y-=sin(deg_to_rad(250))*table_radius+0.15*player_info_widget.height
                    player_info_widget.rel_x-=rel_offset_x#table_radius*0.5*self.table_shape_params["horizontal_stretch"]
                    player_info_widget.rel_x-=player_info_widget.width*0.5
            if player_info_widget.seat_id==3 :
                    player_info_widget.rel_x+=cos(deg_to_rad(290))*table_radius
                    player_info_widget.rel_y-=sin(deg_to_rad(290))*table_radius+0.15*player_info_widget.height
                    player_info_widget.rel_x+=rel_offset_x#table_radius*0.5*self.table_shape_params["horizontal_stretch"]
                    player_info_widget.rel_x+=player_info_widget.width*0.5
            if player_info_widget.seat_id==4 :
                    player_info_widget.rel_x+=cos(deg_to_rad(360))*table_radius
                    player_info_widget.rel_y-=sin(deg_to_rad(360))*table_radius
                    player_info_widget.rel_x-=0.5*rel_offset_x#table_radius*0.5*self.table_shape_params["horizontal_stretch"]
                    player_info_widget.rel_x+=player_info_widget.width*0.5
            if player_info_widget.seat_id==5 :
                    player_info_widget.rel_x+=cos(deg_to_rad(70))*table_radius
                    player_info_widget.rel_y-=sin(deg_to_rad(70))*table_radius
                    player_info_widget.rel_x+=rel_offset_x#table_radius*0.5*self.table_shape_params["horizontal_stretch"]f
                    player_info_widget.rel_x+=player_info_widget.width*0.5
            player_info_widget.rel_y+=0.9125*table_radius*self.table_shape_params["seat_radius_to_table_radius"]#185
            player_info_widget.rel_y-=0.5*player_info_widget.height

    def draw_player_info_widget(self,player_info_widget,focus_seat_highlight=False):
        self.update_player_info_params(player_info_widget)

        left_pill_circle_x=player_info_widget.rel_x-0.5*player_info_widget.width
        left_pill_circle_y=player_info_widget.rel_y
        pill_circle_r=0.5*player_info_widget.height
        right_pill_circle_x=player_info_widget.rel_x+0.5*player_info_widget.width
        right_pill_circle_y=player_info_widget.rel_y
        border_col=self.color_theme.get("seat_border")
        seat_col=self.color_theme.get("seat_surface")
        if player_info_widget.has_focus==True :
            #seat_col=pyray.Color(42,69,60,255)
            #border_col=pyray.Color(143+42,139+38,116+32,255)
            seat_col=pyray.Color(42,69,60,255)
            #border_col=pyray.Color(143+42+24,139+38+20,116+32+16,255)
            border_col=pyray.Color(143+42+24,139+38+22,116+32+20,255)


        inner_pill_circle_r=0.5*player_info_widget.height*0.875

        offset_y=pill_circle_r-inner_pill_circle_r

        info_surface_color=self.color_theme.get("seat_surface")

        test_rect=(
            self.window_width*left_pill_circle_x,
            self.window_height*(left_pill_circle_y-0.5*player_info_widget.height),
            self.window_width*player_info_widget.width,
            self.window_height*player_info_widget.height
            )
        pyray.draw_rectangle_rounded(test_rect,1, 32,seat_col)
        pyray.draw_rectangle_rounded_lines(test_rect,1, 32,0.095*self.window_height*player_info_widget.height,border_col)
        #pyray.draw_rectangle_rounded_lines(rec: Rectangle, roundness: float, segments: int, lineThick: float, color: Color)

        max_chars=14
        name=str(player_info_widget.player_name)
        name_str=""
        to_pad=max_chars-len(name)
        pad_l=to_pad//2
        pad_r=max_chars-len(name)-pad_l
        name_str=pad_l*" "+name+pad_r*" "
        cursor_x=(player_info_widget.rel_x-player_info_widget.width*0.5)*self.window_width
        if player_info_widget.seat_id>=3 :
            cursor_x+=(player_info_widget.width*0.35)*self.window_width
        else :
            cursor_x+=(player_info_widget.width*0.1)*self.window_width
        cursor_y=(player_info_widget.rel_y-0.385*player_info_widget.height)*self.window_height#ry+pill_border_w*0.5#666
        char_width=int(self.window_height*player_info_widget.height/5)
        for name_char in name_str :
            pyray.draw_text_ex(self.player_info_font,str(name_char),(cursor_x,cursor_y),(char_width*2.15),0,self.color_theme.get("player_info"))
            cursor_x+=char_width
        chips_behind_str="$"+str(player_info_widget.chips_behind)
        cursor_x=(player_info_widget.rel_x)*self.window_width-int(char_width*len(chips_behind_str))
        if player_info_widget.seat_id>=3 :
            cursor_x+=(player_info_widget.width*0.2)*self.window_width
        else :
            cursor_x-=(player_info_widget.width*0.025)*self.window_width
        cursor_y=(player_info_widget.rel_y)*self.window_height+0.185*char_width#ry+pill_border_w*0.5#666
        for chips_behind_char in chips_behind_str :
            pyray.draw_text_ex(self.player_info_font,str(chips_behind_char),(cursor_x,cursor_y),(char_width*2.15),0,self.color_theme.get("player_info"))
            cursor_x+=char_width



    def draw_seat_widget_cards(self,seat_widget):

        if self.debug_params["show_seat_widget_card_overlays"]==True :
            self.draw_uv_rect(
                seat_widget.card_widgets[0].rel_x-0.5*seat_widget.card_widgets[0].width,
                seat_widget.card_widgets[0].rel_y-0.5*seat_widget.card_widgets[0].height,
                seat_widget.card_widgets[0].rel_x+0.5*seat_widget.card_widgets[0].width,
                seat_widget.card_widgets[0].rel_y+0.5*seat_widget.card_widgets[0].height,
                pyray.Color(128,255,128,8)
            )
            self.draw_uv_rect(
                seat_widget.card_widgets[1].rel_x-0.5*seat_widget.card_widgets[1].width,
                seat_widget.card_widgets[1].rel_y-0.5*seat_widget.card_widgets[1].height,
                seat_widget.card_widgets[1].rel_x+0.5*seat_widget.card_widgets[1].width,
                seat_widget.card_widgets[1].rel_y+0.5*seat_widget.card_widgets[1].height,
                pyray.Color(128,255,128,8)
            )
        if seat_widget.seat_id<3 :
            self.draw_card_widget(seat_widget.card_widgets[1])
            self.draw_card_widget(seat_widget.card_widgets[0])
        else :
            self.draw_card_widget(seat_widget.card_widgets[0])
            self.draw_card_widget(seat_widget.card_widgets[1])

    def draw_seat_widget(self,seat_widget):
        seat_col=self.color_theme.get("seat_surface")
        border_col=self.color_theme.get("seat_border")
        if seat_widget.has_focus==True :
            seat_col=pyray.Color(42,69,60,255)
            #border_col=pyray.Color(143+42+16,139+38+14,116+32+12,255)
            border_col=pyray.Color(143+42+24,139+38+22,116+32+20,255)

        self.draw_uv_circle(seat_widget.rel_x,seat_widget.rel_y,seat_widget.rel_r,border_col)


        self.draw_uv_circle(seat_widget.rel_x,seat_widget.rel_y,seat_widget.rel_r*0.9,seat_col)#0.925

        if self.debug_params["show_seat_widget_button_position"]==True :
            self.draw_uv_circle(seat_widget.button_rel_x,seat_widget.button_rel_y,seat_widget.rel_r*0.4,pyray.Color(255,255,255,8))
        if self.debug_params["show_seat_widget_chips_inline_position"]==True :
            self.draw_uv_circle(seat_widget.chips_inline_rel_x,seat_widget.chips_inline_rel_y,seat_widget.rel_r*0.4,pyray.Color(255,255,255,8))

        avatar=seat_widget.get_avatar()

        tex=avatar.get_texture()
        pos_x=seat_widget.rel_x*self.window_width
        pos_y=seat_widget.rel_y*self.window_height
        scale=1.45*seat_widget.rel_r*self.window_width/tex.width#1#self.window_width/tex.width
        offset_x=(tex.width*scale*0.5)
        offset_y=(tex.height*scale*0.5)

        pyray.draw_texture_ex(tex,(pos_x-offset_x,pos_y-offset_y),0,scale,(255,255,255,245))

        self.draw_uv_ring(seat_widget.rel_x,seat_widget.rel_y,seat_widget.rel_r,seat_widget.rel_r*0.9,border_col)




        if seat_widget.show_dealer_button==True :
            dealer_button_texture=self.dealer_button_tex
            pos_x=seat_widget.button_rel_x*self.window_width
            pos_y=seat_widget.button_rel_y*self.window_height
            scale=2.15*seat_widget.rel_r*self.window_width/tex.width#1#self.window_width/tex.width
            offset_x=2.15*seat_widget.rel_r*(tex.width*scale)*-1
            offset_y=2.15*seat_widget.rel_r*(tex.height*scale)
            #dealer_button_x=seat_widgetseats[self.dealer_button_seat_id].dealer_button_x-scale*(dealer_button_texture.width//2)
            #dealer_button_y=self.seats[self.dealer_button_seat_id].dealer_button_y-scale*(dealer_button_texture.height//2)
            pyray.draw_texture_ex(dealer_button_texture,(pos_x+offset_x,pos_y-offset_y+1),0,scale,(255,255,255,255))
            pyray.draw_texture_ex(dealer_button_texture,(pos_x+offset_x,pos_y-offset_y),0,scale,(255,255,255,255))

    def update_pot_widget_params(self,pot_widget):
        pot_widget.rel_x=self.table_shape_params["table_center_x_to_window_width"]
        pot_widget.rel_y=self.table_shape_params["table_center_y_to_window_height"]
        table_radius=0.5*(self.table_shape_params["table_height_to_window_height"])

        if pot_widget.pot_id==0 :
            pot_widget.rel_x+=0
            pot_widget.rel_y+=0.1175*table_radius#0.1*table_radius
        elif pot_widget.pot_id==1 :
            pot_widget.rel_x-=0.385*table_radius
            pot_widget.rel_y+=0.205*table_radius
        elif pot_widget.pot_id==2 :
            pot_widget.rel_x+=0.385*table_radius
            pot_widget.rel_y+=0.205*table_radius
        elif pot_widget.pot_id==3 :
            pot_widget.rel_x-=0.21*table_radius
            pot_widget.rel_y+=0.415*table_radius
        elif pot_widget.pot_id==4 :
            pot_widget.rel_x+=0.21*table_radius
            pot_widget.rel_y+=0.415*table_radius
        else :
            print("pot_widget id : ",pot_widget.pot_id)
            assert False,"pot_widget.pot_id invalid"

        #pot_widget.rel_y-=0.075*table_radius

    def draw_card_widget(self,card_widget):
        card_id=card_widget.card_id
        if card_id==-1 :
            return
        card=self.cards[card_id]
        tex=card.get_texture()
        pos_x=card_widget.rel_x*self.window_width
        pos_y=card_widget.rel_y*self.window_height
        scale=card_widget.width*self.window_width/tex.width#1#self.window_width/tex.width
        offset_x=(tex.width*scale*0.5)
        offset_y=(tex.height*scale*0.5)

        pyray.draw_texture_ex(tex,(pos_x-offset_x,pos_y-offset_y),0,scale,(255,252,245,255))



    def draw_chip_stack(self,rel_x,rel_y,chip_count,sort_by_value=False,show_value_as_text=True):
        if chip_count==0 :
            return
        chip_stack=self.chip_set.get_chips(chip_count)
        if show_value_as_text==True :
            stack_x=rel_x*self.window_width
            stack_y=rel_y*self.window_height
            value_text="$"+str(chip_count)
            char_height=self.window_height//50#
            text_offset_y=int(char_height)
            if sort_by_value==True :
                text_offset_y=int(char_height*1.35)
            pyray.draw_text_ex(self.player_info_font,value_text,(int(stack_x-(0.65*char_height)),int(stack_y+text_offset_y)),int(char_height),0,self.color_theme.get("player_info"))
        if sort_by_value==True :
            num_stack_types=0
            for color,value,count in chip_stack :
                if count>0:
                    num_stack_types+=1
            stack_type_index=0
            for color,value,count in chip_stack :
                if count>0 :
                    tex=self.chip_set.get_texture(color)
                    stack_type_index+=1
                    for stack_height_index in range(count) :
                        stack_x=rel_x*self.window_width
                        stack_y=rel_y*self.window_height
                        scale=self.window_width/(tex.height*65)#1#self.window_width/tex.width
                        offset_x=(tex.width*scale*0.5)*(num_stack_types)-(tex.width*scale)*(stack_type_index-1)#+2*index*tex.width*scale)*0.5
                        offset_y=(-0.25*tex.height*scale)*(0.5+stack_height_index)
                        pyray.draw_texture_ex(tex,(stack_x-offset_x,stack_y+offset_y+1),0,scale,(255,255,255,255))
                        pyray.draw_texture_ex(tex,(stack_x-offset_x,stack_y+offset_y),0,scale,(255,255,255,255))
        else :
            chip_index=0
            for color,value,count in chip_stack :
                if count>0 :
                    tex=self.chip_set.get_texture(color)
                    for stack_height_index in range(count) :
                        chip_index+=1
                        stack_x=rel_x*self.window_width
                        stack_y=rel_y*self.window_height
                        scale=self.window_width/(tex.height*65)#1#self.window_width/tex.width
                        offset_x=tex.width*scale*0.5#+2*index*tex.width*scale)*0.5
                        offset_y=(-0.25*tex.height*scale)*(0.5+chip_index)
                        pyray.draw_texture_ex(tex,(stack_x-offset_x,stack_y+offset_y+1),0,scale,(255,255,255,255))
                        pyray.draw_texture_ex(tex,(stack_x-offset_x,stack_y+offset_y),0,scale,(255,255,255,255))

    def draw_pot_widget(self,pot_widget):
        self.update_pot_widget_params(pot_widget)
        if self.debug_params["show_pot_widget_positions"]==True :
            self.draw_uv_circle(pot_widget.rel_x,pot_widget.rel_y,0.02,pyray.Color(255,255,255,8))
        rel_x,rel_y,value=pot_widget.get_render_params()
        self.draw_chip_stack(rel_x,rel_y,value,sort_by_value=True)
    def draw_table_shape(self):

        pyray.draw_rectangle(0,0,self.window_width,self.window_height,self.color_theme.get("table_background"))

        rel_circle_x=self.table_shape_params["table_center_x_to_window_width"]
        rel_circle_y=self.table_shape_params["table_center_y_to_window_height"]
        rel_outer_radius=0.5*(self.table_shape_params["table_height_to_window_height"])
        rel_inner_radius=0.5*(self.table_shape_params["table_height_to_window_height"]-self.table_shape_params["relative_table_border_width"])
        rel_offset_x=rel_outer_radius*self.table_shape_params["horizontal_stretch"]

        self.draw_uv_circle(rel_circle_x-rel_offset_x,rel_circle_y,rel_outer_radius,self.color_theme.get("table_border"))
        self.draw_uv_circle(rel_circle_x+rel_offset_x,rel_circle_y,rel_outer_radius,self.color_theme.get("table_border"))

        #one to the left,one to the right, one to the middle to cover the junk
        self.draw_uv_circle(rel_circle_x-rel_offset_x,rel_circle_y,rel_inner_radius,self.color_theme.get("table_surface"))
        self.draw_uv_circle(rel_circle_x+rel_offset_x,rel_circle_y,rel_inner_radius,self.color_theme.get("table_surface"))
        self.draw_uv_circle(rel_circle_x,rel_circle_y,rel_inner_radius, self.color_theme.get("table_surface"))

        self.draw_uv_rect(
            rel_circle_x-rel_offset_x,
            rel_circle_y-rel_outer_radius,
            rel_circle_x+rel_offset_x,
            rel_circle_y+rel_outer_radius,
            self.color_theme.get("table_border")
            )
        self.draw_uv_rect(
            rel_circle_x-rel_offset_x,
            rel_circle_y-rel_inner_radius,
            rel_circle_x+rel_offset_x,
            rel_circle_y+rel_inner_radius,
            self.color_theme.get("table_surface")
            )

    def update_board_card_widget_params(self,board_card_widget):
        board_card_widget.rel_x=self.table_shape_params["table_center_x_to_window_width"]
        board_card_widget.rel_y=self.table_shape_params["table_center_y_to_window_height"]
        table_radius=0.5*(self.table_shape_params["table_height_to_window_height"])
        board_card_widget.rel_y-=table_radius*0.27#65#35#25
        board_card_widget.width=table_radius*0.24#315
        board_card_widget.height=board_card_widget.width*1.7
        if board_card_widget.id==0 :
            board_card_widget.rel_x-=2*table_radius*0.26#575
        elif board_card_widget.id==1 :
            board_card_widget.rel_x-=1*table_radius*0.26#575
        elif board_card_widget.id==2 :
            board_card_widget.rel_x+=0.0#4*table_radius
        elif board_card_widget.id==3 :
            board_card_widget.rel_x+=1*table_radius*0.26#575
        elif board_card_widget.id==4 :
            board_card_widget.rel_x+=2*table_radius*0.26#575
        else :
            print("board_card_widget id : ",board_card_widget.id)
            assert False,"board_card_widget.id invalid"


    def draw_board_card_widget(self,board_card_widget):
        self.update_board_card_widget_params(board_card_widget)
        if self.debug_params["show_board_card_overlays"]==True :
            self.draw_uv_rect(
                board_card_widget.rel_x-board_card_widget.width*0.5,
                board_card_widget.rel_y-board_card_widget.height*0.5,
                board_card_widget.rel_x+board_card_widget.width*0.5,
                board_card_widget.rel_y+board_card_widget.height*0.5,
                pyray.Color(128,255,128,8)
            )
        self.draw_card_widget(board_card_widget)
