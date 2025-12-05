from helper import FileHandler, Logger
from rich.console import Console
from textwrap import wrap
from copy import deepcopy

console = Console()
logger = Logger(console)


# https://stackoverflow.com/questions/5125619/why-doesnt-list-have-safe-get-method-like-dictionary
def safe_grid_get (grid: list[list[str]], x: int, y: int, default: any = "."):
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
        grid.append(wrap(row, 1))
    return grid


def neighbours(grid: list[list[str]], x: int, y: int) -> list[str]:
    """Get the Content of the Neighbouring Cells in a 2d array (Minesweeper Style)"""
    neighbours = []
    # Why am i like this
    neighbours.append(safe_grid_get(grid, x-1, y-1)) # Top Left
    neighbours.append(safe_grid_get(grid, x+0, y-1)) # Top Center
    neighbours.append(safe_grid_get(grid, x+1, y-1)) # Top Right
    neighbours.append(safe_grid_get(grid, x-1, y+0)) # Middle Left
    neighbours.append(safe_grid_get(grid, x+1, y+0)) # Middle Right
    neighbours.append(safe_grid_get(grid, x-1, y+1)) # Bottom Left
    neighbours.append(safe_grid_get(grid, x+0, y+1)) # Bottom Center
    neighbours.append(safe_grid_get(grid, x+1, y+1)) # Bottom Right
    return neighbours


def is_paper(content: str, symbol: str = "@") -> bool:
    """If the given content is matching the given Symbol return True"""
    if content == symbol:
        return True
    return False


def forklift_certified(grid: list[list[str]], limit: int = 4, symbol: str = "@", replace: str = "X") -> int:
    clean = deepcopy(grid)
    total = 0  # Valid Rolls of Papaer
    x = 0      # (Row) Horizontal Grid Location
    y = 0      # (Col) Vertical Grid Location

    # * Try Each Spot in the Grid
    # * If it is a Roll (@):
    # Check if the surounding Cells contain fewer than "limit" Rolls
    # Position X, Y means we need to check
    #  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx
    # 
    # Y  X-1,Y-1  X-0,Y-1  X+1,Y-1
    # Y  X-1,Y-0           X+1,Y+0
    # Y  X-1,Y+1  X-0,Y+1  X+1,Y+1

    for row in grid:
        for cell in row:
            if is_paper(cell, symbol):
                rolls = 0
                adjacent = neighbours(grid, x, y) # Get the Neighbouring Cells (see Comment above)
                for neighbour in adjacent:
                    if is_paper(neighbour, symbol):
                        rolls += 1

                if rolls < limit:
                    total += 1
                    clean[x][y] = replace
            y += 1
        y = 0
        x += 1

    return total, clean


def process(layout: list[str]):
    grid = prep_grid(layout)
    total, out_grid = forklift_certified(grid)
    return total, out_grid


logger.info("Opening Input File")
input_file = FileHandler.read("04/input", mode="r")
input_data = input_file.split("\n")
test_data = {
    "data": [ "..@@.@@@@.", "@@@.@.@.@@", "@@@@@.@.@@", "@.@@@@..@.", "@@.@@@@.@@", ".@@@@@@@.@", ".@.@.@.@@@", "@.@@@.@@@@", ".@@@@@@@@.", "@.@.@@@.@." ],
    "expected": 13
}
TEST = False

if TEST:
    logger.info("Testing")
    data = test_data.get("data")
    result, outputs = process(data)
    logger.info(f"Expected: {test_data.get("expected")}")
else:
    result, outputs = process(input_data)

logger.info(f"Result  : {result}")
logger.info(f"Outputs : \n")
cleaned = ""
for row in outputs:
    cleaned += f"{"".join(row)}\n"

logger.info(cleaned)
