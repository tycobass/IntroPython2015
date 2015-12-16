
import random
from collections import Counter



def roll(numDice):
    dice =[random.randint(1,6) for x in range(numDice)]
    return dice



def scorecard(dice):
    category = input("Enter the category you want to input your score: ")
    dicecount = Counter(dice)
    keylist = list(dicecount.keys())
    valuelist = list(dicecount.values())

    card = """

    -----------------------------------------
           Yahtzee scorecard
    -----------------------------------------
    """

    ones = 0
    twos = 0
    threes = 0
    fours = 0
    fives = 0
    sixes = 0
    toptotal = ones + twos + threes + fours + fives + sixes
    bonus = 0
    trips = 0
    quads = 0
    house = 0
    smstr = 0
    lgstr = 0
    yahtzee = 0
    chance = 0
    bottotal = trips + quads + house + smstr + lgstr + yahtzee
    total = toptotal + bottotal
    score = 0
    
    if category == 1:
        ones = dice.count(1) * 1

    elif category == 2:
        twos = dice.count(2) * 2

    elif category == 3:
        threes = dice.count(3) * 3

    elif category == 4:
        fours = dice.count(4) * 4

    elif category == 5:
        fives = dice.count(5) * 5

    elif category == 6:
        sixes = dice.count(6) * 6

    elif category == 7 and 3 in valuelist:
        trips = sum(dice)

    elif category == 8 and 4 in valuelist:
        quads = sum(dice)

    elif category == 9 and (3 and 2 in valuelist):
        house = 25

    elif category == 10 and len(keylist) > 3:
        smstr = 30

    elif category == 11 and len(keylist) > 4:
        lgstr = 40

    elif category == 12 and len(keylist) == 5:
        yahtzee = 50 

    elif category == 13:
        chance = sum(dice)

    print(card)
    print("Ones:           {}".format(ones))
    print("Twos:           {}".format(twos))
    print("Threes:         {}".format(threes))
    print("Fours:          {}".format(fours))
    print("Fives:          {}".format(fives))
    print("Sixes:          {}".format(sixes))
    print("Top Total:      {}".format(toptotal))
    print("Bonus:          {}\n".format(bonus))
    print("3 of a kind:    {}".format(trips))
    print("4 of a kind:    {}".format(quads))
    print("Full House:     {}".format(house))
    print("Sm.Straght:     {}".format(smstr))
    print("Lg.Straght:     {}".format(lgstr))
    print("Yahtzee:        {}".format(yahtzee))
    print("Chance:         {}".format(chance))
    print("Bot.Total:      {} \n".format(bottotal))
    print("Total:          {}".format(total))
    print(category)



def main():
    
    roll1 = roll(5)

    print(roll1)

    keep1 = [int(x) for x in input("Enter the dice you want to keep 1-5 and separate by comma or 9 to score or 0 to quit: ").split(',')]

    if keep1[0] == 9:
        scorepad()
    if keep1[0] == 0:
        quit()
    else:
        roll2 = keep1 + roll(5 - len(keep1))

    print(roll2)

    keep2 = [int(x) for x in input("Enter the dice you want to keep 1-5 and separate by comma or 9 to score or 0 to quit: ").split(',')]

    if keep2[0] == 9:
        scorepad()
    if keep2[0] == 0:
        quit()
    else:
        roll3 = keep2 + roll(5 - len(keep2))

    print(roll3)

    scorecard(roll3)

    

if __name__ == "__main__": main()















