from cs50 import get_string

print("hello world!")

answer = get_string("What's your name? ")

# String concatenation
print("hello, " + answer)
print("hello,", answer)
# String formatting
print(f"hello, {answer}")
