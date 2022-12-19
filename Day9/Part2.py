#!/usr/bin/env python3

import sys
from dataclasses import dataclass


@dataclass
class Position:
    # row
    x: int = 0
    # column
    y: int = 0


def simulate_rope(motion_list: list[str], knot_count) -> int:

    if knot_count < 2:
        print("The rope must have at least 2 knots. Exiting...")
        sys.exit(1)

    if len(motion_list) == 0:
        print("There are no motions given in the input. Exiting...")
        sys.exit(1)

    # hash set used to store unique position visits by the ropes tail
    # TODO: replace with something more space efficient such as a bit vector
    unique_positions: set[tuple[int,int]] = set()
    unique_positions.add((0,0))

    # state of the rope as a list of knot positions
    # 0 index is the head
    # start position 's' is 0,0
    rope_knots: list[Position] = []
    for _ in range(knot_count):
        rope_knots.append(Position())

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
                rope_knots[0].x -= 1
            elif motion[0] == 'D':
                rope_knots[0].x += 1
            elif motion[0] == 'L':
                rope_knots[0].y -= 1
            elif motion[0] == 'R':
                rope_knots[0].y += 1

            # move body
            for i in range(1, knot_count):
                x_diff = rope_knots[i-1].x - rope_knots[i].x
                y_diff = rope_knots[i-1].y - rope_knots[i].y
                if abs(x_diff) > 1 or abs(y_diff) > 1:
                    rope_knots[i].x += min(max(x_diff, -1), 1)
                    rope_knots[i].y += min(max(y_diff, -1), 1)

            unique_positions.add((rope_knots[knot_count-1].x, rope_knots[knot_count-1].y))

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

    print(simulate_rope(lines, 10))


if __name__ == '__main__':
    main()
