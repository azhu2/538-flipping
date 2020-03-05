#!/usr/bin/python

from __future__ import division
import argparse

class Solver:
    def __init__(self, iterations):
        self.row_count = int(iterations) + 1
        self.min_value = -2 * self.row_count
        self.max_value = self.row_count + 1

        # Init empty table of Nones
        self.data_table = [[None for _ in range(self.max_value - self.min_value + 1)] for _ in range(self.row_count + 1)]
        # Seed value for starting at 0
        self.data_table[0][self.getIndexForValue(0)] = 1

    def populate_table(self):
        for value in range(self.min_value, self.max_value + 1):
            self.getOrCalculateValue(self.row_count, value)

    def getOrCalculateValue(self, row, value):
        colIndex = self.getIndexForValue(value);

        curValue = self.data_table[row][colIndex]
        if curValue is not None:
            return curValue

        contributions = []

        # Edge case; row 0 is all 0 except for seed value
        if row != 0:
            # Left side contribution
            if value > self.min_value + 1:
                # Coin B - contributions from range(..0) map to range(..2)
                if value <= 2:
                    contributions.append(self.getOrCalculateValue(row - 1, value - 2))
                # Coin A - contributions from range(1..) map to range(2..)
                if value >= 2:
                    contributions.append(self.getOrCalculateValue(row - 1, value - 1))
            # Right side contribution
            if value < self.max_value:
                # Coin B - contributions from range(..0) map to range(..-2)
                if value <= -2:
                    contributions.append(self.getOrCalculateValue(row - 1, value + 2))
                # Coin B - contributions from range(1..) map to range(0..)
                if value >= 0:
                    contributions.append(self.getOrCalculateValue(row - 1, value + 1))

        result = sum(contributions)
        self.data_table[row][colIndex] = result
        return result

    # Convert column label to array column index
    def getIndexForValue(self, value):
        return value - self.min_value

    def print_results(self, debug):
        if debug:
            self.print_debug_table()

        print '-------------------- Results --------------------'
        print('{:>5} | {:>32} | {:>32} | {}'.format('Flips', 'Wins', 'Permutations', 'Win Ratio'))
        for row in range(self.row_count):
            win_count = self.get_win_count(row)
            total_possibilities = pow(2, row)
            win_ratio = win_count / total_possibilities

            print('{:5d} | {:32d} | {:32d} | {:.4%}'.format(row, win_count, total_possibilities, win_ratio))

    def print_debug_table(self):
        print '-------------------- Debug Table --------------------'
        print 'Flips | ',
        for col_label in range(self.min_value, self.max_value + 1):
            print '{:4d}'.format(col_label),
        print
        for row_num, row in enumerate(self.data_table):
            print '{:5d} | '.format(row_num),
            for item in row:
                print '{:4d}'.format(item),
            print
        print '\n'

    def get_win_count(self, row):
        # Sum values in row from 1 to end
        return sum(self.data_table[row][self.getIndexForValue(1):])

def main(iterations, debug):
    solver = Solver(iterations)
    solver.populate_table()
    solver.print_results(debug)

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('iterations', help = 'number of coin flips')
    parser.add_argument('--debug', help = 'print table of permutations (not recommended for iterations > 15)', action = 'store_true')
    args = parser.parse_args()
    return args.iterations, args.debug

if __name__ == '__main__':
    args = parseArgs()
    main(*args);