# Similar to search.c in week 3

import sys

names = ["Bill", "Charlie", "Fred", "George", "Ginny", "Percy", "Ron"]

name = input("Name: ")

if name in names:
    print("Found")
    sys.exit(0)

print("Not found")
sys.exit(1)