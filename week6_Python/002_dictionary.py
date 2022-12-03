# Recreation of the function in problem set 5 (dictionary.c)

# Sets are similar to dictionaries but each element are keys and have no values
words = set()

# Check if a word is in the words set
def check(word):
    if word.lower() in words:
        return True
    else:
        return False

# Loads a file, loop through it and add each word to the words set
def load(dictionary):
    file = open(dictionary, "r")
    for line in file:
        # rstrip() will remove then \n at the end of each line
        word = line.rstrip()
        words.add(word)
    file.close()
    return True

# Use len() function to get the length of a set
def size():
    return len(words)

# Unloading the used memory space is not needed in python
def unload():
    return True