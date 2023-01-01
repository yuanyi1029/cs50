
# -------------------------- Printing a row of question marks --------------------------
# Loop method
for i in range(4):
    # We can set the print function to end with anything by specifying the end parameter
    # This technique can be found from the print function documentation
    print("?", end="")
print()

print("---------------------------------------")

# Print method with multiplication
print("?" * 4)

print("---------------------------------------")

# ------------------------------ Printing a 3 x 3 block -------------------------------
# Nested loop method
for i in range(3):
    for j in range(3):
        print("#", end="")
    print()

print("---------------------------------------")

# Print method with multiplication
for i in range(3):
    print("#" * 3)

print("---------------------------------------")