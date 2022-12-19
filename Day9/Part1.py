#!/usr/bin/env python3

import sys


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


if __name__ == '__main__':
    main()
