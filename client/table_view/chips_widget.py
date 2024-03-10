import pyray
import random

class ChipIMG():
    def __init__(self,img,value,color):
        self.img=img
        self.value=value
        self.color=color
        pyray.image_resize(self.img,38,30)
        self.texture=pyray.load_texture_from_image(self.img)

    def __repr__(self):
        data=(self.value,self.color)
        s=str(data)
        return s
    def get_texture(self):
        return self.texture#self.texture

class ChipSet():
    def __init__(self,chips_path):
        self.value_colors={
            500 : "lightgreen",
            100 :     "magenta",
             50 :       "green",
             25 :        "blue",
             10 :      "purple",
              5 :         "red",
              1 :       "orange"

            }
        self.color_values={
            "lightgreen" :500,
            "magenta"     :100,
            "green"       : 50,
            "blue"        : 25,
            "purple"      : 10,
            "red"         :  5,
            "orange"      :  1,
            }
        self.color_imgs={
            "orange"     :0,
            "red"        :0,
            "purple"     :0,
            "blue"       :0,
            "green"      :0,
            "magenta"    :0,
            "lightgreen":0
            }
        self.chips={
            "orange"     :0,
            "red"        :0,
            "purple"     :0,
            "blue"       :0,
            "green"      :0,
            "magenta"    :0,
            "lightgreen":0
            }
        for color_value in self.color_values:
            full_path=chips_path+"chip_"+color_value+".png"
            #print(chip_path)
            img=pyray.load_image(full_path)
            self.color_imgs[color_value]=img
            chip=ChipIMG(img,color_value,self.color_values[color_value])
            self.chips[color_value]=chip
            #self.color_chips[color_value]=ChipPNG(color_value,self.color_values[color_value])
    def get_texture(self,color):
        chip=self.chips[color]
        tex=chip.get_texture()
        return tex
    def get_chips(self,value):
        chips=[]
        rest=value
        for value_color in self.value_colors :
            div_result=rest//value_color
            color=self.value_colors[value_color]
            packed=(color,value_color,div_result)
            chips.append(packed)
            rest%=value_color
        return chips
