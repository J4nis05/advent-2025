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


def total_fresh_ids(ranges: list[str]):
    merged_ranges = []
    fresh_count = []

    ranges.sort(key=lambda s: int(s.split("-")[0]))
    tuple_ranges = [get_min_max(range_str) for range_str in ranges]

    for current_range in tuple_ranges:
        # list of tuples where index 0 is start and 1 is end
        if len(merged_ranges) == 0:
            merged_ranges.append(current_range)
            continue

        # If the ranges overlap or touch: merge them
        a, b = merged_ranges[-1]
        c, d = current_range
        is_overlapping = a <= d + 1 and c <= b + 1 # +1 for Adjacent ranges
        if is_overlapping:
            merged_ranges[-1] = (min(a, c), max(b, d)) # Merge Range with lowest and highest of both
            continue
        
        # Otherwise just make it a new range
        merged_ranges.append(current_range)

    for start, end in merged_ranges:
        fresh_count.append(end - start + 1)

    return fresh_count


def process(ranges: list[str]):
    outputs = total_fresh_ids(ranges)
    result = sum_list(outputs)
    return result, outputs


logger.info("Opening Input File")
input_file = FileHandler.read("05/input", mode="r")
raw_ranges, _ = input_file.split("\n\n", 1)
ranges = raw_ranges.split("\n")
test_data = {
    "data": [[ "3-5", "10-14", "16-20", "12-18" ], [ 1, 5, 8, 11, 17, 32 ]],
    "expected": 14
}
TEST = False

if TEST:
    logger.info("Testing")
    data = test_data.get("data")
    result, outputs = process(data[0])
    logger.info(f"Expected: {test_data.get("expected")}")
else:
    result, outputs = process(ranges)

logger.info(f"Result  : {result}")
logger.info(f"Outputs : {outputs}")
