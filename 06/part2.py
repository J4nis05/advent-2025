import enum
from helper import FileHandler, Logger
from rich.console import Console
from textwrap import wrap
from copy import deepcopy

console = Console()
logger = Logger(console)


# Add Type Checking if I remember to
def sum_list(input_list: list[int], operator: str = "+") -> int:
    total = 0
    match operator:
        case "*":
            total = 1
            for number in input_list: total *= int(number)
        case "-":
            for number in input_list: total -= int(number)
        case "/":
            for number in input_list: total /= int(number)
        case "+" | _:
            for number in input_list: total += int(number)
    return total


# https://stackoverflow.com/questions/5125619/why-doesnt-list-have-safe-get-method-like-dictionary
def safe_grid_get (grid: list[list[str]], x: int, y: int, default: any = None):
    """Try to get a Value from a 2d array, return a default when index out of range"""
    # Here Negative Numbers are not valid
    if x < 0 or y < 0:
        return default
    try:
        return grid[x][y]
    except IndexError:
        return default


def prep_grid(rows: list[str]) -> list[list[str]]:
    """split a list of strings into a 2d array"""
    grid = []
    for row in rows:
        if row:
            grid.append(wrap(row, 1, drop_whitespace=False))
    return grid


def column_number(grid: list[list[str]], column_index: int, top_down: bool = True) -> str:
    """Gets a Num from a given column in a given grid minus the last row"""
    total_rows = len(grid) - 1
    number = []

    for row_index, row in enumerate(grid):
        if row_index >= total_rows: continue
        number.append(row[column_index])

    # If the Number should be from bottom to top instead
    if not top_down:
        number.reverse()

    return "".join(number).replace(" ", "")


# notes:
# * Equasions have at least 1 column of " " Space between them
# * The Operator is always in the first column of the current equasion
# * These Kids today only learn Additon and multiplication
# >> Use Operators for Start Idx of equasions (list of tuples w/ start and end (inclusive))
# >>>> Start is Operator, end is next operator index -2 (-1 operator, -1 empty column)
# >> "".join(number_list) plus left strip for numbers
def homework(grid: list[list[str]]):
    solutions = []
    start_indexes = []
    total_lines = len(grid)
    operators = [ "+", "-", "*", "/" ] # All 4 just in case
    
    # Get the Start Positions of all Equasions
    last_row = grid[-1]
    for index, character in enumerate(last_row):
        if character in operators:
            start_indexes.append(index)
    total_equasions = len(start_indexes)

    for i in range(total_equasions):
        elements = []
        start_column = start_indexes[i]
        if i == total_equasions - 1:
            # If it's the last one the end column is just the last index
            end_column = len(last_row)
        else:
            end_column = start_indexes[i+1] - 1

        for current_column in range(start_column, end_column):
            elements.append(column_number(grid, current_column))

        operator = last_row[start_column]
        elements.reverse() # I get the numbers from left to right, but it should be reversed
        solutions.append(sum_list(elements, operator))

    solutions.reverse() # I get the numbers from left to right, but it should be reversed
    return solutions


def process(layout: list[str]):
    grid = prep_grid(layout)
    outputs = homework(grid)
    result = sum_list(outputs)
    return result, outputs


logger.info("Opening Input File")
input_file = FileHandler.read("06/input", mode="r")
input_data = input_file.split("\n")
test_data = {
    "data": "123 328  51 64 \n 45 64  387 23 \n  6 98  215 314\n*   +   *   +  \n",
    "expected": 3263827
}
TEST = False

if TEST:
    logger.info("Testing")
    data = test_data.get("data").split("\n")
    result, outputs = process(data)
    logger.info(f"Expected: {test_data.get("expected")}")
else:
    result, outputs = process(input_data)

logger.info(f"Result  : {result}")
logger.info(f"Outputs : {outputs}")
