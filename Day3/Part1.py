#!/usr/bin/env python3

import sys


def get_type_priority(item_type: str) -> int:
    if item_type[0].isupper():
        return ord(item_type[0]) - 38
    # must be lowercase
    return ord(item_type[0]) - 96


def priorities_sum(rucksacks: list[str]) -> int:

    sum = 0

    for ruck in rucksacks:

        # end of input
        if ruck == "\n":
            break

        # rucksack length check (must be even)
        ruck_len = len(ruck)
        # -1 is to account for new line char
        if (ruck_len - 1) % 2 != 0:
            print("Rucksack size is not even. Exiting...")
            sys.exit(1)

        compartment_size = ruck_len // 2
        type_set = set()

        # add each item type in the first compartment to the hashset
        for i in range(compartment_size):
            if not ruck[i].isalpha():
                print(f"Rucksack contains an invalid item type \"{ruck[i]}\". Exiting...")
                sys.exit(1)
            type_set.add(ruck[i])

        # iterate through the second compartment until we find *the* matching item type
        # then add the priority value to the sum
        for i in range(compartment_size, ruck_len):
            if ruck[i] in type_set:
                sum += get_type_priority(ruck[i])
                break

            if not ruck[i].isalpha():
                print(f"Rucksack contains an invalid item type \"{ruck[i]}\". Exiting...")
                sys.exit(1)

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

    print(priorities_sum(lines))


if __name__ == '__main__':
    main()
