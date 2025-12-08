from helper import FileHandler, Logger
from rich.console import Console

console = Console()
logger = Logger(console)


# Add Type Checking if I remember to
def sum_list(input_list: list[int]) -> int:
    total = 0
    for number in input_list: total += number 
    return total


def get_min_max(target: str):
    min, max = target.split("-", 1)
    return int(min), int(max)


def is_in_range(start: int, end: int, value: int, inclusive: bool = True) -> bool:
    if not inclusive:
        start += 1
        end -= 1
    
    if value >= start and value <= end:
        return True
    else:
        return False


def check_ids(ranges: list[str], ids: list[int]):
    fresh_ids = []
    rotten_ids = []

    for product_id in ids:
        if product_id in [ None, "" ]: continue
        found = False
        for product_range in ranges:
            start, end = get_min_max(product_range)
            if is_in_range(start, end, int(product_id)):
                found = True
                break
    
        if found:
            fresh_ids.append(product_id)
        else:
            rotten_ids.append(product_id)

    return len(fresh_ids), len(rotten_ids), fresh_ids, rotten_ids


def process(ranges: list[str], ids: list[int]):
    fresh, rotten, fresh_ids, rotten_ids = check_ids(ranges, ids)
    return fresh, rotten_ids


logger.info("Opening Input File")
input_file = FileHandler.read("05/input", mode="r")
raw_ranges, raw_ids = input_file.split("\n\n", 1)
ids = raw_ids.split("\n")
ranges = raw_ranges.split("\n")
test_data = {
    "data": [[ "3-5", "10-14", "16-20", "12-18" ], [ 1, 5, 8, 11, 17, 32 ]],
    "expected": 3
}
TEST = False

if TEST:
    logger.info("Testing")
    data = test_data.get("data")
    result, outputs = process(data[0], data[1])
    logger.info(f"Expected: {test_data.get("expected")}")
else:
    result, outputs = process(ranges, ids)

logger.info(f"Result  : {result}")
logger.info(f"Outputs : {outputs}")
