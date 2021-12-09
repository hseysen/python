import tkinter as tk


class Places:
    def __init__(self):
        self.c11 = False
        self.c12 = False
        self.c13 = False
        self.c21 = False
        self.c22 = False
        self.c23 = False
        self.c31 = False
        self.c32 = False
        self.c33 = False
        self.c11h = [" "]
        self.c12h = [" "]
        self.c13h = [" "]
        self.c21h = [" "]
        self.c22h = [" "]
        self.c23h = [" "]
        self.c31h = [" "]
        self.c32h = [" "]
        self.c33h = [" "]


try:
    with open("stats.txt", "r") as file:
        wins = []
        for line in file:
            line = line.replace("\n", "")
            wins.append(int(line))
except FileNotFoundError:
    with open("stats.txt", "w") as file:
        file.write("0\n0")
    with open("stats.txt", "r") as file:
        wins = []
        for line in file:
            line = line.replace("\n", "")
            wins.append(int(line))

win = wins[0]
los = wins[1]

holder = Places()

sets = [[holder.c11h[0], holder.c12h[0], holder.c13h[0]],
        [holder.c21h[0], holder.c22h[0], holder.c23h[0]],
        [holder.c31h[0], holder.c32h[0], holder.c33h[0]]]

HEIGHT = 640
WIDTH = 640

finished = False

move_order = 1


def update():
    global sets
    sets = [[holder.c11h[0], holder.c12h[0], holder.c13h[0]],
            [holder.c21h[0], holder.c22h[0], holder.c23h[0]],
            [holder.c31h[0], holder.c32h[0], holder.c33h[0]]]


def check_win():
    global sets
    for i in range(3):
        if sets[i][0][0] == sets[i][1][0] == sets[i][2][0] and sets[i][1][0] != " ":
            return sets[i][0][0]
        if sets[0][i][0] == sets[1][i][0] == sets[2][i][0] and sets[1][i][0] != " ":
            return sets[0][i][0]
    if sets[0][0][0] == sets[1][1][0] == sets[2][2][0] and sets[1][1][0] != " ":
        return sets[1][1][0]
    if sets[2][0][0] == sets[1][1][0] == sets[0][2][0] and sets[1][1][0] != " ":
        return sets[1][1][0]
    return " "


def move(where, c, output, window):
    global finished
    global holder
    global move_order
    global win, los
    if not getattr(holder, c) and not finished:
        key = "X" if move_order == 1 else "O"
        where.configure(text=key, state="disabled", font=("Calibri", 60, "bold"))
        move_order = [1, 0][move_order]
        setattr(holder, c, True)
        setattr(holder, c + "h", [key])
        update()
        if check_win() in ["X", "O"]:
            finished = True
            output.configure(text=check_win() + " Wins")
            if check_win() == "X":
                win += 1
            else:
                los += 1
        else:
            if " " not in sets[0] and " " not in sets[1] and " " not in sets[2]:
                finished = True
                output.configure(text="Nobody wins")
    if finished:
        with open("stats.txt", "w") as fresetting:
            fresetting.write(f"{win}\n{los}")
            tk.Label(window, text="X:\t{:6}\nO:\t{:6}".format(win, los), bg="black", fg="cyan",
                     font=("Calibri", 14, "bold")).place(relx=0.79, rely=0.3, relheight=0.4, relwidth=0.2)


def reset_board(output):
    global sets
    global holder
    global finished
    global move_order
    global p11, p12, p13, p21, p22, p23, p31, p32, p33
    p11.configure(text=" ", state="normal")
    p12.configure(text=" ", state="normal")
    p13.configure(text=" ", state="normal")
    p21.configure(text=" ", state="normal")
    p22.configure(text=" ", state="normal")
    p23.configure(text=" ", state="normal")
    p31.configure(text=" ", state="normal")
    p32.configure(text=" ", state="normal")
    p33.configure(text=" ", state="normal")
    output.configure(text="")
    del holder
    holder = Places()
    finished = False
    move_order = 1
    update()


def main():
    global p11, p12, p13, p21, p22, p23, p31, p32, p33
    root = tk.Tk()
    root.title("Tic Tac Toe")

    canvas = tk.Canvas(root, bg="black", height=HEIGHT, width=WIDTH)
    canvas.pack()

    tk.Label(canvas, text="X:\t{:6}\nO:\t{:6}".format(win, los), bg="black", fg="cyan",
             font=("Calibri", 14, "bold")).place(relx=0.79, rely=0.3, relheight=0.4, relwidth=0.2)

    p11 = tk.Button(canvas, borderwidth=0, activebackground="black", bg="black", fg="white",
                    command=lambda: move(p11, "c11", res, canvas))
    p11.place(relx=0.325, rely=0.25, relwidth=0.155, relheight=0.1525, anchor="n")

    p12 = tk.Button(canvas, borderwidth=0, activebackground="black", bg="black", fg="white",
                    command=lambda: move(p12, "c12", res, canvas))
    p12.place(relx=0.497, rely=0.25, relwidth=0.18, relheight=0.1525, anchor="n")

    p13 = tk.Button(canvas, borderwidth=0, activebackground="black", bg="black", fg="white",
                    command=lambda: move(p13, "c13", res, canvas))
    p13.place(relx=0.669, rely=0.25, relwidth=0.155, relheight=0.1525, anchor="n")

    p21 = tk.Button(canvas, borderwidth=0, activebackground="black", bg="black", fg="white",
                    command=lambda: move(p21, "c21", res, canvas))
    p21.place(relx=0.325, rely=0.405, relwidth=0.155, relheight=0.183, anchor="n")

    p22 = tk.Button(canvas, borderwidth=0, activebackground="black", bg="black", fg="white",
                    command=lambda: move(p22, "c22", res, canvas))
    p22.place(relx=0.497, rely=0.405, relwidth=0.18, relheight=0.183, anchor="n")

    p23 = tk.Button(canvas, borderwidth=0, activebackground="black", bg="black", fg="white",
                    command=lambda: move(p23, "c23", res, canvas))
    p23.place(relx=0.669, rely=0.405, relwidth=0.155, relheight=0.183, anchor="n")

    p31 = tk.Button(canvas, borderwidth=0, activebackground="black", bg="black", fg="white",
                    command=lambda: move(p31, "c31", res, canvas))
    p31.place(relx=0.325, rely=0.592, relwidth=0.155, relheight=0.153, anchor="n")

    p32 = tk.Button(canvas, borderwidth=0, activebackground="black", bg="black", fg="white",
                    command=lambda: move(p32, "c32", res, canvas))
    p32.place(relx=0.497, rely=0.592, relwidth=0.18, relheight=0.153, anchor="n")

    p33 = tk.Button(canvas, borderwidth=0, activebackground="black", bg="black", fg="white",
                    command=lambda: move(p33, "c33", res, canvas))
    p33.place(relx=0.669, rely=0.592, relwidth=0.155, relheight=0.153, anchor="n")

    canvas.create_line(1.625 * HEIGHT / 4, 1 * WIDTH / 4, 1.625 * HEIGHT / 4, 3 * WIDTH / 4, fill="red", width=2)
    canvas.create_line(2.375 * HEIGHT / 4, 1 * WIDTH / 4, 2.375 * HEIGHT / 4, 3 * WIDTH / 4, fill="red", width=2)
    canvas.create_line(1 * HEIGHT / 4, 1.625 * WIDTH / 4, 3 * HEIGHT / 4, 1.625 * WIDTH / 4, fill="red", width=2)
    canvas.create_line(1 * HEIGHT / 4, 2.375 * WIDTH / 4, 3 * HEIGHT / 4, 2.375 * WIDTH / 4, fill="red", width=2)

    res = tk.Label(canvas, bg="black", fg="cyan", font=("Calibri", 20))
    res.place(anchor="n", relx=0.5, rely=0.8, relheight=0.1, relwidth=0.7)

    reset_button = tk.Button(canvas, bg="black", fg="green", font=("Calibri", 20, "bold"), text="Reset Board",
                             command=lambda: reset_board(res))
    reset_button.place(relx=0.5, anchor="n", rely=0.93, relheight=0.05, relwidth=0.3)

    titlec = tk.Label(canvas, bg="black", fg="cyan", font=("Calibri", 40), text="Tic Tac Toe")
    titlec.place(anchor="n", relx=0.5, rely=0.03, relwidth=0.9, relheight=0.1)

    root.mainloop()


if __name__ == "__main__":
    main()
