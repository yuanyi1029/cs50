# TODO

# Recreation of cash.c in problem set 1
from cs50 import get_float


def main():
    cents = get_cents()

    coins = 0

    # Repeat until cents is equal to 0, update cents and increase amount of coins
    while cents > 0:
        if cents >= 25:
            cents = cents - 25
            coins += 1
        elif cents >= 10:
            cents = cents - 10
            coins += 1
        elif cents >= 5:
            cents = cents - 5
            coins += 1
        elif cents >= 1:
            cents = cents - 1
            coins += 1

    print(coins)


# Function to get change in decimal and convert it to amount of cents
def get_cents():
    cents = -1
    while (cents < 0):
        change = get_float("Change owed: ")
        cents = round(change * 100)
    return cents


main()
