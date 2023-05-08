#import numpy as np
import random
import time

names = {0:"Rock", 1:"Paper", 2:"Scissors"}
rules = [0,1,2]

#def rng():
#    return np.random.default_rng(int(10000000*time.time()))

def validate_input(replay):
    actions = {
        0: False,
        1: 1,
        2: 2,
        3: 3
    }
    if replay in actions:
        return actions[replay]
    else:
        return 5
    
def rps(user_choice):
    try:
        if user_choice==4:
            user_choice = int(input("1. Rock\n2. Paper\n3. Scissors\n\nGet\n Set\n  Go!\n"))
        print("Your choice:", names[user_choice-1])
        com_choice = random.choice(rules)
        print("Com's choice:", names[com_choice])
        if rules[user_choice-2] == com_choice:
            print("You Win!")
        elif user_choice-1 == com_choice:
            print("Draw!")
        else:
            print("You Lose!")
        replay = int(input("Enter your choice to play again, or enter 0 to exit\n"))
        return validate_input(replay)
    except:
        try:
            user_choice = int(input("Entered value is invalid. Valid values are 1, 2 and 3.\nTry again or enter 0 to exit\n"))
            return validate_input(user_choice)
        except:
            return 5
        
def play_game():
    replay = 4
    while(replay):
        replay = rps(replay)

play_game()