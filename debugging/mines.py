#!/usr/bin/python3
import random
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Minesweeper:
    def __init__(self, width=10, height=10, mines=10):
        self.width = width
        self.height = height

        # Safety: prevent impossible boards
        total_cells = width * height
        if mines >= total_cells:
            raise ValueError("Number of mines must be less than total number of cells.")

        self.mines = set(random.sample(range(total_cells), mines))
        self.field = [[' ' for _ in range(width)] for _ in range(height)]
        self.revealed = [[False for _ in range(width)] for _ in range(height)]

    def print_board(self, reveal=False):
        clear_screen()
        print('  ' + ' '.join(str(i) for i in range(self.width)))
        for y in range(self.height):
            print(y, end=' ')
            for x in range(self.width):
                if reveal or self.revealed[y][x]:
                    if (y * self.width + x) in self.mines:
                        print('*', end=' ')
                    else:
                        count = self.count_mines_nearby(x, y)
                        print(count if count > 0 else ' ', end=' ')
                else:
                    print('.', end=' ')
            print()

    def count_mines_nearby(self, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  # don't count the cell itself
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (ny * self.width + nx) in self.mines:
                        count += 1
        return count

    def reveal(self, x, y):
        # Bounds check (prevents IndexError)
        if not (0 <= x < self.width and 0 <= y < self.height):
            print("Out of bounds. Try again.")
            return True  # not a mine hit, just invalid move

        if self.revealed[y][x]:
            return True  # already revealed, do nothing

        if (y * self.width + x) in self.mines:
            return False  # hit a mine

        self.revealed[y][x] = True

        # Flood fill if no adjacent mines
        if self.count_mines_nearby(x, y) == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if not self.revealed[ny][nx]:
                            self.reveal(nx, ny)
        return True

    def is_won(self):
        # Count revealed non-mine cells
        revealed_safe = 0
        for y in range(self.height):
            for x in range(self.width):
                idx = y * self.width + x
                if idx not in self.mines and self.revealed[y][x]:
                    revealed_safe += 1

        total_safe = self.width * self.height - len(self.mines)
        return revealed_safe == total_safe

    def play(self):
        while True:
            self.print_board()
            try:
                x = int(input("Enter x coordinate: "))
                y = int(input("Enter y coordinate: "))

                if not self.reveal(x, y):
                    self.print_board(reveal=True)
                    print("Game Over! You hit a mine.")
                    break

                # ✅ Win condition check
                if self.is_won():
                    self.print_board(reveal=True)
                    print("You win! All safe cells have been revealed 🎉")
                    break

            except ValueError:
                print("Invalid input. Please enter numbers only.")

if __name__ == "__main__":
    game = Minesweeper()
    game.play()
