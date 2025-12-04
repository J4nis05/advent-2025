from helper import FileHandler, Logger
from rich.console import Console
import textwrap

console = Console()
logger = Logger(console)


# Add Type Checking if I remember to
def sum_list(input_list: list[int]) -> int:
    total = 0
    for number in input_list: total += number 
    return total


def joltage(bank: str) -> int:
    candidates = []
    index = 1
    length = len(bank)
    splits = textwrap.wrap(bank, 1) # <- Better way to do this?
    for split in splits:
        current_max = "0"
        for i in range(index, length):
            candidate = split + splits[i]
            if int(candidate) > int(current_max):
                current_max = candidate
        candidates.append(int(current_max))        
        index += 1
    candidates.sort(reverse=True)
    return candidates[0]


def process(banks: list[str]):
    outputs = []
    for bank in banks:
        if not bank: continue
        outputs.append(joltage(bank))
    total = sum_list(outputs)
    return total, outputs


logger.info("Opening Input File")
input_file = FileHandler.read("03/input", mode="r")
input_data = input_file.split("\n")
test_data = {
    "data": [ "987654321111111", "811111111111119", "234234234234278", "818181911112111" ],
    "expected": 357
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
logger.info(f"Outputs : {outputs}")
