import csv
import sys


def main():

    # TODO: Check for command-line usage
    # Only allow 3 command line arguments
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # TODO: Read database file into a variable

    with open(sys.argv[1], "r") as file:
        # Read the database into a list of dictionaries using DictReader() and list() functions
        reader = csv.DictReader(file)
        db_dict = list(reader)
        # Read the first row of the database into a list as the DNA headers
        header_list = reader.fieldnames[1:]

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as file:
        # Read the DNA sequence into variable using .read() function
        dna_sequence = file.read()

    # TODO: Find longest match of each STR in DNA sequence

    # Create a dictionary to store the amount of consecutive DNA sequences
    dna_dict = {}
    for headers in header_list:
        consecutives = 0
        # Keep looping until a consecutive DNA is not found
        while headers * (consecutives + 1) in dna_sequence:
            consecutives += 1

        # Add the DNA consecutives into the dictionary
        dna_dict[headers] = consecutives

    # TODO: Check database for matching profiles
    found = False
    # Loop through the list of dictionaries, change match to False if the consecutive DNA does not match
    for i in range(len(db_dict)):
        match = True
        for headers in header_list:
            if dna_dict[headers] != int(db_dict[i][headers]):
                match = False

        # If everything matches, print out the name and change the found variable
        if match == True:
            found = True
            print(db_dict[i]["name"])

    # If not found through the entire database, print no match
    if found == False:
        print("No match")

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
