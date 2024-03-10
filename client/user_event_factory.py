class UserEventFactory():

    def create_user_event(user_event_type,user_event_data):
        user_event={
        "USER_EVENT_TYPE": user_event_type,
        "REQUEST_DATA": user_event_data
        }
        return user_event
