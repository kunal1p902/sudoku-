# Python eBook + 99 Projects: https://resources.legitpython.com/python-ebook-download

import tkinter as tk
from tkinter import messagebox
import time
import random

def generate_full_board():
    board = [[0]*9 for _ in range(9)]

    def is_valid(board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    def solve_board(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for num in nums:
                        if is_valid(board, row, col, num):
                            board[row][col] = num
                            if solve_board(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    solve_board(board)
    return board

def remove_cells(board, count=40):
    removed = 0
    while removed < count:
        i = random.randint(0, 8)
        j = random.randint(0, 8)
        if board[i][j] != 0:
            board[i][j] = 0
            removed += 1
    return board

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")

        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.board = remove_cells(generate_full_board(), 40)

        for i in range(9):
            self.root.grid_columnconfigure(i, weight=1)
            self.root.grid_rowconfigure(i, weight=1)

        self.draw_grid()
        self.create_buttons()

    def draw_grid(self):
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(self.root, width=2, font=("Arial", 24), justify="center")
                entry.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
                if self.board[i][j] != 0:
                    entry.insert(0, str(self.board[i][j]))
                    entry.config(fg="blue", state="disabled")
                self.entries[i][j] = entry

    def create_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=9, column=0, columnspan=9, sticky="nsew")

        self.root.grid_rowconfigure(9, weight=1)
        for i in range(3):
            button_frame.grid_columnconfigure(i, weight=1)

        solve_btn = tk.Button(button_frame, text="Solve", command=self.solve_with_animation)
        solve_btn.grid(row=0, column=0, sticky="nsew")

        check_btn = tk.Button(button_frame, text="Check", command=self.check_solution)
        check_btn.grid(row=0, column=1, sticky="nsew")

        reset_btn = tk.Button(button_frame, text="New Game", command=self.reset_board)
        reset_btn.grid(row=0, column=2, sticky="nsew")

    def reset_board(self):
        self.board = remove_cells(generate_full_board(), 40)
        for i in range(9):
            for j in range(9):
                entry = self.entries[i][j]
                entry.config(state="normal", fg="black")
                entry.delete(0, tk.END)
                if self.board[i][j] != 0:
                    entry.insert(0, str(self.board[i][j]))
                    entry.config(fg="blue", state="disabled")

    def solve_with_animation(self):
        board = [[int(self.entries[i][j].get()) if self.entries[i][j].get() else 0 for j in range(9)] for i in range(9)]

        def is_valid(row, col, num):
            for i in range(9):
                if board[row][i] == num or board[i][col] == num:
                    return False
            start_row, start_col = 3 * (row // 3), 3 * (col // 3)
            for i in range(3):
                for j in range(3):
                    if board[start_row + i][start_col + j] == num:
                        return False
            return True

        def solve():
            for i in range(9):
                for j in range(9):
                    if board[i][j] == 0:
                        for num in range(1, 10):
                            if is_valid(i, j, num):
                                board[i][j] = num
                                self.entries[i][j].delete(0, tk.END)
                                self.entries[i][j].insert(0, str(num))
                                self.entries[i][j].config(fg="green")
                                self.root.update()
                                time.sleep(0.05)

                                if solve():
                                    return True

                                board[i][j] = 0
                                self.entries[i][j].delete(0, tk.END)
                                self.root.update()
                                time.sleep(0.05)
                        return False
            return True

        solve()

    def check_solution(self):
        board = []
        try:
            for i in range(9):
                row = []
                for j in range(9):
                    val = self.entries[i][j].get()
                    if val == "":
                        messagebox.showerror("Error", "The board is not complete.")
                        return
                    num = int(val)
                    if num < 1 or num > 9:
                        messagebox.showerror("Error", "Numbers must be between 1 and 9.")
                        return
                    row.append(num)
                board.append(row)

            def is_valid_board(board):
                for i in range(9):
                    row = set()
                    col = set()
                    box = set()
                    for j in range(9):
                        if board[i][j] in row or board[j][i] in col:
                            return False
                        row.add(board[i][j])
                        col.add(board[j][i])
                        r = 3 * (i // 3) + j // 3
                        c = 3 * (i % 3) + j % 3
                        if board[r][c] in box:
                            return False
                        box.add(board[r][c])
                return True

            if is_valid_board(board):
                messagebox.showinfo("Success", "✅ Correct Solution!")
            else:
                messagebox.showerror("Oops!", "❌ Incorrect Solution.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Only numbers 1-9 allowed.")


root = tk.Tk()
app = SudokuGUI(root)
root.mainloop()