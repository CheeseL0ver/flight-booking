#!/usr/bin/env python
import os, pickle, re, argparse, sys
from typing import List, Dict

# "CONSTANTS"
DB_FILE = "./.data"
SUCCESS = "SUCCESS"
FAIL = "FAIL"
ROW_LETTERS = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
]


class Seat:
    """Dataclass for plane seat representation"""

    def __init__(self, number: int, booked=False):
        """
        Class constructor
        :param number: Number representation for the seat
        :param booked: Status for the seat's booking
        """
        self.number = number
        self.booked = booked

    def __str__(self) -> str:
        return f"Seat Number: {self.number} Booked: {self.booked}"

    def __repr__(self) -> str:
        return f"Seat Number: {self.number} Booked: {self.booked}"


class Row:
    """Dataclass for plane row representation"""

    def __init__(self, letter: str, seats: List[Seat]):
        """
        Class constructor

        :param letter: Letter representation for the row
        :param seats: Seats within the row
        """
        self.letter: str = letter
        self.seats: List[Seat] = seats

    def __str__(self) -> str:
        return f"Row Letter: {self.letter} Seats: {self.seats}"

    def __repr__(self) -> str:
        return f"Row Letter: {self.letter} Seats: {self.seats}"


class Data:
    """Container dataclass for seating information"""

    def __init__(self, rows: Dict[str, Row]):
        """
        Class constructor

        :param rows: Map reprentation of the plane rows
        """
        self.rows: Dict[str, Row] = rows


class Main:
    def __init__(self, args):
        """
        Class constructor

        :param args: Namespace of CLI arguments
        """

        # Regex performs most of the "heavy lifting" for input verification
        self.expression = re.compile("^(BOOK|CANCEL)\s([A-T])([0-7])\s([1-7])$")
        self.data: Data = None
        self.verbose = args.verbose

        # Load/initialize data
        if os.path.exists(DB_FILE):
            # App has run before, load data
            self.data = self.read_data()
        else:
            rows = self.init_rows()
            self.data = Data(rows)

    def init_rows(self) -> List[Row]:
        """
        Initializes data representation of plane rows

        :return Dict[str,Row]: Map reprentation of the plane rows
        """
        rows = {}
        for row_letter in ROW_LETTERS:
            rows[row_letter] = Row(row_letter, [Seat(index) for index in range(8)])
        return rows

    def save_data(self):
        """
        Write 'Data' object to file
        """
        if self.verbose:
            print("Saving data to file...")
        with open(DB_FILE, "wb") as f:
            pickle.dump(self.data, f)

    def read_data(self) -> Data:
        """
        Read data from save file

        :return Data: Class representation of file data
        """
        if self.verbose:
            print("Reading data from file...")
        with open(DB_FILE, "rb") as f:
            return pickle.load(f)

    def modify_booking(self, command) -> bool:
        """
        Modify reservation of seats
        :param command: command to action

        :return bool: True if completed successfully,
                      False otherwise
        """
        match = self.expression.match(command)
        if match:
            # Command matches expected format
            operation, row, start, count = match.group(1, 2, 3, 4)

            # Convert digits
            start = int(start)
            count = int(count)
            stop = start + count

            # Protect against indexing errors
            if stop > len(self.data.rows[row].seats):
                return False

            # Protect against unintended data modification
            seats = self.data.rows[row].seats.copy()
            if operation == "BOOK":
                for index in range(start, stop):
                    if seats[index].booked:
                        if self.verbose:
                            print(f'Failed to book seat(s) using command: "{command}"')
                        return False
                    else:
                        if self.verbose:
                            print(
                                f'Booked seat "{index}" in row "{row}" using command: "{command}"'
                            )
                        seats[index].booked = True

            if operation == "CANCEL":
                for index in range(start, stop):
                    if not seats[index].booked:
                        if self.verbose:
                            print(
                                f'Failed to cancel seat(s) using command: "{command}"'
                            )
                        return False
                    else:
                        if self.verbose:
                            print(
                                f'Cancelled booking for seat "{index}" in row "{row}" using command: "{command}"'
                            )
                        seats[index].booked = False

            # Update the row contents post operation
            self.data.rows[row].seats = seats
            if self.verbose:
                print("Updated instance booking data")
            return True

        else:
            # Input was invalid
            if self.verbose:
                print(f'Failed to operate. Invalid command: "{command}"')
            return False


class CustomParser(argparse.ArgumentParser):
    """Custom parser class to prevent error output"""

    def error(self, message):
        """
        Overridden error handler

        :param message: Error message
        """
        message = FAIL
        raise argparse.ArgumentError(None, message)


def create_parser() -> CustomParser:
    """Helper function to contain parser logic"""
    parser: CustomParser = CustomParser(
        description="Flight booking application", add_help=False
    )
    parser.add_argument(
        "command", metavar="COMMAND", type=str, nargs=3, help="Command for execution"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output (default: False)",
    )

    return parser


def run(args):
    """Helper function to run main logic"""
    command = " ".join(args.command)
    m = Main(args)

    if m.modify_booking(command):
        print(SUCCESS)
        # Only save if data was modified
        m.save_data()
    else:
        print(FAIL)


if __name__ == "__main__":
    try:
        parser = create_parser()
        args = parser.parse_args()
        run(args)
    except:
        print(FAIL)

    sys.exit(0)
