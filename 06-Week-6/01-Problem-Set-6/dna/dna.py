import csv
import sys


def main():
    DNA_bases = []
    subsequences_dict = {}

    # Check for command-line usage
    if len(sys.argv) < 3:
        print("Usage: python dna.py *.csv *.txt")
        sys.exit(1)

    # Read database file into a variable
    with open(sys.argv[1], 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            DNA_bases.append(row)

    # Read DNA sequence file into a variable
    with open(sys.argv[2], 'r') as file:
        dna_sequence = file.read()

    # List of subsequences to check
    subsequences = list(DNA_bases[0].keys())[1:]

    # TODO: Find longest match of each STR in DNA sequence
    for subsequence in subsequences:
        subsequences_dict[subsequence] = longest_match(dna_sequence, subsequence)

    # TODO: Check database for matching profiles
    for person_data in DNA_bases:
        profile_match = 0
        for subsequence in subsequences:
            if int(person_data[subsequence]) == subsequences_dict[subsequence]:
                profile_match += 1

            if profile_match == len(subsequences):
                print(person_data["name"])
                return

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
