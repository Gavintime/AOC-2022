#!/usr/bin/env python3

import sys


def strategy_score(strat_list: list[str]) -> int:

    score = 0

    for strat in strat_list:

        # empty line means end of input
        if strat == '\n':
            break

        # input validation
        if len(strat) not in (3, 4) or \
            strat[0] not in ('A', 'B', 'C') or \
            strat[1] != ' ' or \
            strat[2] not in ('X', 'Y', 'Z'):
            print(f"Invalid strategy: {strat}. Exiting...")
            sys.exit(1)

        # value from outcome
        score += 3 * (ord(strat[2]) - ord('X'))

        # value from shape played
        score += (ord(strat[0]) - ord('A') + ((ord(strat[2]) - ord('X') + 2) % 3)) % 3 + 1



    return score


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

    score = strategy_score(lines)

    print(score)



if __name__ == '__main__':
    main()
