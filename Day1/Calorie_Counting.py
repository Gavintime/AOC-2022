#!/usr/bin/env python3

import sys


def count_calories(cal_list: list[str]) -> int:

    highest_cal = 0
    current_cal = 0

    for line in cal_list:

        if line == '\n':
            highest_cal = max(highest_cal, current_cal)
            current_cal = 0

        else:
            try:
                current_cal += int(line)
            except:
                print(f"Invalid calorie count {line}")
                sys.exit(1)

    return highest_cal


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

    answer = count_calories(lines)
    print(answer)


if __name__ == '__main__':
    main()
