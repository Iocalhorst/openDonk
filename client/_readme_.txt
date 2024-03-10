this file has been last updated on day38

the entry point of the client application is ./client/main_client.py

    i dont like having main.py as entry point because of monitoring with htop is kinda hard when process names arent unique.
    but im used to type "python3 main[...]" in the console and use tab autocomplete.
    thats why i keep "main" as prefix for both(server/client) entry points.


main_client.py runs in its process along with the "connection_thread"

    it hosts and manages all of the windows via piped ipc message exchange.
    the message protocol is "under construction". im making things up as i go.
    there will be a refactoring/consolidation session very soon. oh joy.

main_client.py will (after initializing itself) create a second process in which the main window lives.

    the main_window_process is defined in main_window.py

the ipc message protocol at this point

    there are create_message functions all over the place. those need to be consolidated.
    fow now the goal is to not have any message creating expressions in places that are not a ipc_message_create function.
    its 302 forbidden and will be punished with exmatriculation. (it will get you fired if done repeatedly)
    that said ... the user events are rising. its only one event atm. but its the same problem, same deal.

the main_window.py uses raylib

    the matrix background animation uses way to much cpu time.
    its the ridiculous number of calls to pyray.draw_text() that drives the usage up.
    this needs to be fixed. if not removed. but not today.
