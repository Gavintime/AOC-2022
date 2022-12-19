#!/usr/bin/env python3

import sys
from dataclasses import dataclass


@dataclass
class Position:
    # row
    x: int = 0
    # column
    y: int = 0


def simulate_rope(motion_list: list[str]) -> int:

    if len(motion_list) == 0:
        print("There are no motions given in the input. Exiting...")
        sys.exit(1)

    # hash set used to store unique position visits by the ropes tail
    # TODO: replace with something more space efficient such as a bit vector
    unique_positions: set[tuple[int,int]] = set()
    unique_positions.add((0,0))

    # position of the head and tail of the rope
    # start position 's' is 0,0
    head = Position()
    tail = Position()

    # simulate the rope, one motion at a time
    for motion in motion_list:

        # process input
        if len(motion) < 3 or \
           motion[0] not in ('U', 'D', 'L', 'R') or \
           motion[1] != ' ':
            print(f"The motion \"{motion}\" is invalid. Exitng....")
            sys.exit(1)

        # get step count
        step_count = 0
        try:
            step_count = int(motion[2:])
        except:
            print(f"Motion \"{motion}\" has an invalid step size. Exiting...")
            sys.exit(1)
        if step_count < 1:
            print(f"Motion \"{motion}\" has an invalid step size. Exiting...")
            sys.exit(1)

        # simulate the current motion, one step at a time
        for _ in range(step_count):

            # move head
            if motion[0] == 'U':
                head.x -= 1
            elif motion[0] == 'D':
                head.x += 1
            elif motion[0] == 'L':
                head.y -= 1
            elif motion[0] == 'R':
                head.y += 1

            # move tail
            # will always be a whole number between -2 and 2
            x_diff = head.x - tail.x
            y_diff = head.y - tail.y
            if abs(x_diff) > 1 or abs(y_diff) > 1:
                tail.x += min(max(x_diff, -1), 1)
                tail.y += min(max(y_diff, -1), 1)

            unique_positions.add((tail.x, tail.y))

    return len(unique_positions)


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

    print(simulate_rope(lines))


if __name__ == '__main__':
    main()
