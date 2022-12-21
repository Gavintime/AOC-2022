#!/usr/bin/env python3

import sys

def get_signal_strength_sum(insts: list[str]) -> int:


    if insts is None or len(insts) < 110:
        print("Invalid input given, input must contain atleast 110 instructions")
        sys.exit(1)

    # process the instructions
    signal_sum = 0
    x_register = 1
    cycle_count = 20
    v_value = 0
    addx_processing = False
    inst_index = 0
    while True:

        cycle_count += 1

        if (cycle_count) % 40 == 0:
            signal_stength = (cycle_count - 20) * x_register
            print(f"{cycle_count - 20} * {x_register} = {signal_stength}")
            signal_sum += signal_stength

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

        if inst_index >= len(insts) or (cycle_count - 20) > 220:
            break

    return signal_sum


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

    print(get_signal_strength_sum(lines))


if __name__ == '__main__':
    main()
