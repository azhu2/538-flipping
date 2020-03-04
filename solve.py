#!/usr/bin/python

from __future__ import division
import sys

# TODO make flag
DEBUG = False

# TODO Ew globals
ROW_COUNT = 0
MIN_VALUE = 0
MAX_VALUE = 0

def main(argv = None):
    if argv is None:
        argv = sys.argv

    try:
        global ROW_COUNT
        ROW_COUNT = int(argv[1]) + 1
        # Columns go from -2 * ROW_COUNT to ROW_COUNT, use getIndexForValue() to convert from value to column index
        global MIN_VALUE
        MIN_VALUE = -2 * ROW_COUNT
        global MAX_VALUE
        MAX_VALUE = ROW_COUNT + 1
    except:
        sys.exit('Invalid or missing flip count')

    data_table = init_table()

    populateTable(data_table)

    if DEBUG:
        print_debug_table(data_table)

    # Print results
    print('\n\n{:>5} | {:>12} | {:>12} | {}'.format('Flips', 'Wins', 'Permutations', 'Win Ratio'))
    for row in range(ROW_COUNT):
        win_count = getWinCount(data_table, row)
        total_possibilities = pow(2, row)
        win_ratio = win_count / total_possibilities

        print('{:5d} | {:12d} | {:12d} | ({:.4%})'.format(row, win_count, total_possibilities, win_ratio))

def init_table():
    data_table = [[None for _ in range(MAX_VALUE - MIN_VALUE + 1)] for _ in range(ROW_COUNT + 1)]

    # Seed value for starting at 0
    data_table[0][getIndexForValue(0)] = 1
    return data_table

def populateTable(data_table):
    for value in range(MIN_VALUE, MAX_VALUE + 1):
        getOrCalculateValue(data_table, ROW_COUNT, value)

def getOrCalculateValue(data_table, row, value):
    colIndex = getIndexForValue(value);

    curValue = data_table[row][colIndex]
    if curValue is not None:
        return curValue

    contributions = []

    # Edge case; row 0 is all 0 except for seed value
    if row != 0:
        # Left side contribution
        if value > MIN_VALUE + 1:
            # Coin B - contributions from range(..0) map to range(..2)
            if value <= 2:
                contributions.append(getOrCalculateValue(data_table, row - 1, value - 2))
            # Coin A - contributions from range(1..) map to range(2..)
            if value >= 2:
                contributions.append(getOrCalculateValue(data_table, row - 1, value - 1))
        # Right side contribution
        if value < MAX_VALUE:
            # Coin B - contributions from range(..0) map to range(..-2)
            if value <= -2:
                contributions.append(getOrCalculateValue(data_table, row - 1, value + 2))
            # Coin B - contributions from range(1..) map to range(0..)
            if value >= 0:
                contributions.append(getOrCalculateValue(data_table, row - 1, value + 1))

    result = sum(contributions)
    data_table[row][colIndex] = result
    return result

def print_debug_table(data_table):
    print 'Flips | ',
    for col_label in range(MIN_VALUE, MAX_VALUE + 1):
        print '{:5d}'.format(col_label),
    print
    for row_num, row in enumerate(data_table):
        print '{:5d} | '.format(row_num),
        for item in row:
            print '{:5d}'.format(item),
        print

def getWinCount(data_table, row):
    # Sum values in row from 1 to end
    return sum(data_table[row][getIndexForValue(1):])

# Convert column label to array column index
def getIndexForValue(value):
    return value - MIN_VALUE

if __name__ == '__main__':
    main();