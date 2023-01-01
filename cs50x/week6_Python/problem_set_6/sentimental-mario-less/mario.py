# TODO

# Recreation of mario.c in problem set 1
from cs50 import get_int

# Get user input for height
height = -1
while (height < 1 or height > 8):
    height = get_int("Height: ")

# Loops through each row
for i in range(1, height + 1):
    for j in range(1, height + 1):
        # Loops through each character in a row, determines to print a hash or a space
        if j > height - i:
            print("#", end="")
        else:
            print(" ", end="")
    print("")


