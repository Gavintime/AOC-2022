#!/usr/bin/env python3

import sys

# returns the 1 based index of the end of the first "start of packet marker"
# in the input
# a start of packet marker is defined as sequence of 4 characters that are
# all diferent
def find_marker(signal: str) -> int:

    index = -1

    for i in range(len(signal) - 3):
        if signal[i] not in (signal[i+1], signal[i+2], signal[i+3]) and \
           signal[i+1] not in (signal[i+2], signal[i+3]) and \
           signal[i+2] != signal[i+3]:
            index = i + 3
            break

    if index == -1:
        print("Signal contains no start of packet marker. Exiting...")
        sys.exit(1)

    return index + 1


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

    print(find_marker(lines[0]))


if __name__ == '__main__':
    main()
