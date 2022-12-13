#!/usr/bin/env python3

import sys


def get_assignment(assignment_string: str) -> list[int]:
    pass


def get_assignment_pair(pair_string: str) -> list[int]:

    # starts as strings, converted to ints during parsing
    pair_list: list[int] = ['', '', '', '']

    pair_index = 0

    for c in pair_string[:-1]:

        if c.isnumeric():
            pair_list[pair_index] += c
        elif c == '-' and pair_index == 0:
            pair_list[pair_index] = int(pair_list[pair_index])
            pair_index = 1
        elif c == ',' and pair_index == 1:
            pair_list[pair_index] = int(pair_list[pair_index])
            pair_index = 2
        elif c == '-' and pair_index == 2:
            pair_list[pair_index] = int(pair_list[pair_index])
            pair_index = 3
        else:
            print(f"Assignment pair \"{pair_string}\" formatting is invalid. Exiting...")
            sys.exit(1)

    if pair_list[3] == '':
        print(f"Assignment pair \"{pair_string}\" formatting is invalid. Exiting...")
        sys.exit(1)

    pair_list[3] = int(pair_list[3])

    return pair_list



def count_fully_contained_assignments(assignments_pairs: list[str]) -> int:

    if len(assignments_pairs) < 1:
        print("There must be at least one assingment pair, none were found. Exiting...")
        sys.exit(1)

    fully_contained_count = 0

    for pair_string in assignments_pairs:
        # pair = assignment,assignment
        # assignment = number-number
        # number = 1 or more digits
        pair_ints = get_assignment_pair(pair_string)

        if (pair_ints[0] <= pair_ints[2] and pair_ints[1] >= pair_ints[3]) or \
           (pair_ints[2] <= pair_ints[0] and pair_ints[3] >= pair_ints[1]):
            fully_contained_count += 1

    return fully_contained_count



def main():

    # get filename
    if len(sys.argv) != 2:
        print("Incorrect number of inputs. Please enter a filename.")
        sys.exit(1)
    filename = sys.argv[1]

    lines: list[str]

    # read in input file as list of str lines
    try:
        with open(filename) as file:
            # the sublist index removes the always empty last line
            lines = file.readlines()
    except :
        print(f"Error trying to open {filename}. Exiting")
        sys.exit(1)

    print(count_fully_contained_assignments(lines))


if __name__ == '__main__':
    main()
