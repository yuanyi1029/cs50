people = [
    {"name": "Harry", "house": "Gryffindor"},
    {"name": "Cho", "house": "Ravenclaw"},
    {"name": "Draco", "house": "Slytherin"},
]

def f(person):
    return person["name"]

# The lambda function does the same thing as the f() function
people.sort(key=lambda person: person["name"])
print(people) 