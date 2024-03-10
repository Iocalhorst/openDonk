#
#
#"EVENT_DOMAIN_TYPES"={
#
#
#    "TABLE_EVENT" : {}
#
#    "DEALER_EVENTS":
#            "EVENT_DEALER_INIT"       -> "STATE_WAIT_FOR_PLAYERS_OK"
#            "EVENT_PLAYERS_OK"        -> "EVENT_DEALER_START_SOON"
#            "EVENT_DEALER_START_SOON" -> "EVENT_ANNOUNCE_START","STATE_DEALER_WAIT_15"
#            "EVENT_DEALER_TIMOUT"     -> "EVENT_DEALER_START","EVENT_DEALER_ABORT"
#            "EVENT_DEALER_START"      -> "EVENT_HAND_INIT"
#            "EVENT_HAND_ABORT"        -> "EVENT_DEALER_INIT"
#            "EVENT_HAND_FINISH"       -> "EVENT_DEALER_NEXT"
#
#
#
#
#
#
#
#            _HAND"REGISTER_FAIL"     -> "EVENT_HAND_ABORT"
#            ENUMERATE_SEATS","STATE_WAITASSIGN_BU","EVENT_""STATE_"
#            "STATE_AWAIT"
#            "EVENT_DEALER_ABORT"      -> "EVENT_INIT"
#            "EVENT_DEALER_OK"         -> "STATE_HAND_IN_PROGRESS","WAIT_HAND_FINISHED"
#
#            "EVENT_TIMER_START","EVENT_ANNOUNCE_START",
#            "EVENT_TIMER_ALARM" -> "STATE_AWAIT_DEALER" "EVENT_DEALER_INITIALIZE"
#            "EVENT_TIMEOUT"     -> "STATE_DOUBLE_CHECK"
#            ""
#            "EVENT_PLAYERS_PRE"
#    "}
#
#    "HAND_EVENT":
#        "EVENT_HAND_INIT"         -> "EVENT_REGISTER_PLAYERS"
#    "POT_EVENT":
#    "PLAYER_EVENT":
#    "SEAT_EVENT":
#
#
#"}
#
#
#
#    "EVENT_TYPE_ASSIGN_BU" #dealer_event?!
#            -> "button is at $seat"
#    "EVENT_TYPE_OPTION_POST"
#            -> "deine mudda posts sb"
#    "HAND_EVENT_OPTION_POST_BB"
#    "HAND_EVENT_OPTION_REJECT"
#    "HAND_EVENT_POST_SB"
#    "HAND_EVENT_POST_BB"
#    "HAND_EVENT_POST_BB"
#    "HAND_EVENT_DEAL_CARDS"
#            ->
#    "HAND_EVENT_OPTION_OPEN"
#
