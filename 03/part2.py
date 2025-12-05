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


# https://stackoverflow.com/questions/5125619/why-doesnt-list-have-safe-get-method-like-dictionary
def safe_list_get (l: list, index: int, default: int = 0):
  try:
    return l[index]
  except IndexError:
    return default


#TODO: Some banks are too short, some ignore last numbers
#TODO. Fix Replacement Logic -> Currently only previcous can be replaced
#TODO: While Loop to remove Digits while still long enough?
#      --> While last_digit < new_digit and long_enough
def joltage(bank: str, greed: int = 12) -> int:
    index = 0
    combination = ["0"]
    length = len(bank)

    splits = textwrap.wrap(bank, 1)
    for split in splits:
        current_length = len(combination)                      # How many Batteries are currently Active
        current_number = int(split)                            # What Number is currently getting Checked
        remaining = length - index                             # The Amount of Remaining Splits
        can_remove = (current_length - 1) + remaining >= greed # Can the prev one be removed (Enough splits left)
        
        # Remove the Last item in the Combination while 
        # * it is smaller than the current option
        # * and there is still enough remaining candidates
        while (combination and int(safe_list_get(combination, -1, 0)) < current_number and can_remove):
            combination.pop()
            current_length = len(combination)
            can_remove = (current_length - 1) + remaining >= greed

        # Skip if We are at 12 AND the current Choice is smaller than the last in the list
        if current_length >= greed and current_number <= int(safe_list_get(combination, -1, 0)):
            index += 1
            continue

        # If we're below 12 add the current choice to the list
        if current_length < greed:
            combination.append(split)
        
        index += 1
   
    final = ""
    for item in combination:
        final = final + item
    
    return int(final)



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
    "expected": 3121910778619
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
if TEST: logger.info(f"Expected: [987654321111, 811111111119, 434234234278, 888911112111]")
