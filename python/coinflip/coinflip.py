from random import Random

def run():
    random = Random()
    if random.randint(0, 1) == 1:
        result = 'heads'
    else:
        result = 'tails'
    print(result)

if __name__ == '__main__':
    run()