# TODO

# Recreation of readability.c in problem set 2
from cs50 import get_string


def main():
    # Get user text input
    text = get_string("Text: ")

    letters = 0
    words = 0
    sentences = 0

    # Count number of letters, words, and sentences
    for char in text:
        if char.isalpha():
            letters += 1
        if char == " ":
            words += 1
        if char == "." or char == "?" or char == "!":
            sentences += 1
    words += 1

    # Determine Grade
    lettersper100words = letters / words * 100
    sentencesper100words = sentences / words * 100
    grade = 0.0588 * lettersper100words - 0.296 * sentencesper100words - 15.8

    # Print out the grade
    if grade < 1:
        print("Before Grade 1")
    elif grade > 16:
        print("Grade 16+")
    else:
        print(f"Grade {round(grade)}")


main()