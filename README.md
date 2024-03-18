# openDonk

purpose : poker client/server application for machine learning experiments.
footage : [YouTube](https://www.youtube.com/watch?v=osxyx6oaBag)

prototype in python, using raylib/pyray. you'll need this: 
https://electronstudio.github.io/raylib-python-cffi/index.html

this is a recreational programming challenge and work in progress.
in case you're wondering - the players have no agency at all. 
they are pushing random buttons in a fixed limit holdem style,
the dealer knows the game - i think^^

its a long long way ...


on first run:
```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

deactivate virtual environment:
```
deactivate
```

after first run:
```
source env/bin/activate
```

server entry point :
```
cd server
python main.py
```

client entry point :
```
cd client
python ./main_client.py
```

Credits for the card assets go here :
```md
https://byronknoll.blogspot.com/2011/03/vector-playing-cards.html
```

>Credit for the cringe code belongs to me.

Note : it does work on my win11 machine now, but theres still a bunch of ugly multiprocessing/pipe errors. 
