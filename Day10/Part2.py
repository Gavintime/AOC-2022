#!/usr/bin/env python3

import sys


def process_crt(insts: list[str]) -> list[list[bool]]:

    if insts is None or len(insts) < 110:
        print("Invalid input given, input must contain atleast 110 instructions")
        sys.exit(1)

    # build empty crt screen
    crt_screen: list[list[bool]] = []
    for i in range(6):
        crt_screen.append([])
        for _ in range(40):
            crt_screen[i].append(False)

    # process the instructions
    x_register = 1
    cycle_count = 0
    v_value = 0
    addx_processing = False
    inst_index = 0
    while True:

        # draw pixel to crt
        if (cycle_count % 40) in range(x_register - 1, x_register + 2):
            crt_screen[cycle_count // 40][cycle_count % 40] = True

        cycle_count += 1

        if addx_processing:
            x_register += v_value
            addx_processing = False
            inst_index += 1

        elif insts[inst_index] == 'noop':
            inst_index += 1

        elif insts[inst_index][:5] == 'addx ':
            try:
                v_value = int(insts[inst_index][5:])
            except:
                print(f"Invalid v value given in the instruction \"{insts[inst_index]}\". Exiting...")
                sys.exit(1)
            addx_processing = True

        else:
            print(f"Invalid instruction \"{insts[inst_index]}\". Exiting...")
            sys.exit(1)

        if inst_index >= len(insts):
            break

    return crt_screen


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
    # remove \n from each input line
    for i in range(len(lines)):
        lines[i] = lines[i].rstrip()

    crt = process_crt(lines)
    for row in crt:
        for pixel in row:
            if pixel:
                print('#', end='')
            else:
                print(' ', end='')
        print()


if __name__ == '__main__':
    main()
