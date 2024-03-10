
#takes incoming datasets
#queues these
#TODO : transforms theses into ipc messages for adressing the window process.
#TODO : implement some sort of internal window state update/tracking/housekeeping to extract the table_window routing from the main_client


class WindowMessenger():

    #class method
    def create_ipc_lobby_window_should_close_message(window_id):
        m={
            "MESSAGE_TYPE":"WINDOW_EVENT",
            "MESSAGE_DATA":{
                "WINDOW_EVENT_TYPE":"LOBBY_WINDOW_SHOULD_CLOSE",
                "WINDOW_ID":window_id,
                }
            }
        return m

    def create_ipc_table_window_should_close_message(table_window_id,table_id):
        m={
            "MESSAGE_TYPE":"WINDOW_EVENT",
            "MESSAGE_DATA": {
                "WINDOW_EVENT_TYPE":"TABLE_WINDOW_SHOULD_CLOSE",
                "WINDOW_ID":table_window_id,
                "TABLE_ID":table_id,
                }
        }
        print("DEBUG : [WindowMessenger] create_ipc_table_window_should_close_message")
        return m

    def create_ipc_table_pool_view_update_message(self,table_pool_view_data):
        assert table_pool_view_data is not None,"im sorry dave, but i cant let you do that. pool_data is None"
        m={
            "MESSAGE_TYPE":"TABLE_POOL_VIEW_DATA_UPDATE",
            "TABLE_POOL_VIEW_DATA":table_pool_view_data
        }
        return m

    def create_ipc_table_window_update_message(self,table_window_id,table_id,table_view_data):
        assert table_view_data is not None,"im sorry dave, but i cant let you do that, table_view_data is None"
        m={
            "MESSAGE_TYPE":"TABLE_WINDOW_UPDATE",
            "WINDOW_ID":table_window_id,
            "MESSAGE_DATA":{
                "TABLE_ID":table_id,
                "TABLE_VIEW_DATA":table_view_data
                }
            }
        return m
        print("DEBUG : [window_messenger.create_ipc_table_view_update_message] table_view_data == ",table_view_data)
#        return table_id,ipc_message

    def create_ipc_table_window_event_message(self,table_window_id,table_id,table_event_type,table_event_data):
        assert table_event_data is not None,"im sorry dave, param table_event_data is None"
        assert table_event_type is not None,"im sorry dave, param table_event_type is None"
        valid_table_event_types=["SEAT_EVENT","POT_EVENT","DEALER_EVENT"]
        assert table_event_type in valid_table_event_types
        assert table_window_id is not None,"im sorry dave, param window_id is None"
        assert table_window_id>0,"im sorry dave, param window_id is invalid for table_window_ids"
        assert table_id is not None,"im sorry dave, param table_id is None"
        assert table_id>1000,"im sorry dave, param table_id is not in range for valid table_ids"
        m={
            "MESSAGE_TYPE":"TABLE_WINDOW_EVENT",
            "WINDOW_ID":table_window_id,
            "MESSAGE_DATA":{
                "TABLE_ID":table_id,
                "TABLE_EVENT_TYPE":table_event_type,
                "TABLE_EVENT_DATA":table_event_data
                }
            }
        return m


    def create_ipc_disconnected_message(self):
        m={
            "MESSAGE_TYPE":"BROADCAST_EVENT",
            "EVENT_TYPE":"DISCONNECTED"
        }
        return m

    def create_ipc_connected_message(self):
        m={
            "MESSAGE_TYPE":"BROADCAST_EVENT",
            "EVENT_TYPE":"CONNECTED"
        }
        return m

    def create_ipc_shutdown_message(self):
        m={
            "MESSAGE_TYPE":"BROADCAST_EVENT",
            "EVENT_TYPE":"SHUTDOWN"
        }
        return m
