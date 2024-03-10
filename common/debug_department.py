global_log_domain_params={
    #domain
    #log_domain aka file_name/'klass_name'
    "main_client":{
        #log_domain_user aka function/method name
        "create_table_window" : {           #key_tags
                "log_any" : True,
                "show_table_view_request":True
                },

        "__main__" : {
                "log_any" : True,
                "handle_message_inbox":True,
                "pending_table_view_requests_append":True,
                "handle_pending_table_view_request":True,
                "pending_table_view_request_duplicate":True,
                "handle_table_window_message_inbox":True,
                "remove_table_request_found":True,
                "error_remove_table_request_not_found":True,
                "table_window_delete":True,
                "broadcast_send_shutdown":True
                },
        },

    "connection_thread":{
            "__init__":{
                "log_any":True
                },
            "unregister_table_id":{
                "log_any":True
                },
            "handle_connection_error":{
                "log_any":True,
                "graceful_disconnect":True
                },
            "connect_to_server":{
                "log_any":False,
                "connect_retry":True,
                "connect_success":True,
                "connect_fail":True
                },
            "disconnect_from_server":{
                "log_any":True,
                "disconnect_on_purpose":True
            },
            "handle_message_inbox":{
                "log_any":False,
                "received_ping":True,
                "created_response_pong":True,
                "received_push_table_pool_view":True,
                "received_push_table_view":True
                },
            "update_table_views":{
                "log_any":False,
                "received_table_view_data":False,
                "warning_dropping_table_view_data":True
                },
            "update_table_events":{
                "log_any":False,
                "received_table_event":True,
                "warning_dropping_table_event_data":True,
                "warning_max_table_events_count":True
                }
            },
    "lobby_window":{
            "lobby_window_launch":{
                "log_any":False,
                "message_receive":True,
                "receive_table_pool_data":False,
                "user_event_pop_from_table_pool_view":False
            },
        },
    "table_window":{
            "table_window_launch":{
                "log_any":False,
                "message_receive_any":False,
                "message_receive_table_window_update":False,
                "message_receive_table_window_event":False
            },
        },
    "table_pool_view_renderer":{
            "draw_table":{
                "log_any":False,
                "add_user_event":False
            }
    }
}
#@param lfs - defaults to char(space) as seperator between str(args)
def DONK_LOG(log_prefix=None,log_domain=None,log_domain_user=None,log_domain_user_key=None,log_args=[]):
    assert log_domain is not None
    assert log_domain_user is not None
    assert log_prefix is not None
    lfs=" "
    #if log_domain!="openDonk" :
    domain_params=global_log_domain_params.get(log_domain)
    e_invalid_log_domain="log_domain '"+str(log_domain)+"'"+" does not exist in debug_department.global_log_domain_params"
    assert domain_params is not None,e_invalid_log_domain
    user_params=domain_params.get(log_domain_user)
    e_invalid_log_domain_user="log_domain_user '"+str(log_domain_user)+"'"+" does not exist in log_domain "+"'"+str(log_domain)+"'"
    assert user_params is not None,e_invalid_log_domain_user
    debug_param=user_params.get(log_domain_user_key)
    e_invalid_key="user_key "+"'"+str(log_domain_user_key)+"'"+" does not exist for log_domain_user "+"'"+str(log_domain_user)+"'"
    assert debug_param is not None,e_invalid_key
    if debug_param==True :
        log_message=str(log_prefix)+" : "
        log_message+="["+str(log_domain)+"."+str(log_domain_user)+"]"
        if len(log_args)==0 :
            log_message+=" "+str(log_domain_user_key)
        else :
            for arg in log_args :
                log_message+=lfs
                log_message+=str(arg)
        print(log_message)

def DONK_DEBUG(domain,domain_user,user_key,*args):
    DONK_LOG(log_prefix="DEBUG",log_domain=domain,log_domain_user=domain_user,log_domain_user_key=user_key,log_args=args)
def DONK_WARNING(domain,domain_user,user_key,*args):
    DONK_LOG(log_prefix="WARNING",log_domain=domain,log_domain_user=domain_user,log_domain_user_key=user_key,log_args=args)
def DONK_ERROR(domain,domain_user,user_key,*args):
    DONK_LOG(log_prefix="ERROR",log_domain=domain,log_domain_user=domain_user,log_domain_user_key=user_key,log_args=args)

  #debug_params=client_debug_params

    #if log_domain=="client":
    #    debug_params=client_debug_params
    #else :
    #    assert False,"NOT_IMPLEMENTED"

    #valid_log_levels=[OD_ERROR,OD_WARNING,OD_DEBUG,OD_INFO]
    #log_level_literals=["ERROR","WARNING","DEBUG","INFO"]

    #assert log_level in valid_log_levels,"invalid log level"
