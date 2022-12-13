#!/usr/bin/env python3

import sys


def get_type_priority(item_type: str) -> int:
    if item_type[0].isupper():
        return ord(item_type[0]) - 38
    # must be lowercase
    return ord(item_type[0]) - 96


def badge_sum(rucksacks: list[str]) -> int:

    sum = 0

    # -1 accounts for empty line at end of input
    if (len(rucksacks)) % 3 != 0:
        print("The number of rucksacks is not a multiple of three. Exiting...")
        sys.exit(1)

    # iterate through each set of 3 rucksacks, adding the sum of each badge
    for i in range(0, len(rucksacks), 3):

        # build set of item types from the first rucksack
        type_set = set()

        for item_type in rucksacks[i][:-1]:
            if not item_type.isalpha():
                print(f"Rucksack contains an invalid item type \"{item_type}\". Exiting...")
                sys.exit(1)
            type_set.add(item_type)

        # find the matching item types in the second rugsack
        matching_types = set()
        for item_type in rucksacks[i+1][:-1]:
            if item_type in type_set:
                matching_types.add(item_type)
            elif not item_type.isalpha():
                print(f"Rucksack contains an invalid item type \"{item_type}\". Exiting...")
                sys.exit(1)

        if len(matching_types) == 0:
            print(f"The second rucksack in it's tri pair contains no matching item types with the first rucksack in the tri pair. Exiting...")
            sys.exit(1)

        # find the single matching item type in the third ruscksack
        badge_type = None
        for item_type in rucksacks[i+2][:-1]:
            if item_type in matching_types:
                badge_type = item_type
                break
            elif not item_type.isalpha():
                print(f"Rucksack contains an invalid item type \"{item_type}\". Exiting...")
                sys.exit(1)

        if badge_type is None:
            print(f"The third rucksack in it's tri pair contains no matching item types with the first and second rucksacks in the tri pair. Exiting...")
            sys.exit(1)

        sum += get_type_priority(badge_type)

    return sum


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
            lines = file.readlines()
    except :
        print(f"Error trying to open {filename}. Exiting")
        sys.exit(1)

    print(badge_sum(lines))


if __name__ == '__main__':
    main()
