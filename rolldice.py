import argparse
import math
import logging
import secrets
import base64

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)


class Dice:
    def __init__(self, num_sides):
        self.num_sides = num_sides
        self.rolls = []
        logger.debug(f"Initiated D{num_sides}")

    def roll_dice(self, value=None):
        if value is None:
            value = secrets.randbelow(self.num_sides) + 1
        if value < 1 or value > self.num_sides:
            logger.error(f"Invalid value {value} for {self.num_sides}-sided dice")
            return
        self.rolls.append(value)

    def get_bytes(self):
        binary_str = ''.join([bin(_)[2:] for _ in self.rolls])
        binary_chunks = [binary_str[i:i + 8] for i in range(0, len(binary_str), 8)]
        byte_str = bytes([int(chunk, 2) for chunk in binary_chunks])
        return byte_str


def bits_of_entropy(dice_sides=6):
    """Calculate the bits of entropy of a dice roll."""
    return math.log2(dice_sides)


def required_dice_rolls(dice_sides=6, required_entropy=256):
    entropy = bits_of_entropy(dice_sides=dice_sides)
    ratio = entropy / required_entropy
    return math.floor(1 / ratio)


def simulate_dice_throws(num_sides=6):
    d = Dice(num_sides=num_sides)
    num_dice_rolls = required_dice_rolls(dice_sides=d.num_sides, required_entropy=256)
    for _ in range(num_dice_rolls):
        d.roll_dice()
    byte_str = d.get_bytes()
    byte_str_b64 = base64.b64encode(byte_str).decode()
    return byte_str_b64


def dice_throws(num_sides=None):
    if num_sides is None:
        num_sides = int(input("Enter the number of sides on your dice: "))
    d = Dice(num_sides)
    number_of_rolls = required_dice_rolls(dice_sides=d.num_sides, required_entropy=256)
    print(f"You will need to enter {number_of_rolls} results from dice throws.")
    while len(d.rolls) < number_of_rolls:
        dice_throws = input("Enter a list of numbers separated by comma or space: ")
        dice_throws = dice_throws.replace(",", " ").split()
        dice_throws = [int(num) for num in dice_throws]
        for throw in dice_throws:
            print(f"We need additional {number_of_rolls - len(d.rolls)} dice throws.")
            d.roll_dice(throw)
    byte_str = d.get_bytes()
    byte_str_b64 = base64.b64encode(byte_str).decode()
    return byte_str_b64


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interactive', action='store_true', help='interactive')
    args = parser.parse_args()
    if not args.interactive:
        print(simulate_dice_throws(num_sides=16))
    else:
        print(dice_throws())
