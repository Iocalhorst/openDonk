import pyray
from table_view.color_theme_debug_params import color_theme_debug_params as debug_params

class ColorTheme():
    def __init__(self,theme_dict):
        self.theme_dict=theme_dict
        self.debug_transparency_flag=debug_params.get("enable_debug_transparency")
        assert self.debug_transparency_flag is not None,"debug_param nameError in ColorTheme()"
    def get(self,color_name,debug_param=False):
        col_dict=self.theme_dict.get(color_name)
        r=col_dict.get("r")
        g=col_dict.get("g")
        b=col_dict.get("b")
        a=col_dict.get("a")
        #debug_param=debug_params.get("debug_enable_global_color_theme_transparancy")
        #assert debug_param is not None,"debug_param nameError"
        if self.debug_transparency_flag==True:
            a=int(a*0.5)
            #if color_name in debug_params.get("transparency_coeffs") :
            #    param_value=debug_params["transparency_coeffs"].get(color_name)
            #    assert (param_value>=0 and param_value<=1), "Error : [Color_Theme.get] paramOutOfBounds, 0>=debug_param<=1 "
            #    if param_value==1 :
            #        a=a
            #    elif param_value==0 :
            #        a=0
            #    else :
            #        a_mod=a*(param_value)
            #        a=int(a_mod)
        return pyray.Color(r,g,b,a)
