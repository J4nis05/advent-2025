from helper import FileHandler, Logger
from rich.console import Console

console = Console()
logger = Logger(console)

# Add Type Checking if I remember to
def sum_list(input_list: list[int]) -> int:
    total = 0
    for number in input_list: total += number 
    return total


def find_criminal_ids(range: str) -> list[int]:
    found_ids = []
    current, last = range.split("-", 1)
    current = int(current)
    last = int(last) # <--- I'm sure this is the Best solution 

    # don't let casey see this
    while current <= last:
        length = len(str(current))
        if length % 2 != 0:
            current += 1 
            continue # Odd Pattern can't repeat twice
        split_length = int(length / 2)

        left = str(current)[:split_length]
        right = str(current)[split_length:]
        
        if left == right: found_ids.append(current)
        current += 1

    return found_ids


def process(ranges: list):
    all_criminals = []
    for range in ranges:
        if not range: continue
        all_criminals += find_criminal_ids(range)
    return all_criminals, sum_list(all_criminals)


logger.info("Opening Input File")
input_file = FileHandler.read("02/input", mode="r")
input_data = input_file.split(",")
test_data = {
    "data": "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124",
    "expected": 1227775554 
}
TEST = False

if TEST:
    logger.info("Testing")
    data = test_data.get("data").split(",")
    all_ids, result = process(data)
    logger.info(f"Expected: {test_data.get("expected")}")
else:
    all_ids, result = process(input_data)

logger.info(f"Result: {result}")
logger.debug(f"Found IDs: {all_ids}")
