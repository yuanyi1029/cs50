s = set()

s.add(1)
s.add(2)
s.add(3)
s.add(4)

# This will not add another 3 into the set because it already exists
s.add(3)

s.remove(2)
print(s)
print(f"The set has {len(s)} elements.")