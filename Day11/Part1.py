#!/usr/bin/env python3

from __future__ import annotations
import sys
from collections import deque
from dataclasses import dataclass
from typing import Union



class Monkey:

    @dataclass
    class Test:
        condition: int
        true_monkey: int
        false_monkey: int

    def __init__(self,
                 items: deque[int],
                 operation: tuple[Union[str, int], str, Union[str, int]],
                 test: Monkey.Test):
        self.items: deque[int] = items
        self.operation: tuple[Union[str, int], str, Union[str, int]] = operation
        self.test: Monkey.Test = test

    # inspect (pop) current item, do the operation, divide by 3,
    # then return the item and a number representing which monkey it should be
    # thrown to
    def inspect_process(self) -> tuple[int, int]:

        item_and_target: tuple
        item_and_target = (0, 0)

        item = self.items.pop()




        return item_and_target



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
