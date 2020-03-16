from random import Random

def run():
    if Random.randint(0, 1) == 1:
        print('It is Heads!')
    else:
        print('It is Tails!')