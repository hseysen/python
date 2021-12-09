import pygame
import sys
import random
import tkinter as tk


SCORE = 0
pygame.font.init()
HEIGHT = 600
WIDTH = 900
MARGIN = 50
cols = 4
rows = 4
board = None
GRID_COLOR = (255, 255, 255)
NUM_ON_BOX_COLOR = (0, 0, 0)
BOARD_BACKGROUND_COLOR = (40, 122, 180)
GAME_BACKGROUND_COLOR = (60, 142, 200)
GUI_ON_RIGHT_COLOR = (20, 29, 30)
SCORE_TEXT_COLOR = (255, 0, 0)
TITLE_TEXT_COLOR = (156, 80, 210)


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


class Board(object):
    def __init__(self):
        self.pos = (MARGIN, MARGIN)
        self.rows = rows
        self.cols = cols
        self.body = [[None, None, None, None],
                     [None, None, None, None],
                     [None, None, None, None],
                     [None, None, None, None]]

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.send_move("left")
                    return
                elif keys[pygame.K_RIGHT]:
                    self.send_move("right")
                    return
                elif keys[pygame.K_UP]:
                    self.send_move("up")
                    return
                elif keys[pygame.K_DOWN]:
                    self.send_move("down")
                    return

    def draw(self, surface):
        size_btw_x = (HEIGHT - 2 * MARGIN + 1) // self.cols
        size_btw_y = (HEIGHT - 2 * MARGIN + 1) // self.rows
        x = self.pos[1]
        y = self.pos[0]
        for l in range(self.cols + 1):
            pygame.draw.line(surface, GRID_COLOR, (x, self.pos[1]), (x, HEIGHT - MARGIN))
            x += size_btw_x
        for l in range(self.rows + 1):
            pygame.draw.line(surface, GRID_COLOR, (self.pos[0], y), (HEIGHT - MARGIN, y))
            y += size_btw_y
        for i in range(len(self.body)):
            for obj in self.body[i]:
                if type(obj) is Box:
                    obj.draw(surface)

    def send_move(self, dirn):
        if dirn.__eq__("left"):
            for i in range(len(self.body)):
                for j in range(1, len(self.body[i])):
                    if type(self.body[i][j]) is Box:
                        self.body[i][j].move("left")
        elif dirn.__eq__("right"):
            for i in range(len(self.body)):
                for j in range(len(self.body[i]) - 2, -1, -1):
                    if type(self.body[i][j]) is Box:
                        self.body[i][j].move("right")
        elif dirn.__eq__("up"):
            for i in range(1, len(self.body)):
                for j in range(len(self.body[i])):
                    if type(self.body[i][j]) is Box:
                        self.body[i][j].move("up")
        elif dirn.__eq__("down"):
            for i in range(len(self.body) - 2, -1, -1):
                for j in range(len(self.body[i])):
                    if type(self.body[i][j]) is Box:
                        self.body[i][j].move("down")
        empty_spot = False
        for i in range(len(self.body)):
            for obj in self.body[i]:
                if obj is None:
                    empty_spot = True
        if empty_spot:
            spawn_box()

    @staticmethod
    def reset():
        global board
        board = Board()
        spawn_box()


class Box(object):
    def __init__(self, yx, value):
        self.color = VAL_TO_COLOR[value]
        self.y = yx[0]
        self.x = yx[1]
        self.w = (HEIGHT - 2 * MARGIN + 1) // board.cols
        self.h = (HEIGHT - 2 * MARGIN + 1) // board.rows
        self.value = value
        self.pos = (MARGIN + self.w * self.x, MARGIN + self.h * self.y)

    def move(self, dirn):
        x = self.x
        y = self.y
        if dirn.__eq__("up"):
            stop = 0
            while y != stop:
                if board.body[y - 1][x] is None:
                    board.body[y][x], board.body[y - 1][x] = board.body[y - 1][x], board.body[y][x]
                    self.y -= 1
                    y -= 1
                    self.pos = (MARGIN + self.w * self.x, MARGIN + self.h * self.y)
                    continue
                elif type(board.body[y - 1][x]) is Box:
                    if self.value == board.body[y - 1][x].value:
                        merge_box(self, board.body[y - 1][x])
                break
        elif dirn.__eq__("down"):
            stop = 3
            while y != stop:
                if board.body[y + 1][x] is None:
                    board.body[y][x], board.body[y + 1][x] = board.body[y + 1][x], board.body[y][x]
                    self.y += 1
                    y += 1
                    self.pos = (MARGIN + self.w * self.x, MARGIN + self.h * self.y)
                    continue
                elif type(board.body[y + 1][x]) is Box:
                    if self.value == board.body[y + 1][x].value:
                        merge_box(self, board.body[y + 1][x])
                break
        elif dirn.__eq__("left"):
            stop = 0
            while x != stop:
                if board.body[y][x - 1] is None:
                    board.body[y][x], board.body[y][x - 1] = board.body[y][x - 1], board.body[y][x]
                    self.x -= 1
                    x -= 1
                    self.pos = (MARGIN + self.w * self.x, MARGIN + self.h * self.y)
                    continue
                elif type(board.body[y][x - 1]) is Box:
                    if self.value == board.body[y][x - 1].value:
                        merge_box(self, board.body[y][x - 1])
                break
        elif dirn.__eq__("right"):
            stop = 3
            while x != stop:
                if board.body[y][x + 1] is None:
                    board.body[y][x], board.body[y][x + 1] = board.body[y][x + 1], board.body[y][x]
                    self.x += 1
                    x += 1
                    self.pos = (MARGIN + self.w * self.x, MARGIN + self.h * self.y)
                    continue
                elif type(board.body[y][x + 1]) is Box:
                    if self.value == board.body[y][x + 1].value:
                        merge_box(self, board.body[y][x + 1])
                break

    def draw(self, surface):
        self.color = VAL_TO_COLOR[self.value]
        pygame.draw.rect(surface, self.color, (self.pos[0] + 1, self.pos[1] + 1, self.w - 1, self.h - 1))
        if self.value >= 1000000:
            size = 30
        elif self.value >= 100000:
            size = 40
        else:
            size = 50
        font = pygame.font.SysFont(None, size, "bold")
        text = font.render(str(self.value), False, NUM_ON_BOX_COLOR)
        surface.blit(text, (self.pos[0] + (self.w - text.get_rect().width) / 2, self.pos[1] +
                            (self.h - text.get_rect().height) / 2))


def merge_box(box_hitter, box_target):
    global SCORE
    box_target.value += box_hitter.value
    SCORE += box_target.value
    board.body[box_hitter.y][box_hitter.x] = None


def spawn_box():
    x = random.randint(0, 3)
    y = random.randint(0, 3)
    while type(board.body[y][x]) is Box:
        x = random.randint(0, 3)
        y = random.randint(0, 3)
    val = random.choice([2, 4])
    o = Box((y, x), val)
    board.body[y][x] = o


def draw_menu(surface):
    pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, (MARGIN, MARGIN, HEIGHT - 2 * MARGIN, HEIGHT - 2 * MARGIN))
    x = pygame.draw.rect(surface, GUI_ON_RIGHT_COLOR, (HEIGHT - MARGIN / 2, MARGIN, WIDTH - HEIGHT, HEIGHT - 2 * MARGIN))
    font = pygame.font.SysFont("Times New Roman", 30, "bold")
    s_text = font.render(f"Score: {SCORE}", False, SCORE_TEXT_COLOR)
    surface.blit(s_text, (HEIGHT - MARGIN / 2 + (x.width - s_text.get_rect().width) / 2, MARGIN + x.height / 2))
    t_font = pygame.font.SysFont("Perpetua", 100, "bold")
    title_text = t_font.render("2048", False, TITLE_TEXT_COLOR)
    surface.blit(title_text, (HEIGHT - MARGIN / 2 + (x.width - title_text.get_rect().width) / 2, MARGIN + x.height / 8))


def redraw_window(surface):
    surface.fill(GAME_BACKGROUND_COLOR)
    draw_menu(surface)
    board.draw(surface)
    pygame.display.update()


def check_game_over():
    for rs in range(len(board.body)):
        for obj in board.body[rs]:
            if obj is None:
                return False
    for i in range(len(board.body)):
        for j in range(1, len(board.body[i])):
            if board.body[i][j].value == board.body[i][j - 1].value:
                return False
    for i in range(len(board.body)):
        for j in range(len(board.body[i]) - 2, -1, -1):
            if board.body[i][j].value == board.body[i][j + 1].value:
                return False
    for i in range(1, len(board.body)):
        for j in range(len(board.body[i])):
            if board.body[i][j].value == board.body[i - 1][j].value:
                return False
    for i in range(len(board.body) - 2, -1, -1):
        for j in range(len(board.body[i])):
            if board.body[i][j].value == board.body[i + 1][j].value:
                return False
    return True


def save_score(name, master):
    global SCORE
    x = name
    while " " in x:
        x = x.replace(" ", "")
    if x.__eq__(""):
        name = "UNNAMED"
    num = 0
    try:
        with open("scores.txt", "r") as file:
            for line in file:
                num += 1
    except FileNotFoundError:
        with open("scores.txt", "w") as file:
            file.write("\t\t\t{:11} | \t\t{:10} \n".format("NAME", "SCORE"))
        with open("scores.txt", "r") as file:
            for line in file:
                num += 1
    with open("scores.txt", "a") as file:
        file.write("{})\t\t{:15} | {:10}\n".format(num, name[:15], SCORE))
    SCORE = 0
    try:
        master.destroy()
    except:
        pass


def mbox():
    r_h = 500
    r_w = 500
    root = tk.Tk()
    root.title("You lost")
    root.attributes("-topmost", True)

    canvas = tk.Canvas(root, height=r_h, width=r_w, bg="orange")
    canvas.pack()

    prompt = tk.Label(canvas, text=f"Score: {SCORE}.\nPlease Enter your name to\nsave your score:", bg="orange",
                      font=("Courier", 22, "bold"))
    prompt.place(anchor="n", relx=0.5, rely=0.2, relwidth=0.9, relheight=0.3)

    entry = tk.Entry(canvas, font=("Calibri", 28, "bold"))
    entry.place(anchor="n", relx=0.5, rely=0.45, relwidth=0.8, relheight=0.1)

    save_button = tk.Button(canvas, font=("Courier", 22, "bold"), text="Save",
                            command=lambda: save_score(entry.get(), root))
    save_button.place(anchor="n", relx=0.5, rely=0.56, relwidth=0.3, relheight=0.1)

    root.mainloop()


def main():
    global board
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    board = Board()
    spawn_box()
    while True:
        pygame.time.delay(50)
        clock.tick(10)
        if check_game_over():
            mbox()
            board.reset()
        board.update()
        redraw_window(window)


if __name__ == "__main__":
    main()
