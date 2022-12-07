#!/usr/bin/env python3

import sys


def count_calories(cal_list: list[str]) -> list[int]:

    top_three_cals = [0, 0, 0]
    current_cal = 0

    for line in cal_list:

        if line == '\n':

            # get smallest elem index of the top 3 so far,
            # and replace it with the current cal count (if it's larger)
            index = top_three_cals.index(min(top_three_cals))
            top_three_cals[index] = max(top_three_cals[index], current_cal)
            current_cal = 0

        else:
            try:
                current_cal += int(line)
            except:
                print(f"Invalid calorie count {line}")
                sys.exit(1)

    return top_three_cals


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

    top_three = count_calories(lines)
    answer = 0
    for cal in top_three:
        answer += cal

    print(answer)


if __name__ == '__main__':
    main()
