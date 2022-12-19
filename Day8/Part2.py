#!/usr/bin/env python3

import sys

# TODO: find solution better than O(n^2) time

def get_highest_scenic_score(trees: list[str]) -> int:

    # get grid size
    row_count = len(trees)
    if row_count < 1:
        print("Invalid grid. Exiting...")
        sys.exit(1)
    col_count = len(trees[0])
    if col_count < 1:
        print("Invalid grid. Exiting...")
        sys.exit(1)

    highest_score = 0

    # iterate through each tree, calculating scenic score
    for x in range(row_count):
        for y in range(col_count):

            current_score = 1
            temp_count = 0

            # looking left
            for i in range(y - 1, -1, -1):
                temp_count += 1
                if trees[x][y] <= trees[x][i]:
                    break
            if temp_count > 0:
                current_score *= temp_count
            temp_count = 0

            # looking right
            for i in range(y + 1, col_count):
                temp_count += 1
                if trees[x][y] <= trees[x][i]:
                    break
            if temp_count > 0:
                current_score *= temp_count
            temp_count = 0

            # looking up
            for i in range(x - 1, -1, -1):
                temp_count += 1
                if trees[x][y] <= trees[i][y]:
                    break
            if temp_count > 0:
                current_score *= temp_count
            temp_count = 0

            # looking down
            for i in range(x + 1, row_count):
                temp_count += 1
                if trees[x][y] <= trees[i][y]:
                    break
            if temp_count > 0:
                current_score *= temp_count
            temp_count = 0

            highest_score = max(current_score, highest_score)

    return highest_score



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


    print(get_highest_scenic_score(lines))


if __name__ == '__main__':
    main()
