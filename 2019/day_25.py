"""Advent of Code 2019 Day 25 - Cryostasis."""

from collections import defaultdict, deque
from itertools import combinations


class Droid:
    """Class for an ASCII-capable, intcode controlled Droid."""

    def __init__(self, code):
        """Initialises intcode (dict) and an input list."""
        self.code = code
        self.inputs = deque()
        self.outputs = ''
        self.pointer = 0

    def run_intcode(self):
        """Run intcode program on code."""
        relative_base = 0
        while True:
            opcode = self.code[self.pointer]

            if 99 < opcode <= 22210:
                opcode, modes = parse_instruction(opcode)
            else:
                modes = [0, 0, 0]

            if opcode == 99:   # halt
                return

            if modes[0] == 0:
                param_1 = self.code[self.pointer + 1]
            elif modes[0] == 1:
                param_1 = self.pointer + 1
            else:
                param_1 = self.code[self.pointer + 1] + relative_base

            if modes[1] == 0:
                param_2 = self.code[self.pointer + 2]
            elif modes[1] == 1:
                param_2 = self.pointer + 2
            else:
                param_2 = self.code[self.pointer + 2] + relative_base

            if modes[2] == 0:
                param_3 = self.code[self.pointer + 3]
            else:
                param_3 = self.code[self.pointer + 3] + relative_base

            if opcode == 1:   # addition
                self.code[param_3] = self.code[param_1] + self.code[param_2]
                self.pointer += 4

            elif opcode == 2:   # multiplication
                self.code[param_3] = self.code[param_1] * self.code[param_2]
                self.pointer += 4

            elif opcode == 3:   # input
                if self.inputs:
                    new_value = self.inputs.popleft()
                    self.code[param_1] = new_value
                    self.pointer += 2
                else:
                    yield "Waiting on input"

            elif opcode == 4:   # output
                self.pointer += 2
                output = chr(self.code[param_1])
                self.outputs += output
                if output == '\n':
                    to_yield = self.outputs
                    self.outputs = ''
                    yield to_yield

            elif opcode == 5:   # jump-if-true
                if self.code[param_1] == 0:
                    self.pointer += 3
                else:
                    self.pointer = self.code[param_2]

            elif opcode == 6:   # jump-if-false
                if self.code[param_1] != 0:
                    self.pointer += 3
                else:
                    self.pointer = self.code[param_2]

            elif opcode == 7:   # less than
                if self.code[param_1] < self.code[param_2]:
                    self.code[param_3] = 1
                else:
                    self.code[param_3] = 0
                self.pointer += 4

            elif opcode == 8:   # equals
                if self.code[param_1] == self.code[param_2]:
                    self.code[param_3] = 1
                else:
                    self.code[param_3] = 0
                self.pointer += 4

            elif opcode == 9:   # adjust relative base
                relative_base += self.code[param_1]
                self.pointer += 2

            else:
                print("Invalid or incorrectly parsed instruction.")
                return


def parse_instruction(value):
    """Return opcode and mode parsed from instruction value."""
    str_value = str(value)
    opcode = int(str_value[-2:])
    modes = [int(x) for x in list(str_value)[:-2]]
    while len(modes) != 3:
        modes.insert(0, 0)
    return (opcode, list(reversed(modes)))


def try_item_combos(droid, game):
    """Try all item combinations at the security office until success."""
    # Hypercube required or weight will be too light so never drop it
    items = [
        'pointer', 'coin', 'mug', 'manifold',
        'easter egg', 'astrolabe', 'candy cane'
    ]
    combos = combinations(items, 3)
    for combo in combos:
        for item in items:
            command = 'drop {}\n'.format(item)
            droid.inputs.extend([ord(x) for x in command])
        for item in combo:
            command = 'take {}\n'.format(item)
            droid.inputs.extend([ord(x) for x in command])
        command = 'east\n'
        droid.inputs.extend([ord(x) for x in command])

        while True:
            output = next(game)
            if output == 'Waiting on input':
                break
            print(output)


intcode_dict = defaultdict(int)
with open('input.txt') as f:
    i = 0
    for instruction in f.read().split(','):
        intcode_dict[i] = int(instruction)
        i += 1

# Solved manually (playing the game) with automation for the security room
# This automation is specific to my puzzle input
droid = Droid(intcode_dict)
game = droid.run_intcode()

while True:
    try:
        output = next(game)
        print(output)
        if output == 'Command?\n':
            command = input()
            if command == 'combos':
                try_item_combos(droid, game)
                continue
            command += '\n'
            droid.inputs.extend([ord(x) for x in command])
    except StopIteration:
        break
