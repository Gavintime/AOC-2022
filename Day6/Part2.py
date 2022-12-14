#!/usr/bin/env python3

import sys

# returns the 1 based index of the end of the first "start of message marker"
# in the input
# a start of message marker is defined as sequence of 14 characters that are
# all diferent
def find_marker(signal: str) -> int:

    index = -1

    # iterate through potential message marker start points
    for i in range(len(signal) - 13):

        valid_point = True

        # compare the 14 next elements against each other
        for j in range(i, i + 14):
            if signal[j] in signal[j+1:i+14]:
                # skip redundant points
                i = j + 1
                valid_point = False
                break

        if valid_point:
            index = i + 13
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
