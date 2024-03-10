import pyray
from common.happy_objects import *
#from debug_params import debug_params
from common.debug_department import DONK_WARNING,DONK_DEBUG,DONK_ERROR
from user_event_factory import UserEventFactory #used to wrap "doubleclick, open selected poker_table_view" for ipc-message forwarding
#some naming/wording issues need to be adressed
#
#   table as in database.table, not pokertable
#   col means column as in database.table.column
#   color means color and is always spelled verbose
#
#   i may decide to prefix/suffix identifiers if confusion happens and/or i have a concept/scheme
class TablePoolViewRenderer(HappyObject):
    def __init__(self):
        self.table_pool_font=None
        #table as in database.show(tables), not poker tables
        self.table_params={
            "offset_x":50,
            "offset_y":100,
            "row_width":500,
            "row_height":20,
            "num_rows":16, #1 title,15 datasets,
            "num_cols":5
            }
        self.col_params={
                0:{
                 "title":"table_id",
                 "key":"table_id",
                 "width":75
                 },
                1:{
                 "title":"table_name",
                 "key":"table_name",
                 "width":180
                 },
                2:{
                 "title":"game",
                 "key":"game_type",
                 "width":70
                 },
                3:{
                 "title":"seats",
                 "key":"num_seats",
                 "width":70
                 },
                4:{
                 "title":"stakes",
                 "key":"stakes",
                 "width":105
                 },
            }
        #self.table_background_color=pyray.Color(192,172,172,42)
        self.table_background_color=pyray.Color(69,100,42,96)
        #self.table_outline_color=pyray.Color(128,112,112,255)
        self.table_outline_color=pyray.Color(28,99,12,172)

        list_col_indizes=list(self.col_params.keys())
        assert self.table_params["num_cols"]==len(list_col_indizes),"table_params['num_cols'] doesnt match the number of specified col_params"
        sum_col_width=0
        #print("DEBUG : [table_pool_view_renderer.__init__] list_col_indizes : ",list_col_indizes)
        for col_index in list_col_indizes :
            col_params=self.col_params[col_index]
            sum_col_width+=col_params["width"]
        assert sum_col_width==self.table_params["row_width"],"width of columns doent add up to row width"
        self.rows={}
        self.selected_row=-1
        self.user_events=[]

    def has_user_events(self):
        if len(self.user_events)>0 :
            return True
        else :
            return False
    def pop_user_event(self):
        user_event=self.user_events.pop(0)
        return user_event
    def set_table_pool_font(self,table_pool_font):
        assert table_pool_font is not None,"font arg is None"
        self.table_pool_font=table_pool_font

    def is_happy(self):
        reason=None
        if not self.table_pool_font or self.table_pool_font is None :
            reason="table_pool_font"
        if reason is None:
            return True
        else :
            print("TableRendererNotHappy because : ", reason)
            return False

    def clap_your_hands(self):
        print(__name__," : clap, clap")

    def slurp(self,table_datasets):
        self.rows.clear()
        for index,dataset in enumerate(table_datasets):
            self.rows[index+1]=dataset
            #print("DEBUG : [dataset] ",dataset)
        if len(table_datasets)==0 :
            return

        #print("DEBUG : table_datasets = ",table_datasets)
    def get_row_data_by_row_index(self,row_index):
        row_indizes=list(self.rows.keys())
        dummy_row_data={"table_id":"","table_name":"","game_type":"","num_seats":"","stakes":""}
        if row_index in row_indizes :
            row_data=self.rows.get(row_index)
            return row_data
        else :
            return dummy_row_data
        #for row_index in row_indizes :
        #    row_data=self.rows.get(row_index)
        #    print("DEBUG : row index ",row_index,", row_data : ",row_data)
        #assert False
    def is_mouse_over_table(self):
        mouse_pos=pyray.get_mouse_position()
        table_height=self.table_params.get("row_height")*self.table_params.get("num_rows")
        table_width=self.table_params.get("row_width")
        area_x=self.table_params.get("offset_x")
        area_y=self.table_params.get("offset_y")+self.table_params.get("row_height")
        area_height=table_height-self.table_params.get("row_height")
        area_width=table_width
        if mouse_pos.x>area_x and mouse_pos.x<area_x+area_width and mouse_pos.y>area_y and mouse_pos.y<area_y+area_height :
            return True
        else :
            return False
    def get_row_where_mouse_is_over(self):
        assert self.is_mouse_over_table()==True,"dont call get_row_where_mouse_is_over() without checking if is_mouse_over_table()"
        mouse_pos=pyray.get_mouse_position()
        area_x=self.table_params.get("offset_x")
        area_y=self.table_params.get("offset_y")
        area_width=self.table_params.get("row_width")
        area_height=self.table_params.get("row_height")
        row_index=0
        while row_index<self.table_params.get("num_rows"):
            if mouse_pos.x>area_x and mouse_pos.x<area_x+area_width and mouse_pos.y>=area_y and mouse_pos.y<area_y+area_height :
                return row_index
            else :
                area_y+=self.table_params.get("row_height")
                row_index+=1

    def draw_table(self):
        table_x=self.table_params.get("offset_x")
        table_y=self.table_params.get("offset_y")
        table_width=self.table_params.get("row_width")
        table_height=self.table_params.get("row_height")*self.table_params.get("num_rows")
        pyray.draw_rectangle(table_x,table_y,table_width,table_height,self.table_background_color)
        pyray.draw_rectangle_lines(table_x,table_y,table_width,table_height,self.table_outline_color)
        pyray.draw_rectangle_lines(table_x-1,table_y-1,table_width+2,table_height+2,self.table_outline_color)


#        title_row={self.col_params[0].title,self.col_params[1].title,self.col_params[2].title,self.col_params[3].title,self.col_params[4].title)
        mouse_row=-1
        if self.is_mouse_over_table()==True :
            mouse_row=self.get_row_where_mouse_is_over()
            if pyray.is_mouse_button_pressed(pyray.MOUSE_BUTTON_LEFT) :
                if mouse_row==self.selected_row :
                    details=self.get_row_data_by_row_index(mouse_row)
                    user_event=UserEventFactory.create_user_event("REQUEST_TABLE_VIEW",details)
                    self.user_events.append(user_event)
                    #debug_param=debug_params.get("debug_table_pool_view_renderer_add_user_event")
                    #assert debug_param is not None,"debug_param nameError"
                    #if debug_param==True :
                    #    print("DEBUG : [table_pool_view_renderer] added user_event : ",str(user_event))
                else :
                    self.selected_row=mouse_row
        for row_index in range(self.table_params.get("num_rows")) :
            row_x=table_x
            row_y=table_y+row_index*self.table_params.get("row_height")
            if mouse_row==row_index :
                pyray.draw_rectangle(row_x,row_y,table_width,self.table_params.get("row_height"),pyray.Color(69+24,69+32,12+69,69+42))
            if row_index==self.selected_row :
                pyray.draw_rectangle(row_x,row_y,table_width,self.table_params.get("row_height"),pyray.Color(69*2+24,69*2+32,12+69*2,2*(69+42)))

            pyray.draw_rectangle_lines(row_x,row_y,table_width,self.table_params.get("row_height"),self.table_outline_color)

            cursor_x=row_x
            cursor_y=row_y
            row_data=self.get_row_data_by_row_index(row_index)
            for col_index in range(self.table_params.get("num_cols")) :
                col_params=self.col_params.get(col_index)
                col_width=col_params.get("width")
                pyray.draw_rectangle_lines(cursor_x,cursor_y,col_width,self.table_params.get("row_height"),self.table_outline_color)
                field_text=""
                if row_index==0 :
                    field_text=col_params.get("title")
                else :
                    field_name=col_params.get("key")
                    field_text=str(row_data.get(field_name))
                    if field_name=="num_seats" :
                        field_text+="max"
                    #print(field_text)
                pyray.draw_text_ex(self.table_pool_font,field_text,(cursor_x+8,cursor_y+3),14,0,pyray.Color(200,212,182,255))
                cursor_x+=col_width
