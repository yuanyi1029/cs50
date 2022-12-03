# Recreation of agree.c in week 1

s = input("Do you agree? ")

# Original method:
if s == "Y" or s == "y":
    print("Agreed.")
elif s == "N" or s == "n":
    print("Not agreed.")

s = s.lower()

# Other method:
if s in ["y", "yes"]:
    print("Agreed.")
elif s in ["n", "no"]:
    print("Not agreed.")
