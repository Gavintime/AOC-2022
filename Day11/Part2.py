#!/usr/bin/env python3

from __future__ import annotations
import sys
from collections import deque
from dataclasses import dataclass
from heapq import nlargest


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
        self.inspect_count: int = 0
        self.limiter = 1

    def __str__(self) -> str:
        print_string = "Monkey x:\n  Starting items: "
        print_string += str(self.items)
        print_string += "\n  Operation: new = "
        print_string += str(self.operation)
        print_string += "\n  Test: divisible by "
        print_string += str(self.test.condition)
        print_string += "\n    If true: throw to monkey "
        print_string += str(self.test.true_monkey)
        print_string += "\n    If false: throw to monkey "
        print_string += str(self.test.false_monkey)
        return print_string

    # inspect (pop) current item, do the inspect operation,
    # then return the item and a number representing which monkey it should be
    # thrown to based on divisibility condition
    # also increments inspect count
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

        item %= self.limiter
        # item = item % self.limiter

        # conduct the monkeys test to find the target monkey for the throw
        # the test is always a divisibility test
        target_monkey = 0
        if item % self.test.condition == 0:
            target_monkey = self.test.true_monkey
        else:
            target_monkey = self.test.false_monkey

        self.inspect_count += 1

        return (item, target_monkey)


# parse the given input and return a list of monkey objects
# the monkeys index in the list coorisponds to it's ID
def parse_monkeys(monkey_strs: list[str]) -> list[Monkey]:

    if monkey_strs is None or len(monkey_strs) < 13:
        print("Invalid input given. Input must contain at least 2 monkeys. Exiting...")
        sys.exit(1)

    # parse monkeys one at a time
    monkey_list: list[Monkey] = []
    for i in range(0, len(monkey_strs), 7):

        # verify monkey header and starting items header
        if monkey_strs[i] != f'Monkey {i // 7}:':
            print(f"Invalid monkey header \"{monkey_strs[i]}\". Exiting...")
            print(f'Monkey {i % 7}:')
            print(i)
            sys.exit(1)
        items_header = '  Starting items: '
        if monkey_strs[i+1][:len(items_header)] != items_header:
            print(f"Invalid starting items \"{monkey_strs[i+1]}\" for monkey {i}. Exiting...")
            sys.exit(1)

        # parse starting items
        monkey_items: deque[int] = deque()
        for item in monkey_strs[i+1][len(items_header):].split(', '):
            try:
                monkey_items.append(int(item))
            except:
                print(f"Invalid starting items \"{monkey_strs[i+1]}\" for monkey {i}. Exiting...")
                sys.exit(1)

        # verify operation header
        operation_header = '  Operation: new = '
        if monkey_strs[i+2][:len(operation_header)] != operation_header:
            print(f"Invalid operation \"{monkey_strs[i+2]}\" for monkey {i}. Exiting...")
            sys.exit(1)

        # verify and parse operation operands and operator
        operation = tuple(monkey_strs[i+2][len(operation_header):].split())
        if len(operation) != 3 or \
           (operation[0] != 'old' and not operation[0].isnumeric()) or \
           (operation[2] != 'old' and not operation[2].isnumeric()) or \
           operation[1] not in ('+', '*'):
            print(f"Invalid operation \"{monkey_strs[i+2]}\" for monkey {i}. Exiting...")
            print((operation[0] != 'old' or not operation[0].isnumeric()))
            sys.exit(1)

        # verify test header
        test_header = '  Test: divisible by '
        if monkey_strs[i+3][:len(test_header)] != test_header:
            print(f"Invalid test \"{monkey_strs[i+3]}\" for monkey {i}. Exiting...")
            sys.exit(1)

        # parse test operand
        test_operand = 0
        try:
            test_operand = int(monkey_strs[i+3][len(test_header):])
        except:
            print(f"Invalid test \"{monkey_strs[i+3]}\" for monkey {i}. Exiting...")
            sys.exit(1)

        # verify true and false test result headers
        true_header = '    If true: throw to monkey '
        if monkey_strs[i+4][:len(true_header)] != true_header:
            print(f"Invalid test true result \"{monkey_strs[i+4]}\" for monkey {i}. Exiting...")
            sys.exit(1)
        false_header = '    If false: throw to monkey '
        if monkey_strs[i+5][:len(false_header)] != false_header:
            print(f"Invalid test false result \"{monkey_strs[i+5]}\" for monkey {i}. Exiting...")
            sys.exit(1)

        # parse test result monkey IDs
        true_monkey = 0
        try:
            true_monkey = int(monkey_strs[i+4][len(true_header):])
        except:
            print(f"Invalid test true monkey \"{monkey_strs[i+4]}\" for monkey {i}. Exiting...")
            sys.exit(1)
        false_monkey = 0
        try:
            false_monkey = int(monkey_strs[i+5][len(false_header):])
        except:
            print(f"Invalid test true monkey \"{monkey_strs[i+5]}\" for monkey {i}. Exiting...")
            sys.exit(1)

        # verify monkey tail
        # len check is to skip tail check on last monkey since the last monkey
        # has no tail :(
        if (i+6) < len(monkey_strs) and monkey_strs[i+6] != '':
            print(f"Invalid monkey tail \"{monkey_strs[i+6]}\" for monkey {i}. Exiting...")
            sys.exit(1)

        # build the monkey and add the new monkey to the monkey list
        new_test = Monkey.Test(test_operand, true_monkey, false_monkey)
        new_monkey = Monkey(monkey_items, operation, new_test)
        monkey_list.append(new_monkey)

    return monkey_list


def assign_limiter(monkeys: list[Monkey]):

    conditions = []
    for monkey in monkeys:
        conditions.append(monkey.test.condition)

    my_num = 1
    for con in conditions:
        my_num *= con

    for monkey in monkeys:
        monkey.limiter = my_num

    return


def get_monkey_buisiness(monkeys: list[Monkey], rounds: int) -> int:

    # conduct the rounds one at a time
    for i in range(rounds):
        # print(f"Round {i+1}")
        # give each monkey a turn each round
        for monkey in monkeys:
            # let each monkey each round inspect and throw all their items
            # during their turn
            while len(monkey.items) > 0:
                thrown_item, target_monkey = monkey.inspect_test_throw()
                monkeys[target_monkey].items.append(thrown_item)

    # find the two most active monkeys and multiply their inspect counts together
    inspect_counts = []
    for monkey in monkeys:
        inspect_counts.append(monkey.inspect_count)
    two_largest = nlargest(2, inspect_counts)

    return two_largest[0] * two_largest[1]


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
        print(f"Error trying to open \"{filename}\". Exiting")
        sys.exit(1)
    # remove \n from each input line
    for i in range(len(lines)):
        lines[i] = lines[i].rstrip()


    monkeys = parse_monkeys(lines)
    # for monkey in monkeys:
    #     print(monkey)
    assign_limiter(monkeys)
    print(get_monkey_buisiness(monkeys, 10000))


if __name__ == '__main__':
    main()
