import os, pickle, re
from typing import List, Dict

DB_FILE = "./.data"
ROW_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']

class Seat:
    """Dataclass for plane seat representation"""
    def __init__(self, number, booked=False):
        """
        Class constructor
        :param number: Number representation for the seat
        :param booked: Status for the seat's booking
        """
        self.number = number
        self.booked = booked

    def __str__(self):
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

    def __str__(self):
        return f"Row Letter: {self.letter} Seats: {self.seats}"

    def __repr__(self):
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
    def __init__(self):
        """Class constructor"""
        self.expression = re.compile("^(BOOK|CANCEL)\s([A-T])([0-7])\s([1-7])$")
        self.data: Data = None
        
        # Load/initialize data
        if os.path.exists(DB_FILE):
            # App has run before, load data
            self.data = self.read_data()
        else:
            rows = self.init_rows()
            self.data = Data(rows)

    def init_rows(self):
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
        with open(DB_FILE, 'wb') as f:
            pickle.dump(self.data, f)

    def read_data(self):
        """
        Read data from save file

        :return Data: Class representation of file data
        """
        with open(DB_FILE, 'rb') as f:
            return pickle.load(f)

    def modify_booking(self, command):
        """
        Modify reservation of seats
        :param command: command to action
        
        :return bool: True if completed successfully,
                      false otherwise
        """
        match = self.expression.match(command)
        if match:
            #Command matches expected format
            operation, row, start, count = match.group(1, 2, 3, 4)

            #Convert digits
            start = int(start)
            count = int(count)
            stop = start + count

            #Protect 
            if stop > len(self.data.rows[row].seats):
                return False

            if operation == 'BOOK':
                seats = self.data.rows[row].seats.copy()
                for index in range(start, stop):
                    if seats[index].booked:
                        return False
                    else:
                        seats[index].booked = True

                # Update the row contents
                self.data.rows[row].seats = seats
                return True

            if operation == 'CANCEL':
                seats = self.data.rows[row].seats.copy()
                for index in range(start, stop):    
                    if not seats[index].booked:
                        return False
                    else:
                        seats[index].booked = False

                # Update the row contents
                self.data.rows[row].seats = seats
                return True
    
        else:
            #Input was invalid
            return False
        
if __name__ == "__main__":
    m = Main()

    # Given TC
    print(f'BOOK A0 1: {m.modify_booking("BOOK A0 1")}')
    print(f'CANCEL A0 1: {m.modify_booking("CANCEL A0 1")}')
    print(f'BOOK A0 1: {m.modify_booking("BOOK A0 1")}')
    print(f'BOOK A0 1: {m.modify_booking("BOOK A0 1")}')
    print(f'BOOK A1 1: {m.modify_booking("BOOK A1 1")}')
    print(f'BOOK A2 4: {m.modify_booking("BOOK A2 4")}')
    print(f'BOOK A5 1: {m.modify_booking("BOOK A5 1")}')
    print(f'BOOK A6 3: {m.modify_booking("BOOK A6 3")}')
    print(f'BOOK A6 4: {m.modify_booking("BOOK A6 4")}')
    print(f'BOOK A8 1: {m.modify_booking("BOOK A8 1")}')
    print(f'BOOK U1 1: {m.modify_booking("BOOK U1 1")}')

    # Additional TC
    print(f'BOOK A0 7: {m.modify_booking("BOOK A0 7")}')
    print(f'BOOK A0 7: {m.modify_booking("BOOK A0 7")}')
    print(f'BOOK A0 0: {m.modify_booking("BOOK A0 0")}')
    print(f'BOOK A0 10: {m.modify_booking("BOOK A0 10")}')
    print(f'CANCEL A0 7: {m.modify_booking("CANCEL A0 7")}')
    print(f'CANCEL A0 7: {m.modify_booking("CANCEL A0 7")}')

    # m.save_data()
