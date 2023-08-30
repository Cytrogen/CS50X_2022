import csv
import sys


def main():
    # TODO: Check for command-line usage
    # if len(sys.argv) != 3:
    #     print("Usage: python dna.py data.csv sequence.txt")
    #     exit(1)

    # TODO: Read database file into a variable
    # Open data.csv
    with open(f"{sys.argv[1]}", "r") as databaseFile:
        reader = csv.reader(databaseFile)
        # Read the first line
        # ['name', 'AGATC', 'AATG', 'TATC']
        rowOne = next(reader)
        del rowOne[0]
        # Read the file into a list
        # [['Alice', '2', '8', '3'], ['Bob', '4', '1', '5'], ['Charlie', '3', '2', '5']]
        database = list(reader)

        # print(rowOne)
        # print(database)

    # TODO: Read DNA sequence file into a variable
    # Open sequence.txt
    with open(f"{sys.argv[2]}", "r") as sequenceFile:
        # Read the file into a string
        sequence = sequenceFile.read()
        # print(sequence)

    # TODO: Find longest match of each STR in DNA sequence
    count = 0
    n = []
    # i = subsequence
    for i in rowOne:
        count += 1
        point = 0
        # n = longest match of subsequence in sequence
        # [4, 1, 5]
        n.append(longest_match(sequence, i))
    # print(f"n: {n}")
    # print()

    # TODO: Check database for matching profiles
    # Get a list of subsequences under a person
    for i in database:
        point = 0
        m = []
        for j in range(1, len(i)):
            # print(i[j])
            m.append(int(i[j]))
        # print(m)

        # Compare two lists
        # for j in n:
        #     for k in m:
        #         print(f'{j} and {k}')
        #         if (j == k):
        #             point += 1
        #             print(f'point: {point}')
        #             if point == (len(i) - 1):
        #                 print(i[0])
        #                 exit(0)
        #             else:
        #                 pass
        #             break

        # Compare two lists
        if n == m:
            print(i[0])
            exit(0)
        # print()

    print('No match')
    # return


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