#!/usr/bin/python3

class Sudoku:
    def __init__(self):
        self.new_game()

    def new_game(self):
        self.set_board("000000000000000000000000000000000000000000000000000000000000000000000000000000000")


    def set_board(self, s):
        self.board = []
        for c in s:
            c = int(c)
            if c > 0:
                self.board.append({c})
            else:
                self.board.append({1, 2, 3, 4, 5, 6, 7, 8, 9})

    def print_board(self):
        for row in range(9):
            if row % 3 == 0:
                print("+-------+-------+-------+")
            for col in range(9):
                if col % 3 == 0:
                    print("| ", end='')
                square = row * 9 + col
                if len(self.board[square]) == 1:
                    print(next(iter(self.board[square])), "", end='')
                else:
                    print("  ", end='')
            print("|")
        print("+-------+-------+-------+")


if __name__ == "__main__":
    with open('puzzles.txt') as f:
        puzzles = f.read().rstrip('\n').splitlines()

    s = Sudoku()
    s.print_board()
    s.set_board(puzzles[0])
    s.print_board()


