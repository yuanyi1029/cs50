# Recreation of status.c in week 2

import sys

# sys.exit() is function from sys module that returns a number which acts as the exit status
# use 'echo $?' after executing this program to view the exit status
if len(sys.argv) != 2:
    print("Missing command-line argument")
    sys.exit(1)

print(f"hello, {sys.argv[1]}")
sys.exit(0)

