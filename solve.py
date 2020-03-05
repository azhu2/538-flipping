#!/usr/bin/python

from __future__ import division
import argparse

class Solver:
    def __init__(self, iterations):
        self.row_count = int(iterations) + 1
        self.min_value = -2 * self.row_count
        self.max_value = self.row_count + 1

    def solve(self):
        # Init empty table of Nones
        self.data_table = [[None for _ in range(self.max_value - self.min_value + 1)] for _ in range(self.row_count + 1)]
        # Seed value for starting at 0
        self.data_table[0][self.__getIndexForValue(0)] = 1

        for value in range(self.min_value, self.max_value + 1):
            self.__getOrCalculateValue(self.row_count, value)

        self.results_table = []
        for row in range(self.row_count):
            win_count = self.__get_win_count(row)
            total_possibilities = pow(2, row)
            win_ratio = win_count / total_possibilities

            self.results_table.append([row, win_count, total_possibilities, win_ratio])

    def __getOrCalculateValue(self, row, value):
        colIndex = self.__getIndexForValue(value);

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
                    contributions.append(self.__getOrCalculateValue(row - 1, value - 2))
                # Coin A - contributions from range(1..) map to range(2..)
                if value >= 2:
                    contributions.append(self.__getOrCalculateValue(row - 1, value - 1))
            # Right side contribution
            if value < self.max_value:
                # Coin B - contributions from range(..0) map to range(..-2)
                if value <= -2:
                    contributions.append(self.__getOrCalculateValue(row - 1, value + 2))
                # Coin B - contributions from range(1..) map to range(0..)
                if value >= 0:
                    contributions.append(self.__getOrCalculateValue(row - 1, value + 1))

        result = sum(contributions)
        self.data_table[row][colIndex] = result
        return result

    def __get_win_count(self, row):
        # Sum values in row from 1 to end
        return sum(self.data_table[row][self.__getIndexForValue(1):])

    # Convert column label to array column index
    def __getIndexForValue(self, value):
        return value - self.min_value

    def print_results(self, debug):
        if debug:
            self.__print_debug_table()

        # Variable width columns; log(2)(10) = 3.01, so this should be enough for any number of iterations we can handle
        width = int(self.row_count / 3) + 1
        print '-------------------- Results --------------------'
        print('{:>5} | {:>{width}} | {:>{width}} | {}'.format('Flips', 'Wins', 'Permutations', 'Win Ratio', width = width))
        for row in self.results_table:
            print('{:5d} | {:{width}d} | {:{width}d} | {:.4%}'.format(*row, width = width))

    def __print_debug_table(self):
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

def main(iterations, output_file, debug):
    solver = Solver(iterations)
    solver.solve()
    solver.print_results(debug)
    if output_file is not None:
        dump_results_to_file(solver.results_table, output_file)

def dump_results_to_file(results_table, output_file):
    with open(output_file, 'w') as f:
        f.write('Flips,Wins,Permutations,Win Ratio\n')
        for row in results_table:
            f.write(','.join(map(str, row)) + '\n')
        print('Results written to {}'.format(output_file))

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('iterations', help = 'number of coin flips')
    parser.add_argument('-o', '--output', help = 'output (csv) file')
    parser.add_argument('--debug', help = 'print table of permutations (not recommended for iterations > 15)', action = 'store_true')
    args = parser.parse_args()
    return args.iterations, args.output, args.debug

if __name__ == '__main__':
    args = parseArgs()
    main(*args);