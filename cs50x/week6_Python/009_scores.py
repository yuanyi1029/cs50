# Recreation of scores.c in week 2

from cs50 import get_int

# An empty list
scores = []

# Get integer input and append to list
for i in range(3):
    score = get_int("Score: ")
    scores.append(score)

# Calculate average
average = sum(scores) / len(scores)

print(f"Average: {average}")