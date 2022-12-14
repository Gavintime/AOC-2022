#!/usr/bin/env python3

import sys
from collections import deque


# TODO: allow for multi digit/non numerical stack names


# returns a dict of deques parsed from input, as well as index of first instruction
def parse_crates(crates: list[str]) -> tuple[dict[str,deque[str]],int]:

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

    return (stack_map, stack_label_index + 2)


# returns the first number of the given string, terminated by a space
# also returns the index directly after the terminating space
def get_number(input: str) -> tuple[int, int]:

    # get crate count of instruction
    number = ''
    index = 0
    while input[index] != ' ':
        if not input[index].isnumeric():
            print(f"Instruction starting at \"{input}\" does not follow correct format. Exiting...")
            sys.exit(1)
        number += input[index]
        index += 1

    return (int(number), index + 1)


def parse_instructions(stack_map: dict[str,deque[str]], inst_raw: list[str]) -> list[tuple[int,str,str]]:

    inst_list: list[tuple[int,str,str]] = []


    for inst in inst_raw:

        if inst == '\n':
            break

        inst = inst[:-1]

        crate_count: int
        source_stack: str
        dest_stack: str

        if len(inst) < 18 or inst[0:5] != 'move ':
            print(f"Instruction \"{inst}\" does not follow correct format. Exiting..1.")
            sys.exit(1)

        # get crate count of instruction, index 5 must be the index of the left
        # most digit of the the crate size
        inst_index = 5
        crate_count, temp_index = get_number(inst[inst_index:])
        inst_index += temp_index


        if inst[inst_index:inst_index+5] != 'from ':
            print(f"Instruction \"{inst}\" does not follow correct format. Exiting...2")
            sys.exit(1)

        # get name (digit) of the source/destination crate stacks
        inst_index += 5
        source_stack = inst[inst_index]
        if inst[inst_index+1:inst_index+5] != ' to ':
            print(f"Instruction \"{inst}\" does not follow correct format. Exiting...3")
            sys.exit(1)
        dest_stack = inst[inst_index+5]

        inst_list.append((crate_count, source_stack, dest_stack))

    return inst_list


def process_instruction(stack_map: dict[str,deque[str]], inst_list: list[tuple[int,str,str]]) -> str:

    answer = ''

    for inst in inst_list:
        # pop/push as many times as the instruction says
        # now with simulating multi crate movement by using a temporary stack

        temp_stack = deque()
        for _ in range(inst[0]):
            temp_stack.append(stack_map[inst[1]].pop())
        for _ in range(inst[0]):
            stack_map[inst[2]].append(temp_stack.pop())

    # add the top value of each stack to the answer and return
    # TODO: handle empty stacks?
    for i in range(1, len(stack_map) + 1):
        answer += stack_map[str(i)][-1]
    return answer


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
    inst_list = parse_instructions(stack_map, lines[inst_index:])
    answer = process_instruction(stack_map, inst_list)
    print(answer)


if __name__ == '__main__':
    main()
