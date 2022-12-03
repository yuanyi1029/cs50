# Recreation of swap.c in week 4

x = 1
y = 2

print(f"x is {x}, y is {y}")
# Swapping variables without using temporary variables
x, y = y, x
print(f"x is {x}, y is {y}")