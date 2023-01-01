# Recreation of greet.c in week 2

# We import argv from the sys module to accept command line arguments
from sys import argv


# This is just for reference to print each command line argument
for arg in argv:
    print(arg)

# Give a name as a command line argument and it will print hello, name
if len(argv) == 2:
    print(f"hello, {argv[1]}")
else:
    print("hello, world")
