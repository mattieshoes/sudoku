#!/usr/bin/python3

import time

class Sudoku:
    def __init__(self):
        self.build_affects_table()
        self.new_game()

    def build_affects_table(self):
        self.affects = [set() for i in range(81)]
        for i in range(81):
            row = i // 9
            col = i % 9

            # shares row
            for n in range(row * 9, row * 9 + 9):
                self.affects[i].add(n)

            # shares col
            for n in range(col, 81, 9):
                self.affects[i].add(n)

            # do square
            for r in range((row // 3) * 3, (row // 3) * 3 + 3):
                for c in range((col // 3) * 3, (col // 3) * 3 + 3):
                    self.affects[i].add(r * 9 + c)

            # remove self
            self.affects[i].remove(i)

    def new_game(self):
        self.set_board("000000000000000000000000000000000000000000000000000000000000000000000000000000000")

    def set_board(self, s):
        self.board = []
        for c in s:
                self.board.append(int(c))
        self.history = []
        self.build_possibles_table()

    def print_board(self):
        for row in range(9):
            if row % 3 == 0:
                print("+-------+-------+-------+")
            for col in range(9):
                if col % 3 == 0:
                    print("| ", end='')
                square = row * 9 + col
                if self.board[square] > 0:
                    print(self.board[square], "", end='')
                else:
                    print("  ", end='')
            print("|")
        print("+-------+-------+-------+")

    def build_possibles_table(self):
        self.possibles = [{} for i in range(81)]
        for i in range(81):
            self.update_possibles(i)

    def update_possibles(self, index):
        if self.board[index] > 0:
            self.possibles[index] = set()
        else:
            self.possibles[index] = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            for i in self.affects[index]:
                if self.board[i] in self.possibles[index]:
                    self.possibles[index].remove(self.board[i])

    def solve(self):
        # find unsolved square with least possibilities
        # bail if there's an unsolved square with no possible values
        min = 10
        min_index = -1
        for i in range(81):
            p = len(self.possibles[i])
            if self.board[i] == 0:
                if p == 0:
                    return False
                if p < min:
                    min = p
                    min_index = i
        
        # Solved detection
        if min_index == -1:
            return True
        
        # Iterate through possible values for the square with the least possibilities
        for value in self.possibles[min_index]:
            self.make_move(min_index, value)
            result = self.solve()
            if not result:
                self.undo_move()
            else:
                return True
        return False

    def prove(self):
        count = 0
        # find unsolved square with least possibilities
        # bail if there's an unsolved square with no possible values
        min = 10
        min_index = -1
        for i in range(81):
            p = len(self.possibles[i])
            if self.board[i] == 0:
                if p == 0:
                    return False
                if p < min:
                    min = p
                    min_index = i
        
        # Solved detection
        if min_index == -1:
            return 1
        
        # Iterate through possible values for the square with the least possibilities
        for value in self.possibles[min_index]:
            self.make_move(min_index, value)
            count += self.prove()
            self.undo_move()
        return count

    def make_move(self, index, value):
        if value not in self.possibles[index]:
            return False
        self.history.append(index)
        self.board[index] = value
        self.possibles[index] = set()
        for i in self.affects[index]:
            self.update_possibles(i)
        return True


    def undo_move(self):
        h = self.history.pop()
        self.board[h] = 0
        self.update_possibles(h)
        for i in self.affects[h]:
            self.update_possibles(i)

if __name__ == "__main__":
    with open('puzzles.txt') as f:
        puzzles = f.read().rstrip('\n').splitlines()
    s = Sudoku()
    for i,p in enumerate(puzzles):
        s.set_board(p)
        st = time.time()        
        result = s.prove()
        pt = time.time() - st
        st = time.time()
        s.solve()
        st = time.time() - st

        print(f"Puzzle {i:3} solved in {st:0.2f} seconds and proved in {pt:0.2f} seconds")
        #s.print_board()


