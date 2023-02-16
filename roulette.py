import random

def main():
    #welcome comments
    print("=----------------------------------------------=")
    print("     Welcome to a Python Roullete simulator     ")
    print("=----------------------------------------------=")
    print("  This is European Roullete so there is one 0  ")
    print("   You can choose to bet on the Outside bets   ")
    print("    and/or you can bet on multiple numbers.    ")
    print("     i would recomend having a picture of a    ")
    print("          roullete board already open          ")
    print("=----------------------------------------------=")
    intialize()
    
def intialize():
    bets = {} 
    #intializes number of coins
    print("how many coins do you want to start with?")
    coins = get_postive_num()
    #intializes betting minium
    print("what betting minium do you want?")
    limit = get_postive_num()
    print("----GAME START----")
    start(coins,limit,bets)
    
def start(coins,limit, bets):
    print("you have " + str(coins) + " coins left")
    print("do you want to to bet on Inside(numbers), or on Outside?")
    print("i = Inside | o = Outside")
    #santizes input to either go to bet on inside or outside table bets
    #inside being just the numbers
    #outside being black red, odd even, etc.
    while True:
        choice = input().lower()
        if choice == "i":
            #inside bet selected
            inside(coins,limit,bets)
        elif choice == "o":
            #outside bet selected
            outside(coins,limit,bets)
        else:
            print("not a valid choice try again")
            continue
        
def inside(coins,limit, bets):
    #asks how many coins user wants to bet
    coinsBet = get_bet(coins,limit)
    print("bet is " + str(coinsBet) + " coins")
    # ask number of bets to place
    print("how many bets do you want to make with your " + str(coinsBet) +" coins?")
    n = num_of_bets(coins,limit,coinsBet)
    #updating balance based on how many bets made with coinsBet
    coins = coins - n * coinsBet
    #iterating through the amount of bets requested
    for i in range(0, n):
        print("what number do you want to pick?")
        ele = get_postive_num() 
        if 0 <= ele <= 36: # check if number is on the board
            bets[ele] = coinsBet #if choice is in range then add it to the dictionary of bets
        else:
            print("not a number on the board try again")
            n += 1
    #known problem where if you input to only do 1 bet, and you mess one up, will place no bets and take coins
    #known problem where if you input same number over and over, will suck up your coins
    #asks if user wants to keep betting
    print("your bets are on" + str(bets))
    keep_betting(coins,limit, bets)
    
def num_of_bets(coins,limit,coinsBet):
    #checks to see if user has the balance to make the number of bets
    while True:
        n = get_postive_num()
        if coins < coinsBet * n:
            print("not enough balance to place bet, please try again")
            continue
        if limit > coinsBet * n:
            print("lower then the limit of " + str(limit) + " please try again")
            continue
        else:
            return n
        
def outside(coins,limit,bets):
    #asks how many coins user wants to bet
    coinsBet = get_bet(coins,limit)
    #updates user balance
    coins = coins - coinsBet
    print("bet is " + str(coinsBet) + " coins")
    #lists off all the bets a user can make on the outside
    print("what do you want to bet on?")
    print("40 = 1st 12 | 41 = 2nd 12 | 42 = 3rd 12")
    print("43 = odd | 44 = even | 45 = red | 46 = black")
    print("47 = 1-18 | 48 = 19-36|")
    print("49 = Top row | 50 = middle | 51 = bottom row (look up a picture)")
    while True:
        print("what would you like to choose? : ")
        choice = get_postive_num()
        if 40 <= choice <= 51:
            #if choice is in range then add it to the dictionary of bets
            bets[choice] = coinsBet
            #asks if user wants to keep betting
            print("your bets are on" + str(bets))
            keep_betting(coins,limit, bets)
        else:
            print("not a valid choice try again")
            continue

def get_bet(coins,limit):
    #checks to see if user has the balance to make the bet and that it is over the minimum
    while True:
        print("How much do you want to bet?")
        coinsBet = get_postive_num()
        if coinsBet > coins:
            print("not enough balance to place bet")
            continue
        if coinsBet < limit:
            print("lower then the limit of " + str(limit) + " please try again")
            continue
        else:
            return coinsBet

def get_postive_num():
    #santizes input to only get a number higher then 0
    while True:
        try:
            number = int(input("input number: "))
            if number >= 0:
                return number
            else:
                print("not valid number try again")
        except:
            print("not valid number try again")
            
def keep_betting(coins,limit, bets):
    #asks if the user wants to keep betting
    print("would you like to bet on more? (n will make it spin)")
    while True:
        choice = input("y = yes | n = no :")
        if choice == "y":
            #if the user doesnt have enough coins, will just spin
            if coins == 0:
                print("sorry not enough coins starting the spin")
                spin(coins,limit,bets)
            else:
                start(coins,limit,bets)
        elif choice == "n":
            spin(coins,limit,bets)
        else:
            print("not a valid choice try again")
            continue

def spin(coins,limit,bets):
    #spin a random number between 0 and 36
    spunNum = random.randrange(0, 36)
    print("Number is " + str(spunNum) + "!")
    #check the outside winning bets (is a lot of weird ones so just a lot of math)
    outsideWinners = check_outside(spunNum)
    #passes the dictionary from outside winners, with the dictionary of bets made, to check final winnings
    check_winnings(coins,spunNum,outsideWinners,limit,bets)

def check_outside(spunNum):
    #intializes dictionary for outside win bets
    #key is what won, value is payout
    #winning selection : payout
    outsideWinners = {}
    blackNums = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]
    top = [3,6,9,12,15,18,21,24,27,30,33,36]
    middle = [2,5,8,11,14,17,20,23,26,29,32,35]
    if spunNum == 0:
        #if its 0 just break payout is handled as inside
        outsideWinners = {100:100}
    if spunNum >= 12:
        #1st 12, payout 1:2
        outsideWinners[40] = 2
    elif 12 < spunNum <=24:
        #2nd 12, payout 1:2
        outsideWinners[41] = 2
    else:
        #3nd 12, payout 1:2
        outsideWinners[42] = 2
    if (spunNum % 2) != 0:
        #even, payout 1:1
        outsideWinners[43] = 1
    else:
        #odd, payout 1:1
        outsideWinners[44] = 1
    if spunNum not in blackNums:
        #red, payout 1:1
        print("Number is red")
        outsideWinners[45] = 1
    else:
        print("Number is black")
        #black, payout 1:1
        outsideWinners[46] = 1
    if spunNum <= 18:
        #1-18, payout 1:1
        outsideWinners[47] = 1
    else:
        #19-36, payout 1:1
        outsideWinners[48] = 1
    if spunNum in top:
        #top row of numbers, payout 1:2
        outsideWinners[49] = 2
    elif spunNum in middle:
        #middle row of numbers, payout 1:2
        outsideWinners[50] = 2
    else:
        #bottom row of numbers, payout 1:2
        outsideWinners[51] = 2
    return outsideWinners

def check_winnings(coins,spunNum,outsideWinners,limit,bets):
    #iterates through the list of outside table bets
    for num in outsideWinners:
        #if a outside bet matches up then winner
        if num in bets:
            print("winner on the outside table")
            payout = outsideWinners[num]
            print("payout is " + str(payout) + " for this bet")
            #caculates payout based on the payout for function check_outside
            coins = coins + payout * bets[num]
    #iterates through the list bets on numbers
    for num in bets:
        #if a number matches up, then payout 1:35
        if num == spunNum:
            print("winner on the number " + str(num))
            coins = coins + bets[num] * 35
            print("new coins balance is " + str(coins))
    #clear bets
    spunNum = 0
    outsideWinners = {}
    bets = {}
    #start over
    start(coins, limit, bets)
"""
things to add.
1. way to remove bets
2. bot that will play roullete using martingale betting system
3. bot that will play advanced martingale betting system
4. a way to quit without killing the program
5. a way to spin without having to bet
things to fix.
1. the multi betting system
"""
if __name__ == '__main__':
    main()