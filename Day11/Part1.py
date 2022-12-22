#!/usr/bin/env python3

from __future__ import annotations
import sys
from collections import deque
from dataclasses import dataclass


class Monkey:

    @dataclass
    class Test:
        condition: int
        true_monkey: int
        false_monkey: int

    def __init__(self,
                 items: deque[int],
                 operation: tuple[str, str, str],
                 test: Monkey.Test):
        self.items: deque[int] = items
        self.operation: tuple[str, str, str] = operation
        self.test: Monkey.Test = test

    # inspect (pop) current item, do the inspect operation, floor divide by 3,
    # then return the item and a number representing which monkey it should be
    # thrown to based on divisibility condition
    def inspect_test_throw(self) -> tuple[int, int]:

        item = self.items.popleft()

        # set operation operands
        left_operand = 0
        right_operand = 0
        if self.operation[0] == 'old':
            left_operand = item
        else:
            left_operand = int(self.operation[0])
        if self.operation[2] == 'old':
            right_operand = item
        else:
            right_operand = int(self.operation[2])

        # apply the inspection operation
        if self.operation[1] == '+':
            item = left_operand + right_operand
        # operator must be *
        else:
            item = left_operand * right_operand

        # apply relief floor division
        item //= 3

        # conduct the monkeys test to find the target monkey for the throw
        # the test is always a divisibility test
        target_monkey = 0
        if item % self.test.condition == 0:
            target_monkey = self.test.true_monkey
        else:
            target_monkey = self.test.false_monkey

        return (item, target_monkey)



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
