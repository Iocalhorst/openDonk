import logging
from deck import *
#nut low                                    (23457)  =   2  +   3  +   4  +   5  +  7  =  21   |    +     0   =    21
#best nopair hand values                    (AKQJ9)  =  14  +  13  +  12  +  11  +  9  =  59   |    +     1   =    60
#lowest one pair +lowest 3 holdcards        (22345)  =   2  +   2  +   3  +   4  +  5  =  16   |    +    60   =    76
#best one pair      + best 3 kicker         (AAKQJ)  =  14  +  14  +  13  +  12  + 11  =  64   |    +    60   =   124 + 1
#lowest two pair + best kicker              (22334)  =   2  +   2  +   3  +   3  +  4  =  14   |    +   125   =   139
#best two pair      + best kicker           (AAKKQ)  =  14  +  14  +  13  +  13  + 12  =  65   |    +   125   =   190 + 1
#lowest 3oak      + best 2 kicker           (22234)  =   2  +   2  +   2  +   3  +  4  =  13   |    +   191   =   204
#highest 3oak     + top 2 kicker            (AAAKQ)  =  14  +  14  +  14  +  13  + 12  =  67   |    +   191   =   258 + 1
#lowest straight ("wheel")                  (A2345)  =   1  +   2  +   3  +   4  +  5  =  12   |    +   259   =   271
#2nd lowest straight                        (23456)  =   2  +   3  +   4  +   5  +  6  =  20   |    +   259   =   279
#highest straight ("broadway")              (AKQJT)  =  14  +  13  +  12  +  11  + 10  =  60   |    +   259   =   319 + 1
#lowest  flush                              (23457)  =   2  +   3  +   4  +   5  +  7  =  21   |    +   320   =   341
#highest flush                              (AKQJ9)  =  14  +  13  +  12  +  11  +  9  =  59   |    +   320   =   379 + 1
#lowest full house                          (22233)  =   2  +   2  +   2  +   3  +  3  =  12   |    +   380   =   392
#highest full house                         (AAAKK)  =  14  +  14  +  14  +  13  + 13  =  68   |    +   380   =   448 + 1
#lowest  4oak                               (22223)  =   2  +   2  +   2  +   2  +  3  =  11   |    +   449   =   569
#highest 4oak                               (AAAAK)  =  14  +  14  +  14  +  14  + 13  =  69   |    +   449   =   508 + 1
#lowest straight flush                      (A2345)  =   1  +   2  +   3  +   4  +  5  =  15   |    +   509   =   524
#2nd lowest straight flush                  (23456)  =   2  +   3  +   4  +   5  +  6  =  20   |    +   509   =   529 + 1
#royal flush                                (AKQJT)  =  14  +  13  +  12  +  11  + 10  =  60   |    +   530   =   590

category_biases={       "high card"  :     0,
                         "one pair"  :    60,
                        "two pair"   :   125,
                 "three of a kind"   :   191,
                        "straight"   :   259,
                           "flush"   :   320,
                      "full house"   :   380,
                  "four of a kind"   :   449,
                  "straight flush"   :   509,
                     "royal flush"   :   530
                     }


def is_flush(cards):
    clubs=[]
    spades=[]
    hearts=[]
    diamonds=[]

    for c in cards :
        if c.s=="c" :
            clubs.append(c)
        if c.s=="s" :
            spades.append(c)
        if c.s=="h" :
            hearts.append(c)
        if c.s=="d" :
            diamonds.append(c)
    clubs.sort()
    spades.sort()
    hearts.sort()
    diamonds.sort()
    if len(clubs)>=5 :
        i=len(clubs)
        hand=[clubs[i-1],clubs[i-2],clubs[i-3],clubs[i-4],clubs[i-5]]
        return True,hand
    if len(spades)>=5 :
        i=len(spades)
        hand=[spades[i-1],spades[i-2],spades[i-3],spades[i-4],spades[i-5]]
        return True,hand
    if len(hearts)>=5 :
        i=len(hearts)
        hand=[hearts[i-1],hearts[i-2],hearts[i-3],hearts[i-4],hearts[i-5]]
        return True,hand
    if len(diamonds)>=5 :
        i=len(diamonds)
        hand=[diamonds[i-1],diamonds[i-2],diamonds[i-3],diamonds[i-4],diamonds[i-5]]
        return True,hand
    return False,cards

def is_straight(cards):
    unique_vals=[]
    unique_cards=[]
    for c in cards :
        if c.val not in unique_vals :
            unique_cards.append(c)
            unique_vals.append(c.val)
    hand=[]
    if 14 in unique_vals and 13 in unique_vals and 12 in unique_vals and 11 in unique_vals and 10 in unique_vals :
        for uc in unique_cards :
            if uc.val>=10 and uc.val<=14:
                hand.append(uc)
        return True,hand
    if 13 in unique_vals and 12 in unique_vals and 11 in unique_vals and 10 in unique_vals and 9 in unique_vals :
        for uc in unique_cards :
            if uc.val>=9 and uc.val<=13:
                hand.append(uc)
        return True,hand
    if 12 in unique_vals and 11 in unique_vals and 10 in unique_vals and 9 in unique_vals and 8 in unique_vals :
        for uc in unique_cards :
            if uc.val>=8 and uc.val<=12:
                hand.append(uc)
        return True,hand
    if 11 in unique_vals and 10 in unique_vals and 9 in unique_vals and 8 in unique_vals and 7 in unique_vals :
        for uc in unique_cards :
            if uc.val>=7 and uc.val<=11:
                hand.append(uc)
        return True,hand
    if 10 in unique_vals and 9 in unique_vals and 8 in unique_vals and 7 in unique_vals and 6 in unique_vals :
        for uc in unique_cards :
            if uc.val>=6 and uc.val<=10:
                hand.append(uc)
        return True,hand
    if 9 in unique_vals and 8 in unique_vals and 7 in unique_vals and 6 in unique_vals and 5 in unique_vals :
        for uc in unique_cards :
            if uc.val>=5 and uc.val<=9:
                hand.append(uc)
        return True,hand
    if 8 in unique_vals and 7 in unique_vals and 6 in unique_vals and 5 in unique_vals and 4 in unique_vals :
        for uc in unique_cards :
            if uc.val>=4 and uc.val<=8:
                hand.append(uc)
        return True,hand
    if 7 in unique_vals and 6 in unique_vals and 5 in unique_vals and 4 in unique_vals and 3 in unique_vals :
        for uc in unique_cards :
            if uc.val>=3 and uc.val<=7:
                hand.append(uc)
        return True,hand
    if 6 in unique_vals and 5 in unique_vals and 4 in unique_vals and 3 in unique_vals and 2 in unique_vals :
        for uc in unique_cards :
            if uc.val>=2 and uc.val<=6:
                hand.append(uc)
        return True,hand
    if 5 in unique_vals and 4 in unique_vals and 3 in unique_vals and 2 in unique_vals and 14 in unique_vals :
        for uc in unique_cards :
            if uc.val==14 :
                hand.append(uc)
        for uc in unique_cards :
            if uc.val>=2 and uc.val<=5 :
                hand.append(uc)

        tmp=hand[0]
        hand[0]=hand[4]
        hand[4]=tmp
        return True,hand
    return False,cards



def is_4oak(cards):
    matching_val=0
    for v in values :
        count=0
        for c in cards :
            if c.val==v :
                count+=1
                if count==4 :
                    matching_val=c.val
                    break
    if matching_val==0 :
        return False,cards
    hand=[]
    for c in cards:
        if c.val==matching_val:
            hand.append(c)
            cards.remove(c)
    cards.sort()
    cards.reverse()
    hand.append(cards[0])
    return True,hand


def is_full(cards):
    #no trips - no full
    matching_val_trips=0
    #no pair - no full
    matching_val_pair=0

    for v in values :
        count=0
        for c in cards :
            if c.val==v :
                count+=1
                if count==3 :
                    matching_val_trips=c.val
                    break

    if matching_val_trips==0 :
        return False,cards

    for v in values :
        count=0
        for c in cards :
            if c.val!=matching_val_trips and c.val==v :
                count+=1
                if count==2 :
                    matching_val_pair_a=c.val
                    break

    if matching_val_pair==0:
        return False,cards

    #we have to cover the case of another pair in the hold, higher than the one we already got
    for v in values :
        count=0
        for c in cards :
            if c.val!=matching_val_trips and c.val!=matching_val_pair and c.val==v :
                count+=1
                if count==2 :
                    if c.val>matching_val_pair :
                        matching_val_pair=v
                    break

    hand=[]
    for c in cards :
        if c.val==matching_val_trips :
            hand.append(c)
    for c in cards :
        if c.val==matching_val_pair :
            hand.append(c)
    return True,hand


def is_3oak(cards):
    matching_val=0
    for v in values :
        count=0
        for c in cards :
            if c.val==v :
                count+=1
                if count==3 :
                    matching_val=c.val
                    break
    if matching_val==0 :
        return False,cards

    triplet=[]
    for c in cards :
        if c.val==matching_val:
            triplet.append(c)

    kicker1=None
    for c in cards :
        if c.val!=matching_val :
            if kicker1 :
                if c.val>kicker1.val:
                    kicker1=c
            else :
                kicker1=c
    kicker2=None
    for c in cards :
        if c.val!=matching_val and c.val!=kicker1.val:
            if kicker2 :
                if c.val<kicker2.val:
                    kicker2=c
            else :
                kicker2=c
    hand=triplet
    hand.append(kicker1)
    hand.append(kicker2)
    return True,hand


def is_one_pair(cards):
    pair_val=0
    kicker1=None
    kicker2=None
    kicker3=None

    for v in values :
        count=0
        for c in cards :
            if c.val==v :
                count+=1
                if count==2 :
                    pair_val=v
                    break

    if pair_val==0 :
        return False,cards

    for c in cards :
        if c.val!=pair_val :
            if kicker1 :
                if c.val>kicker1.val :
                    kicker1=c
            else :
                kicker1=c
    for c in cards :
        if c.val!=pair_val and c.val!=kicker1.val:
            if kicker2 :
                if c.val>kicker2.val :
                    kicker2=c
            else :
                kicker2=c
    for c in cards :
        if c.val!=pair_val and c.val!=kicker1.val and c.val!=kicker2.val:
            if kicker3 :
                if c.val>kicker3.val :
                    kicker3=c
            else :
                kicker3=c

    hand=[]
    for c in cards :
        if c.val==pair_val:
            hand.append(c)
    hand.append(kicker3)
    hand.append(kicker2)
    hand.append(kicker1)
    return True,hand

def is_two_pair(cards):
    kicker=None
    pair_values=[]
    for v in values :
        count=0
        for c in cards :
            if c.val==v :
                count+=1
                if count==2 :
                    pair_values.append(v)
                    break

    if len(pair_values)<2 :
        return False,cards

    pair_values.reverse()
    hand=[]
    for c in cards :
        if c.val==pair_values[0]:
            hand.append(c)
    for c in cards :
        if c.val==pair_values[1]:
            hand.append(c)

    kicker=None
    for c in cards :
        if c.val not in pair_values :
            if kicker :
                if c.val>kicker.val :
                    kicker=c
            else :
                kicker=c



    hand.append(kicker)
    return True,hand

def cards_sum(cards):
    s=0
    for c in cards :
        s+=c.val
    return s

def determine_best_combination(flop,turn,river,holdcards):
    cards=[]
    for c in flop :
        cards.append(c)
    cards.append(turn)
    cards.append(river)
    for h in holdcards :
        cards.append(h)
    cards.sort()

    has_flush,hand=is_flush(cards)
    has_straight,hand=is_straight(hand)

    if has_flush :
        if has_straight :
            if hand[4].val==14 :
                score=category_biases["royal flush"]+cards_sum(hand)
                #l0g("royal flush! : ",hand," score : ",score)
                return "royal flush",hand,score
            else :
                score=category_biases["straight flush"]+cards_sum(hand)
                #l0g("straight flush! : ",hand,"score: ",score)
            return "straight flush",hand,score
        else :
            score=category_biases["flush"]+cards_sum(hand)
            #l0g("flush : ",hand,"score: ",score)
        return "flush",hand,score

    cards.reverse()
    has_4oak,hand=is_4oak(cards)
    if has_4oak :
        score=category_biases["four of a kind"]+cards_sum(hand)
        #l0g("four of a kind : ",hand,"score : ",score)
        return "four of a kind",hand,score

    has_full,hand=is_full(cards)
    if has_full :
        score=category_biases["full house"]+cards_sum(hand)
        #l0g("full house : ",hand,"score : ",score)
        return "full house",hand,score

    has_straight,hand=is_straight(cards)
    if has_straight :
        score=category_biases["straight"]+cards_sum(hand)
        #l0g("straight : ",hand,"score : ",score)
        return "straight",hand,score

    has_3oak,hand=is_3oak(cards)
    if has_3oak :
        score=category_biases["three of a kind"]+cards_sum(hand)
        return "three of a kind: ",hand,score

    has_two_pair,hand=is_two_pair(cards)
    if has_two_pair :
        score=category_biases["two pair"]+cards_sum(hand)
        #l0g("two pair : ",hand,"score : ",score)
        return "two pair : ",hand,score

    has_one_pair,hand=is_one_pair(cards)
    if has_one_pair :
        score=category_biases["one pair"]+cards_sum(hand)
        #l0g("pair : ",hand,"score : ",score)
        return "pair",hand,score

    cards.sort()
    cards.reverse()
    hand=[]
    for i in range(5) :
        hand.append(cards[i])
    score=cards_sum(hand)
    score=category_biases["high card"]+cards_sum(hand)
    #l0g("high card : ",hand,"score : ",score)
    return "high card",hand,score
