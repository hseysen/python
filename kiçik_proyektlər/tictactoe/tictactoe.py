import tkinter as tk
import os
from typing import List


class TicTacToeButton(tk.Button):
    def __init__(self, master, rc):
        super().__init__(master, borderwidth=0, activebackground="black", bg="black", fg="white", command=self.move)
        self.r, self.c = int(rc[0]), int(rc[1])

    def move(self):
        global finished, move_order, output, win, los
        if not finished:
            key = "X" if move_order == 1 else "O"
            super().configure(text=key, state="disabled", font=KFONT)
            move_order = (move_order + 1) % 2
            b.board[self.r][self.c] = key
            if check_win() in ["X", "O"]:
                finished = True
                output.configure(text=check_win() + " Wins")
                if check_win() == "X":
                    win += 1
                else:
                    los += 1
                fm.update_file(win, los)
            else:
                if " " not in b.board[0] and " " not in b.board[1] and " " not in b.board[2]:
                    finished = True
                    output.configure(text="Nobody wins")


class ResetButton(tk.Button):
    def __init__(self, master):
        super().__init__(master, bg="black", fg="green", font=RFONT, text="Reset Board", command=self.reset_board)

    @staticmethod
    def reset_board():
        global finished, move_order, output, p, b
        finished = False
        move_order = 1
        output.configure(text="")
        b = Places()
        for row in p:
            for tttb in row:
                tttb.configure(text=" ", state="normal")


class Places:
    def __init__(self):
        self.board = [[" ", " ", " "],
                      [" ", " ", " "],
                      [" ", " ", " "]]


class FileManager:
    def __init__(self, canvas):
        self.filename = "./stats.txt"
        self.canvas = canvas

    def update_file(self, wn, ls):
        with open(self.filename, "w") as wf:
            wf.write(f"{wn}\n{ls}")
            tk.Label(self.canvas, text="X:\t{:6}\nO:\t{:6}".format(wn, ls), bg="black", fg="cyan",
                     font=("Calibri", 14, "bold")).place(relx=0.79, rely=0.3, relheight=0.4, relwidth=0.2)

    def read_file(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as wf:
                wf.write("0\n0")

        with open(self.filename, "r") as rf:
            wins = []
            for line in rf:
                line = line.replace("\n", "")
                wins.append(int(line))
            return wins


def check_win():
    for i in range(3):
        if b.board[i][0][0] == b.board[i][1][0] == b.board[i][2][0] and b.board[i][1][0] != " ":
            return b.board[i][0][0]
        if b.board[0][i][0] == b.board[1][i][0] == b.board[2][i][0] and b.board[1][i][0] != " ":
            return b.board[0][i][0]
    if b.board[0][0][0] == b.board[1][1][0] == b.board[2][2][0] and b.board[1][1][0] != " ":
        return b.board[1][1][0]
    if b.board[2][0][0] == b.board[1][1][0] == b.board[0][2][0] and b.board[1][1][0] != " ":
        return b.board[1][1][0]
    return " "


RFONT = ("Calibri", 20, "bold")
KFONT = ("Calibri", 60, "bold")
HEIGHT = 640
WIDTH = 640
win = 0
los = 0
finished = False
move_order = 1

output: tk.Label
p: List[List[TicTacToeButton]] = [[], [], []]
fm: FileManager
b = Places()


def main():
    global p, output, fm, win, los
    root = tk.Tk()
    root.title("Tic Tac Toe")

    canvas = tk.Canvas(root, bg="black", height=HEIGHT, width=WIDTH)
    canvas.pack()

    fm = FileManager(canvas)
    win, los = fm.read_file()

    tk.Label(canvas, text="X:\t{:6}\nO:\t{:6}".format(win, los), bg="black", fg="cyan",
             font=("Calibri", 14, "bold")).place(relx=0.79, rely=0.3, relheight=0.4, relwidth=0.2)

    p[0].append(TicTacToeButton(canvas, "00"))
    p[0].append(TicTacToeButton(canvas, "01"))
    p[0].append(TicTacToeButton(canvas, "02"))
    p[1].append(TicTacToeButton(canvas, "10"))
    p[1].append(TicTacToeButton(canvas, "11"))
    p[1].append(TicTacToeButton(canvas, "12"))
    p[2].append(TicTacToeButton(canvas, "20"))
    p[2].append(TicTacToeButton(canvas, "21"))
    p[2].append(TicTacToeButton(canvas, "22"))

    p[0][0].place(relx=0.325, rely=0.25, relwidth=0.155, relheight=0.1525, anchor="n")
    p[0][1].place(relx=0.497, rely=0.25, relwidth=0.18, relheight=0.1525, anchor="n")
    p[0][2].place(relx=0.669, rely=0.25, relwidth=0.155, relheight=0.1525, anchor="n")
    p[1][0].place(relx=0.325, rely=0.405, relwidth=0.155, relheight=0.183, anchor="n")
    p[1][1].place(relx=0.497, rely=0.405, relwidth=0.18, relheight=0.183, anchor="n")
    p[1][2].place(relx=0.669, rely=0.405, relwidth=0.155, relheight=0.183, anchor="n")
    p[2][0].place(relx=0.325, rely=0.592, relwidth=0.155, relheight=0.153, anchor="n")
    p[2][1].place(relx=0.497, rely=0.592, relwidth=0.18, relheight=0.153, anchor="n")
    p[2][2].place(relx=0.669, rely=0.592, relwidth=0.155, relheight=0.153, anchor="n")

    canvas.create_line(1.625 * HEIGHT / 4, 1 * WIDTH / 4, 1.625 * HEIGHT / 4, 3 * WIDTH / 4, fill="red", width=2)
    canvas.create_line(2.375 * HEIGHT / 4, 1 * WIDTH / 4, 2.375 * HEIGHT / 4, 3 * WIDTH / 4, fill="red", width=2)
    canvas.create_line(1 * HEIGHT / 4, 1.625 * WIDTH / 4, 3 * HEIGHT / 4, 1.625 * WIDTH / 4, fill="red", width=2)
    canvas.create_line(1 * HEIGHT / 4, 2.375 * WIDTH / 4, 3 * HEIGHT / 4, 2.375 * WIDTH / 4, fill="red", width=2)

    output = tk.Label(canvas, bg="black", fg="cyan", font=("Calibri", 20))
    output.place(anchor="n", relx=0.5, rely=0.8, relheight=0.1, relwidth=0.7)

    reset_button = ResetButton(canvas)
    reset_button.place(relx=0.5, anchor="n", rely=0.93, relheight=0.05, relwidth=0.3)

    titlec = tk.Label(canvas, bg="black", fg="cyan", font=("Calibri", 40), text="Tic Tac Toe")
    titlec.place(anchor="n", relx=0.5, rely=0.03, relwidth=0.9, relheight=0.1)

    root.mainloop()


if __name__ == "__main__":
    main()
