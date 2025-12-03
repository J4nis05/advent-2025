from helper import FileHandler, Logger
from rich.console import Console

console = Console()
logger = Logger(console)


class Dial():
    def __init__(self):
        self.first    = 0  # Left Side (min) of the Dial
        self.last     = 99 # Right Side (max) od the Dial
        self.position = 50 # Initial Start Position
        self.hits     = 0  # Total Times the 
        self.target   = 0  # Target Position that Increments the Hits
        self.step     = 1  # Workaround until I learn Math
    
    def decode(self, value: str):
        """Split a Value between Direction and Num"""
        direction = value[:1]
        number = value[1:]
        if direction not in ["L", "R"]:
            logger.error(f"Direction {direction} is not Valid")
            ValueError()
        if not number.isdigit():
            logger.error(f"Number {number} is not Valid")
            ValueError()
        return direction, int(number)
    
    def step_rotate(self, dir: str, amt: int):
        """Workaround until I learn Math"""
        for i in range(amt):
            if dir.upper() == "R":
                new = self.position + self.step
            else:
                new = self.position - self.step
            
            if   new > self.last : self.position = self.first
            elif new < self.first: self.position = self.last
            else                 : self.position = new

    def rotate(self, dir: str, amt: int):
        self.step_rotate(dir, amt)
        if self.position == self.target: self.hits += 1
        return self.position


def process(dial: Dial, steps: list):
    for step in steps:
        if not step: continue
        direction, amount = dial.decode(step)
        dial.rotate(direction, amount)



logger.info("Opening Input File")
input_file = FileHandler.read("01/input", mode="r")
input_combination = input_file.split("\n")
test_data = {
    "data": ["L68", "L30", "R48", "L5", "R60", "L55", "L1", "L99", "R14", "L82", ],
    "expected": 3 
}

dial = Dial()
TEST = False

if TEST:
    logger.info("Running Test")
    process(dial, test_data.get("data"))
    logger.info(f"Expected: {test_data.get("expected")}")
else:
    logger.info("Processing...")
    process(dial, input_combination)

logger.info(f"Result: {dial.hits}")
