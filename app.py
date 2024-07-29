import json, os, pickle, re

DB_FILE = "./.data"
ROW_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']

class Seat:
    def __init__(self, number, booked=False):
        self.number = number
        self.booked = booked

    def __str__(self):
        return f"Seat Number: {self.number} Booked: {self.booked}"
    
    def __repr__(self) -> str:
        return f"Seat Number: {self.number} Booked: {self.booked}"

class Row:
    def __init__(self, letter, seats):
        self.letter = letter
        self.seats = seats

    def __str__(self):
        return f"Row Letter: {self.letter} Seats: {self.seats}"

    def __repr__(self):
        return f"Row Letter: {self.letter} Seats: {self.seats}"

class Data:
    def __init__(self, rows):
        self.rows = rows

class Main:
    def __init__(self):
        self.data = None
        if os.path.exists(DB_FILE):
            # App has run before, load data
            self.data = self.read_data()
        else:
            rows = self.init_data()
            self.data = Data(rows)

        self.expression = re.compile("^(BOOK|CANCEL)\s([A-T][0-7])\s([0-7])")
    
    def init_data(self):
        rows = {}
        for row_letter in ROW_LETTERS:
            rows[row_letter] = Row(row_letter, [Seat(index) for index in range(8)])
        return rows

    def save_data(self):
        with open(DB_FILE, 'wb') as f:
            pickle.dump(self.data, f)

    def read_data(self):
        with open(DB_FILE, 'rb') as f:
            return pickle.load(f)

    def modify_seat(self, command):
        match = self.expression.match(command)
        if match:
            #Command matches expected format
            operation, start, count = match.group(1, 2, 3)

            if operation == 'BOOK':
                pass
            else:
                pass
    
if __name__ == "__main__":
    m = Main()
    # print(m.expression.match("BOOK A0 7"))
    # print(m.expression.match("CANCEL A2 7"))
    # print(m.expression.match("BOOK A0 8"))
    # print(m.expression.match("CANCEL A20 7"))
    # print(m.expression.match("BOOK Z0 7"))
    # print(m.expression.match("CANCEL U2 7"))
    # print(m.expression.match("REMOVE A2 7"))
    m.data.rows['A'].seats[0].booked = True
    m.save_data()
    print(len(m.data.rows['A'].seats))
