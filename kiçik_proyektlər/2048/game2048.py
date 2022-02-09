import pygame
import sys
import os
import random
import tkinter as tk
from typing import List


pygame.font.init()
VAL_TO_COLOR = {
    2: (0, 255, 0),
    4: (0, 255, 127),
    8: (0, 250, 154),
    16: (124, 252, 0),
    32: (127, 255, 0),
    64: (50, 205, 50),
    128: (173, 255, 47),
    256: (0, 128, 0),
    512: (20, 132, 42),
    1024: (34, 139, 34),
    2048: (0, 100, 0),
    4096: (154, 205, 50),
    8192: (60, 179, 113),
    16384: (46, 139, 87),
    32768: (143, 188, 143),
    65536: (107, 142, 35),
    131072: (85, 107, 47),
    262144: (128, 128, 0)
}


class Board:
    HEIGHT = 600
    WIDTH = 900
    MARGIN = 50
    ROWS = 4
    COLS = 4

    def __init__(self):
        self.pos = (Board.MARGIN, Board.MARGIN)
        self.body: List[List[Slot]] = [[], [], [], []]

        for i in range(Board.ROWS):
            for j in range(Board.COLS):
                self.body[j].append(Slot(i, j))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.send_move(1)
                return
            elif keys[pygame.K_RIGHT]:
                self.send_move(3)
                return
            elif keys[pygame.K_UP]:
                self.send_move(0)
                return
            elif keys[pygame.K_DOWN]:
                self.send_move(2)
                return

    def draw(self, surface):
        size_btw_x = (Board.HEIGHT - 2 * Board.MARGIN + 1) // Board.COLS
        size_btw_y = (Board.HEIGHT - 2 * Board.MARGIN + 1) // Board.ROWS
        x = self.pos[1]
        y = self.pos[0]
        for lin in range(Board.COLS + 1):
            pygame.draw.line(surface, GRID_COLOR, (x, self.pos[1]), (x, Board.HEIGHT - Board.MARGIN))
            x += size_btw_x
        for lin in range(Board.ROWS + 1):
            pygame.draw.line(surface, GRID_COLOR, (self.pos[0], y), (Board.HEIGHT - Board.MARGIN, y))
            y += size_btw_y
        for i in range(len(self.body)):
            for slot in self.body[i]:
                if type(slot.occupying_box) is Box:
                    slot.occupying_box.draw(surface)

    def send_move(self, dirn):
        i_start = [1, 0, len(self.body) - 2, 0][dirn]
        i_end = [len(self.body), len(self.body), -1, len(self.body)][dirn]
        i_incr = [1, 1, -1, 1][dirn]

        j_start = [0, 1, 0, len(self.body) - 2][dirn]
        j_end = [len(self.body), len(self.body), len(self.body), -1][dirn]
        j_incr = [1, 1, 1, -1][dirn]

        for i in range(i_start, i_end, i_incr):
            for j in range(j_start, j_end, j_incr):
                if type(self.body[i][j].occupying_box) is Box:
                    self.body[i][j].occupying_box.move(dirn)

        empty_spot = False
        for i in range(len(self.body)):
            for slot in self.body[i]:
                if slot.occupying_box is None:
                    empty_spot = True
        if empty_spot:
            self.spawn_box()

    def spawn_box(self):
        x = random.randint(0, 3)
        y = random.randint(0, 3)
        while type(self.body[y][x].occupying_box) is Box:
            x = random.randint(0, 3)
            y = random.randint(0, 3)
        val = random.choice([2, 4])
        board.body[y][x].occupying_box = Box(x, y, val)

    @staticmethod
    def reset():
        global board
        board = Board()
        board.spawn_box()


class Slot:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.occupying_box = None


class Box:
    def __init__(self, x, y, value):
        self.color = VAL_TO_COLOR[value]
        self.x = x
        self.y = y
        self.w = (Board.HEIGHT - 2 * Board.MARGIN + 1) // Board.COLS
        self.h = (Board.HEIGHT - 2 * Board.MARGIN + 1) // Board.ROWS
        self.value = value
        self.pos = (Board.MARGIN + self.w * self.x, Board.MARGIN + self.h * self.y)

    def move(self, dirn):
        x1 = self.x
        y1 = self.y

        stop = [0, 0, 3, 3][dirn]
        deltx = [0, -1, 0, 1][dirn]
        delty = [-1, 0, 1, 0][dirn]
        newpos = lambda x, y: (Board.MARGIN + self.w * x, Board.MARGIN + self.h * y)

        if dirn % 2 == 0:
            while y1 != stop:
                if board.body[y1 + delty][x1 + deltx].occupying_box is None:
                    board.body[y1][x1].occupying_box, board.body[y1 + delty][x1 + deltx].occupying_box = board.body[y1 + delty][x1 + deltx].occupying_box, board.body[y1][x1].occupying_box
                    self.y += delty
                    y1 += delty
                    self.pos = newpos(self.x, self.y)
                elif type(board.body[y1 + delty][x1 + deltx].occupying_box) is Box:
                    if self.value == board.body[y1 + delty][x1 + deltx].occupying_box.value:
                        GameManager.merge_box(self, board.body[y1 + delty][x1 + deltx].occupying_box)
                    break
        else:
            while x1 != stop:
                if board.body[y1 + delty][x1 + deltx].occupying_box is None:
                    board.body[y1][x1].occupying_box, board.body[y1 + delty][x1 + deltx].occupying_box = board.body[y1 + delty][x1 + deltx].occupying_box, board.body[y1][x1].occupying_box
                    self.x += deltx
                    x1 += deltx
                    self.pos = newpos(self.x, self.y)
                elif type(board.body[y1 + delty][x1 + deltx].occupying_box) is Box:
                    if self.value == board.body[y1 + delty][x1 + deltx].occupying_box.value:
                        GameManager.merge_box(self, board.body[y1 + delty][x1 + deltx].occupying_box)
                    break

    def draw(self, surface):
        self.color = VAL_TO_COLOR[self.value]
        pygame.draw.rect(surface, self.color, (self.pos[0] + 1, self.pos[1] + 1, self.w - 1, self.h - 1))
        font = pygame.font.SysFont("Arial", 50, "bold")
        text = font.render(str(self.value), False, NUM_ON_BOX_COLOR)
        surface.blit(text, (self.pos[0] + (self.w - text.get_rect().width) / 2, self.pos[1] + (self.h - text.get_rect().height) / 2))


class GameManager:
    @staticmethod
    def merge_box(box_hitter, box_target):
        global SCORE
        box_target.value += box_hitter.value
        SCORE += box_target.value
        board.body[box_hitter.y][box_hitter.x].occupying_box = None

    @staticmethod
    def draw_menu(surface):
        pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, (Board.MARGIN, Board.MARGIN, Board.HEIGHT - 2 * Board.MARGIN, Board.HEIGHT - 2 * Board.MARGIN))
        x = pygame.draw.rect(surface, GUI_ON_RIGHT_COLOR, (Board.HEIGHT - Board.MARGIN / 2, Board.MARGIN, Board.WIDTH - Board.HEIGHT, Board.HEIGHT - 2 * Board.MARGIN))
        font = pygame.font.SysFont("Times New Roman", 30, "bold")
        s_text = font.render(f"Score: {SCORE}", False, SCORE_TEXT_COLOR)
        surface.blit(s_text, (Board.HEIGHT - Board.MARGIN / 2 + (x.width - s_text.get_rect().width) / 2, Board.MARGIN + x.height / 2))
        t_font = pygame.font.SysFont("Perpetua", 100, "bold")
        title_text = t_font.render("2048", False, TITLE_TEXT_COLOR)
        surface.blit(title_text, (Board.HEIGHT - Board.MARGIN / 2 + (x.width - title_text.get_rect().width) / 2, Board.MARGIN + x.height / 8))

    @staticmethod
    def redraw_window(surface):
        surface.fill(GAME_BACKGROUND_COLOR)
        GameManager.draw_menu(surface)
        board.draw(surface)
        pygame.display.update()

    @staticmethod
    def check_game_over():
        for rs in range(len(board.body)):
            for slot in board.body[rs]:
                if slot.occupying_box is None:
                    return False
        for i in range(len(board.body)):
            for j in range(1, len(board.body[i])):
                if board.body[i][j].occupying_box.value == board.body[i][j - 1].occupying_box.value:
                    return False
        for i in range(len(board.body)):
            for j in range(len(board.body[i]) - 2, -1, -1):
                if board.body[i][j].occupying_box.value == board.body[i][j + 1].occupying_box.value:
                    return False
        for i in range(1, len(board.body)):
            for j in range(len(board.body[i])):
                if board.body[i][j].occupying_box.value == board.body[i - 1][j].occupying_box.value:
                    return False
        for i in range(len(board.body) - 2, -1, -1):
            for j in range(len(board.body[i])):
                if board.body[i][j].occupying_box.value == board.body[i + 1][j].occupying_box.value:
                    return False
        return True

    @staticmethod
    def reset_score(event=None):
        global SCORE
        SCORE = 0


class FileManager:
    FILE_HEADING = "\t\t\t{:11} | \t\t{:10} \n".format("NAME", "SCORE")
    SCORE_FORMAT = "{})\t\t{:15} | {:10}\n"

    def __init__(self, master):
        self.filename = "./scores.txt"
        self.master = master

    def save_score(self, name):
        if name.isspace():
            name = "UNNAMED"

        if not os.path.exists(self.filename):
            with open(self.filename, "w") as file:
                file.write(FileManager.FILE_HEADING)

        num = 0
        with open(self.filename, "r") as file:
            for _ in file:
                num += 1

        with open(self.filename, "a") as file:
            file.write(FileManager.SCORE_FORMAT.format(num, name[:15], SCORE))
        GameManager.reset_score()

        try:
            self.master.destroy()
        except Exception:
            pass


def gameover_screen():
    r_h = 500
    r_w = 500
    root = tk.Tk()
    root.title("Game Over")
    root.attributes("-topmost", True)
    root.bind('<Destroy>', GameManager.reset_score)
    fm = FileManager(root)

    canvas = tk.Canvas(root, height=r_h, width=r_w, bg="orange")
    canvas.pack()

    prompt = tk.Label(canvas, text=f"Score: {SCORE}.\nPlease Enter your name to\nsave your score:", bg="orange", font=("Courier", 22, "bold"))
    prompt.place(anchor="n", relx=0.5, rely=0.2, relwidth=0.9, relheight=0.3)

    entry = tk.Entry(canvas, font=("Calibri", 28, "bold"))
    entry.place(anchor="n", relx=0.5, rely=0.45, relwidth=0.8, relheight=0.1)

    save_button = tk.Button(canvas, font=("Courier", 22, "bold"), text="Save", command=lambda: fm.save_score(entry.get()))
    save_button.place(anchor="n", relx=0.5, rely=0.56, relwidth=0.3, relheight=0.1)

    root.mainloop()


SCORE = 0
GRID_COLOR = (255, 255, 255)
NUM_ON_BOX_COLOR = (0, 0, 0)
BOARD_BACKGROUND_COLOR = (40, 122, 180)
GAME_BACKGROUND_COLOR = (60, 142, 200)
GUI_ON_RIGHT_COLOR = (20, 29, 30)
SCORE_TEXT_COLOR = (255, 0, 0)
TITLE_TEXT_COLOR = (156, 80, 210)
board: Board


def main():
    global board
    window = pygame.display.set_mode((Board.WIDTH, Board.HEIGHT))
    clock = pygame.time.Clock()
    board = Board()
    board.spawn_box()
    while True:
        pygame.time.delay(50)
        clock.tick(10)
        if GameManager.check_game_over():
            gameover_screen()
            board.reset()
        board.update()
        GameManager.redraw_window(window)


if __name__ == "__main__":
    main()
