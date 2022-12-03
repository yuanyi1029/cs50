# Recreation of phonebook.c in week 3

# Open a people dictionary
people = {
    "Carter": "+1-617-495-1000",
    "David": "+1-949-468-2750"
}

name = input("Name: ")

# Check if the input name is in the dictionary by checking each key in the dictionary
if name in people:
    # Determine the phone number of the input name by getting the value from the dictionary
    number = people[name]
    print(f"Number: {number}")

