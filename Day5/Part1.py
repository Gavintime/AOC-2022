#!/usr/bin/env python3

import sys
from collections import deque

# returns a dict of deques parsed from input, as well as index of first instruction
def parse_crates(crates: list[list[str]]) -> list[dict[deque[str]] | int]:

    if len(crates[0]) < 3:
        print("Input does not start with a valid crate drawing. Exiting...")
        sys.exit(1)

    # get index of end of crate part of input (index of bottom of stack row)
    stack_label_index = 0
    while not crates[stack_label_index][1].isnumeric():
        if not (crates[stack_label_index][1].isalpha() or crates[stack_label_index][1] == ' '):
            print("Input does not start with a valid crate drawing. Exiting...")
            sys.exit(1)
        stack_label_index += 1

    # create deque for each crate stack, storing in a hash map
    stack_map: dict[str, deque] = {}

    for i in range(1, len(crates[stack_label_index]), 4):
        if crates[stack_label_index][i] in stack_map:
            print(f"Crate drawing has duplicate stack names for {crates[stack_label_index][i]}. Exiting...")
            sys.exit(1)
        stack_map[crates[stack_label_index][i]] = deque()

    # add stacked crates to their respective deque
    current_level = stack_label_index - 1

    while current_level >= 0:
        for i in range(1, len(crates[current_level]), 4):
            if crates[current_level][i] == ' ':
                continue
            if not crates[current_level][i].isalpha():
                print(f"Crate drawing has invalid crate value {crates[current_level]}. Exiting...")
                sys.exit(1)
            stack_map[crates[stack_label_index][i]].append(crates[current_level][i])
        current_level -= 1

    return [stack_map, stack_label_index + 2]


def process_instructions(stack_map: dict[deque[str]], instructions: list[str]) -> str:

    for inst in instructions:

        if inst[0:5] != 'move ':
            print(f"Instruction {inst} does not follow correct format. Exiting...")
            sys.exit(1)

        # get crate count of instruction
        crate_count: int = ''
        inst_index = 5

        while inst[inst_index] != ' '


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

    stack_map, inst_index = parse_crates(lines)
    output = process_instructions(stack_map, lines[inst_index:])
    print(output)


if __name__ == '__main__':
    main()
