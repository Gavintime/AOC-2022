#!/usr/bin/env python3

import sys


def count_visible_trees(trees: list[str]) -> int:

    # get grid size
    row_count = len(trees)
    if row_count < 1:
        print("Invalid grid. Exiting...")
        sys.exit(1)
    col_count = len(trees[0])
    if col_count < 1:
        print("Invalid grid. Exiting...")
        sys.exit(1)

    # store coords of known visible trees in a hash set
    # border trees will not be stored
    visible_trees: set[tuple[int,int]] = set()

    # start with the size of the grid border
    # all trees along the border are always visible
    tree_count = 2 * row_count + 2 * (col_count - 2)

    # count visible trees viewed from the left and right side of grid
    # skip the first and last row, as they are always visible
    for x in range(1, row_count - 1):

        # left to right
        highest_tree_left = trees[x][0]
        if highest_tree_left != 9:
            # skip first and last trees as they are always visible
            for y in range(1, col_count - 1):

                if trees[x][y] > highest_tree_left:

                    # this check is useless for the first direction we check
                    # as no trees have been known to be visible at this point
                    # if (x,y) not in visible_trees:
                    tree_count += 1
                    visible_trees.add((x,y))

                    highest_tree_left = trees[x][y]
                    if highest_tree_left == 9:
                        break

        # right to left
        highest_tree_right = trees[x][col_count - 1]
        if highest_tree_right != 9:
            # the extra -1 is to account for it being inclusive, compared to the above for loop
            for y in range((col_count - 1) -1, 0, -1):
                if trees[x][y] > highest_tree_right:
                    if (x,y) not in visible_trees:
                        tree_count += 1
                        visible_trees.add((x,y))
                    highest_tree_right = trees[x][y]
                    if highest_tree_right == 9:
                        break

    # same as above, but now looking from top and bottom
    for y in range(1, col_count - 1):

        # top to down
        highest_tree_top = trees[0][y]
        if highest_tree_top != 9:
            for x in range(1, row_count - 1):

                if trees[x][y] > highest_tree_top:

                    if (x,y) not in visible_trees:
                        tree_count += 1
                        visible_trees.add((x,y))

                    highest_tree_top = trees[x][y]
                    if highest_tree_top == 9:
                        break

        # down to top
        highest_tree_down = trees[row_count - 1][y]
        if highest_tree_down != 9:
            for x in range((row_count - 1) -1, 0, -1):
                if trees[x][y] > highest_tree_down:
                    if (x,y) not in visible_trees:
                        tree_count += 1
                        visible_trees.add((x,y))
                    highest_tree_down = trees[x][y]
                    if highest_tree_down == 9:
                        break

    return tree_count


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

    answer = count_visible_trees(lines)
    print(answer)


if __name__ == '__main__':
    main()
