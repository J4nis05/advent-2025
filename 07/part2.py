from dataclasses import asdict
from enum import Enum
from helper import FileHandler, Logger
from rich.console import Console
from textwrap import wrap
from copy import deepcopy
from random import randint
from collections import defaultdict
import json

console = Console()
logger = Logger(console)

def randid() -> str:
    return randint(1000000, 9999999)

class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

class Grid:
    def __init__(self, layout: list[str] | str):
        self.layout = layout
        self.rows = []
        self.grid = self.prep_grid()
        self.cursor = (0, 0) # X / Y, Row / Column
        self.height = len(self.grid)
        self.width = len(max(self.grid, key=len))


    def prep_grid(self):
        """Prepare Grid based on input string / list[str]"""
        if type(self.layout) == str:
            self.rows = self.layout.split("\n")
        else:
            self.rows = self.layout

        if not self.rows[-1]:
            self.rows.pop(-1)

        grid = []
        for row in self.rows:
            if row:
                grid.append(wrap(row, 1, drop_whitespace=False))
        return grid

    # https://stackoverflow.com/questions/5125619/why-doesnt-list-have-safe-get-method-like-dictionary
    def safe_get (self, default: any = None):
        """Try to get a Value from a 2d array, return a default when index out of range"""
        # Here Negative Numbers are not valid
        x, y = self.cursor
        if x < 0 or y < 0:
            return default
        try:
            return self.grid[x][y]
        except IndexError:
            return default

    def get_cursor(self) -> (int, int):
        return self.cursor
    
    def set_cursor(self, x: int = 0, y: int = 0) -> str:
        if x < 0: x = 0
        if y < 0: y = 0
        if x >= self.height: x = self.height - 1
        if y >= self.width: y = self.width - 1
        self.cursor = (x, y)
        return self.grid[x][y]
    
    def move_cursor(self, direction: Direction, amount: int) -> str:
        """Move X Steps Up, Down, Left, or Right based on cursor"""
        x, y = self.get_cursor()
        match direction:
            case Direction.UP:
                new_pos = 0 if x - amount <= 0 else x - amount
                self.set_cursor(new_pos, y)
            case Direction.DOWN:
                new_pos = self.height - 1 if x + amount >= self.height else x + amount
                self.set_cursor(new_pos, y)
            case Direction.LEFT:
                new_pos = 0 if y - amount <= 0 else y - amount
                self.set_cursor(x, new_pos)
            case Direction.RIGHT:
                new_pos = self.width - 1 if y + amount >= self.width else y + amount
                self.set_cursor(x, new_pos)

        return self.safe_get()

    def move_left(self):
        return self.move_cursor(Direction.LEFT, 1)
    
    def move_right(self):
        return self.move_cursor(Direction.RIGHT, 1)
    
    def move_up(self):
        return self.move_cursor(Direction.UP, 1)
    
    def move_down(self):
        return self.move_cursor(Direction.DOWN, 1)

    def get_row(self, x: int) -> list[str]:
        return self.grid[x]

    def get_column(self, y: int) -> list[str]:
        column = []
        for row in self.grid:
            column.append(row[y])
        return column

    def find_all(self, symbol: str) -> list[(int, int)]:
        positions = []
        x = 0
        y = 0
        for row in self.grid:
            for character in row:
                if character == symbol:
                    positions.append((x, y))
                y += 1
            y = 0
            x += 1
        if not positions:
            return [(0, 0)]
        return positions

    def replace_current_location(self, symbol: str):
        if not symbol: return
        x, y = self.get_cursor()
        self.grid[x][y] = symbol

    def string_grid(self) -> str:
        pretty_grid = ""
        for row in self.grid:
            pretty_grid += "".join(row) + "\n"
        return pretty_grid


def beam(grid: Grid, start_character: str = "S", splitter_character: str = r"^", pipe_character: str = "|"):
    if not start_character   : start_character = "S"
    if not splitter_character: splitter_character = r"^"
    if not pipe_character    : pipe_character = "|"

    start = grid.find_all(start_character)[0]
    split_locations = []
    active_beams = { randid(): start }

    # Part 1 -> Get all Active Splitters
    while active_beams:
        beam_keys = list(active_beams.keys())
        for beam_key in beam_keys:
            x, y = active_beams.get(beam_key, (0, 0))
            grid.set_cursor(x, y)
            character = grid.move_cursor(Direction.DOWN, 1)

            match character:
                case z if z == pipe_character:
                    # There is already a beam here so skip
                    active_beams.pop(beam_key, None)
                    continue

                case z if z == splitter_character:
                    # Splitter Found, remove current beam and create 2 new ones
                    current_location = grid.get_cursor()
                    x, y = current_location
                    if current_location not in split_locations:
                        split_locations.append(current_location)
                    active_beams[randid()] = (x, y - 1)
                    active_beams[randid()] = (x, y + 1)
                    grid.set_cursor(x, y - 1)
                    grid.replace_current_location(pipe_character)
                    grid.set_cursor(x, y + 1)
                    grid.replace_current_location(pipe_character)
                    active_beams.pop(beam_key, None)
                    continue

                case "." | _:
                    # Neither splitter, nor beam, so make beam here
                    grid.replace_current_location(pipe_character)
                    active_beams[beam_key] = grid.get_cursor()

    # Part 1.1 -> Reset Board
    pipes = grid.find_all(pipe_character)
    for x, y in pipes:
        grid.set_cursor(x, y)
        grid.replace_current_location(".")

    # Part 1.2 -> Remove all Inactive Splitters
    splitters = grid.find_all(splitter_character)
    for x, y in splitters:
        if (x, y) in split_locations:
            continue
        grid.set_cursor(x, y)
        grid.replace_current_location(".")

    # Part 2 -> Timelines
    start_x, start_y = start
    timelines = { start_y: 1 }
    exits = 0
    for x in range(start_x, grid.height):
        next_timelines = defaultdict(int)
        row = grid.get_row(x)
        for y, amount in timelines.items():
            if y < 0 or y >= grid.width:
                exits += amount
                continue

            cell = row[y]
            if cell == splitter_character:
                left, right = y - 1, y + 1
                if left >= 0: next_timelines[left] += amount
                else: exits += amount

                if right < grid.width: next_timelines[right] += amount
                else: exits += amount
            else:
                next_timelines[y] += amount
        
        timelines = next_timelines

    total_timelines = exits + sum(timelines.values())
    return total_timelines, timelines, grid


def process(layout: list[str]):
    grid = Grid(layout)
    result, outputs, out_grid = beam(grid)
    return result, outputs, out_grid


logger.info("Opening Input File")
input_file = FileHandler.read("07/input", mode="r")
input_data = input_file.split("\n")
test_data = {
    "data": ".......S.......\n...............\n.......^.......\n...............\n......^.^......\n...............\n.....^.^.^.....\n...............\n....^.^...^....\n...............\n...^.^...^.^...\n...............\n..^...^.....^..\n...............\n.^.^.^.^.^...^.\n...............",
    "expected": 40
}
TEST = False

if TEST:
    logger.info("Testing")
    data = test_data.get("data").split("\n")
    result, outputs, grid = process(data)
    logger.info(f"Expected: {test_data.get("expected")}")
else:
    result, outputs, grid = process(input_data)

logger.info(f"Result  : {result}")
logger.info(f"Outputs : {json.dumps(outputs, indent=4)}")
