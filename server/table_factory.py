import random
from dealer import *
from common.view_model_factory import *
from common.view_model_controller import *
from table import Table
from seat import Seat
from table_observer import TableObserver
from server_thread import PokerServer

class TableFactory():
    last_table_id=1000
    #https://www.flavorwire.com/225706/the-most-ridiculous-ikea-product-names-and-what-they-mean
    #https://www.ikea.com/de/de/search/?q=table&page=2
    #https://www.housebeautiful.com/uk/lifestyle/a38500747/ikea-product-names-visit-sweden/
    table_names={
        "Fyrkantig"   :  0,
        "Riktig Ögla" :  0,
        "Grönkulla"   :  0,
        "Grundtal"    :  0,
        "Norrviken"   :  0,
        "Sparsam"     :  0,
        "Dagstorp"    :  0,
        "Flärdfukk"   :  0,
        "Knutstorp"   :  0,
        "Norröra"     :  0,
        "Ödmjuk"      :  0,
        "Smörboll"    :  0,
        "Sven"        :  0,
        "Jokkmokk"    :  0,
        "Knarrevik"   :  0,
        "Lagkapten"   :  0,
        "Voxlöff"     :  0,
        "Köttbullar"  :  0,
        "Smørrebrød"  :  0,
        "Bolmen"      :  0, # a large lake in the Småland region of southern Sweden (toilet brush)
        "Järvfjället" :  0, # a mountain in Swedish Lapland (gaming chair)
        "Extorp"      :  0, # a suburb of Stockholm (sofa)
        "Skärhamn"    :  0, # a fishing village on the island of Tjörn off the coast of West Sweden (door handle)
        "Stubbarp"    :  0, # a manor house in the Skåne region of southern Sweden (cabinet legs)
        "Kallax"      :  0, # a coastal village near Luleå in Swedish Lapland (storage shelf)
        "Höljes"      :  0, # one of the most sparsely populated areas in Sweden":0, # # a forest in the Värmland region (pendant lamp)
        "Hemsjö"      :  0, # a village in the Blekinge region (block candle)
        "Toftan"      :  0, # a lake in the Dalarna region (waste bin)
        "Mästerby"    :  0, # an historical battleground on the island of Gotland (a step stool)
        "Voxnan"      :  0, # a river with waterfalls and rapids in the Hälsingland region (shower shelf)
        "Himleån"     :  0, # ravines in the Halland region (bath towel)
        "Laxviken"    :  0, # a rural village in the Jämtland Härjedalen region (cabinet door)
        "Ingatorp"    :  0, # a village where you'll find one of Sweden’s oldest wooden buildings":0, # # in the Småland region (extendable table)
        "Misterhult"  :  0, # an archipelago of 2":0, # #000 islands near Kalmar in the Småland region (a bamboo lamp)
        "Vrena"       :  0, # a village near the east coast in the Sörmland region (countertop)
        "Björksta"    :  0, # a village close to the university town of Uppsala (picture with frame)
        "Norberg"     :  0, # a small town in Västmanland region (folding table)
        "Askersund"   :  0, # a small town near Örebro in central Sweden (cabinet door)
        "Rimforsa"    :  0, # a small village in the Östergötland region of east Sweden (work bench)
        "Bodviken"    :  0# a mountain lake in the UNESCO World heritage area of the High Coast in northern Sweden (washbasin).
    }

    roman_numeric_literals={
                  1   :  "I",
                  2   :  "II",
                  3   :  "III",
                  4   :  "IV",
                  5   :  "V",
                  6   :  "VI",
                  7   :  "VII",
                  8   :  "VIII",
                  9   :  "IX",
                  10  :  "X",
                  11  :  "XI",
                  12  :  "XII",
                  13  :  "XIII",
                  14  :  "XIV",
                  15  :  "XV",
                  16  :  "XVI",
                  17  :  "XVII",
                  18  :  "XVIII",
                  19  :  "XIX",
                  }
    def generate_table_name():
        name,count = random.choice(list(TableFactory.table_names.items()))
        count+=1
        TableFactory.table_names[name]=count
        table_name=name+" "+TableFactory.roman_numeric_literals.get(count)
        return table_name

    def create_table_nlhe_6max():
        table_name=TableFactory.generate_table_name()
        print("DEBUG :[TableFactory] : creating Table '",table_name,"'")
        TableFactory.last_table_id+=1
        table=Table(TableFactory.last_table_id,table_name,num_seats=6,game_type="nlhe",stakes={"sb":1,"bb":2})
        for seat_id in range(table.num_seats):
            seat=Seat(seat_id)
            table.add_seat(seat)
        observer=TableObserver()
        observer.set_proxy(PokerServer.get_instance())
        observer.observe(table)
        return table
