from table_view.button_widget import ButtonWidget

class OptionWidget():
    def __init__(self,option_font):
        self.buttons=[ButtonWidget("Fold"),ButtonWidget("Call"),ButtonWidget("Raise")]
        self.x=0.5
        self.y=0.79
        self.w=1-self.x*1.1#0.51625
        self.h=0.1375
        self.font=option_font

    def draw(self,w,h,color_theme):
        o_col_b=color_theme.get("button_border")
        o_col_s=color_theme.get("button_surface")
        o_w=int(w*self.w)
        o_h=int(h*self.h)
        o_x=int(w*self.x)
        o_y=int(h*self.y)
        #debug_param=debug_params.get("debug_show_overlay_option_widget")
        #assert debug_param is not None,"debug_param nameError"
        #if debug_param==True :
        #    pyray.draw_rectangle(o_x,o_y,o_w+int(0.5*self.buttons[0].border_w*o_h),o_h+int(0.5*self.buttons[0].border_w*o_h),color_theme.get("button_border"))
        for index,button in enumerate(self.buttons) :
            button_w=o_w//len(self.buttons)
            button_h=o_h
            button_x=o_x+(button_w*index)
            button_y=o_y
            b_rect_x=int(button_x+(0.5*button_w*button.border_w))
            b_rect_y=int(button_y+(0.5*button_w*button.border_w))
            b_rect_h=int(button_h-0.5*(button_w*button.border_w))
            b_rect_w=int(button_w-(0.5*button_w*button.border_w))

#            if debug_params.get("enable_debug") :
#                pyray.draw_rectangle(b_rect_x,b_rect_y,b_rect_w,b_rect_h,color_theme.get("button_surface"))
#            #rounded corners
            c_o_r=button_h*button.corner_r
            c1_o_x=b_rect_x+c_o_r
            c1_o_y=b_rect_y+c_o_r
            c2_o_x=b_rect_x+b_rect_w-c_o_r
            c2_o_y=b_rect_y+c_o_r
            c3_o_x=b_rect_x+b_rect_w-c_o_r
            c3_o_y=b_rect_y+b_rect_h-c_o_r
            c4_o_x=b_rect_x+c_o_r
            c4_o_y=b_rect_y+b_rect_h-c_o_r
            corners_o=[(c1_o_x,c1_o_y),(c2_o_x,c2_o_y),(c3_o_x,c3_o_y),(c4_o_x,c4_o_y)]
            col_tmp1=pyray.Color(102,109,80,255)
            col_tmp2=pyray.Color(63,64,42,255)
            col_tmp3=pyray.Color(83,42,122,132)
            for x,y in corners_o :
                pyray.draw_circle(int(x),int(y),int(c_o_r),color_theme.get("button_border"))#col_tmp1)
            rect1_o_x=int(c1_o_x)
            rect1_o_y=int(c1_o_y-c_o_r)
            rect1_o_w=int(button_w-2*c_o_r-0.5*button_w*button.border_w)
            rect1_o_h=int(button_h-0.5*button_w*button.border_w)
            rect2_o_x=int(c1_o_x-c_o_r)
            rect2_o_y=int(c1_o_y)
            rect2_o_w=int(button_w-0.5*button_w*button.border_w)
            rect2_o_h=int(button_h-2*c_o_r-0.5*button_w*button.border_w)

            pyray.draw_rectangle(rect1_o_x,rect1_o_y,rect1_o_w,rect1_o_h,color_theme.get("button_border"))
            pyray.draw_rectangle(rect2_o_x,rect2_o_y,rect2_o_w,rect2_o_h,color_theme.get("button_border"))


            c_i_r=int(c_o_r*(1-(0.5*button.border_w)))
            margin=int(c_i_r*(0.215*button.border_w))
            c1_i_x=int(c1_o_x+margin)
            c1_i_y=int(c1_o_y+margin)
            c2_i_x=int(c2_o_x-margin)
            c2_i_y=int(c2_o_y+margin)
            c3_i_x=int(c3_o_x-margin)
            c3_i_y=int(c3_o_y-margin)
            c4_i_x=int(c4_o_x+margin)
            c4_i_y=int(c4_o_y-margin)
            corners_i=[(c1_i_x,c1_i_y),(c2_i_x,c2_i_y),(c3_i_x,c3_i_y),(c4_i_x,c4_i_y)]

            for x,y in corners_i :
                pyray.draw_circle(int(x),int(y),int(c_i_r),color_theme.get("button_surface"))
            rect1_i_x=c1_i_x
            rect1_i_y=c1_i_y-c_i_r
            rect1_i_w=c2_i_x-c1_i_x
            rect1_i_h=c3_i_y-c1_i_y+c_i_r*2
            rect2_i_x=c1_i_x-c_i_r
            rect2_i_y=c1_i_y
            rect2_i_w=c2_i_x-c1_i_x+c_i_r*2
            rect2_i_h=c3_i_y-c2_i_y

            pyray.draw_rectangle(rect1_i_x,rect1_i_y,rect1_i_w,rect1_i_h,color_theme.get("button_surface"))
            pyray.draw_rectangle(rect2_i_x,rect2_i_y,rect2_i_w,rect2_i_h,color_theme.get("button_surface"))
            #pyray.draw_text_ex(self.player_info_font,str(name_char),(cursor_x,cursor_y),(char_width*2),0,color_theme.get("player_info"))
            char_w=rect2_i_w//11.5
            char_h=int(char_w*1.85)
            for idx,c in enumerate(button.s) :
                offset_x=int(rect2_i_x+int(rect2_i_w*0.5)-(0.5*char_w*len(button.s))+(idx*char_w))+1.5*margin
                offset_y=int(rect2_i_y+int(rect2_i_h*0.5)-(0.5*char_h))+margin
                #if debug_params.get("enable_debug") :
                #    if idx%2 == 0 :
                #        pyray.draw_rectangle(offset_x,offset_y,char_w,char_h,(100,200,50,64))
                #    else :
                pyray.draw_rectangle(offset_x,offset_y,char_w,char_h,(250,200,100,32))
                pyray.draw_text_ex(self.font,str(c),(offset_x,offset_y),char_h,0,(224,212,192,255))

            #
            #rect1_x=int(c1_x)
            #rect1_y=int(c1_y-c_r)
            #rect1_w=int(button_w-2*c_r-0.5*button_w*button.border_w)
            #rect1_h=int(button_h-0.5*button_w*button.border_w)
            #rect2_x=int(c1_x-c_r)
            #rect2_y=int(c1_y)
            #rect2_w=int(button_w-0.5*button_w*button.border_w)
            #rect2_h=int(button_h-2*c_r-0.5*button_w*button.border_w)

            #pyray.draw_rectangle(rect1_i_x,rect1_i_y,rect1_i_w,rect1_i_h,col_tmp4)
            #pyray.draw_rectangle(rect2_i_x,rect2_i_y,rect2_i_w,rect2_i_h,col_tmp4)
