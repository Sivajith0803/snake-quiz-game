"""
Snake Quiz Challenge
Author: ChatGPT (template for competition)
How to run: python snake_quiz.py
Dependencies: pygame
"""
import pygame
import random
import sys
import os
import math
import time

# -------------------------
# Config / Constants
# -------------------------
WIDTH, HEIGHT = 800, 640
BLOCK = 20                       # grid block size (px)
COLS, ROWS = WIDTH // BLOCK, HEIGHT // BLOCK
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (10, 10, 10)
NEON_GREEN = (100, 255, 100)
NEON_PINK = (255, 80, 180)
NEON_BLUE = (80, 200, 255)
APPLE_RED = (255, 70, 70)
PANEL_BG = (8, 12, 18, 200)      # used with alpha surfaces

# Files
HIGH_SCORE_FILE = "highscore.txt"
ASSETS_DIR = "assets"            # optional: put sounds here (eat.wav, ding.wav, buzz.wav)

# -------------------------
# Utilities
# -------------------------
def ensure_highscore_file():
    if not os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write("0")

def read_highscore():
    ensure_highscore_file()
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read().strip() or "0")
    except:
        return 0

def write_highscore(v):
    try:
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(int(v)))
    except:
        pass

def load_sound(name):
    path = os.path.join(ASSETS_DIR, name)
    if os.path.exists(path):
        try:
            return pygame.mixer.Sound(path)
        except:
            return None
    return None

# -------------------------
# Question Bank (Python questions)
# -------------------------
QUESTION_BANK = [
    {"q": "What is the output of: print(2**3)?", "opts": ["5", "6", "8", "9"], "a": 2},
    {"q": "Which keyword is used to define a function in Python?", "opts": ["func", "def", "function", "define"], "a": 1},
    {"q": "What data type is returned by input() in Python 3?", "opts": ["int", "str", "float", "list"], "a": 1},
    {"q": "Which operator is used for string concatenation?", "opts": ["+", "&", ".", "*"], "a": 0},
    {"q": "What does 'len' function return for a list?", "opts": ["number of elements", "first element", "last index", "sum of elements"], "a": 0},
    {"q": "Which of these is a tuple?", "opts": ["[1,2]", "(1,2)", "{1,2}", "<1,2>"], "a": 1},
    {"q": "How do you start a comment in Python?", "opts": ["//", "#", "/*", "<!--"], "a": 1},
    {"q": "Which loop is guaranteed to run at least once?", "opts": ["for", "while", "do-while (not in Python)", "None"], "a": 2},
    {"q": "What is correct way to import math module?", "opts": ["import math", "include math", "from math import all", "using math"], "a": 0},
    {"q": "Which method adds an item to a list?", "opts": ["add()", "append()", "push()", "insert_end()"], "a": 1},
    {"q": "What is output: print(10//3)?", "opts": ["3.333", "3", "3.0", "4"], "a": 1},
    {"q": "Which is immutable in Python?", "opts": ["list", "dict", "set", "tuple"], "a": 3},
    {"q": "How to create an empty set?", "opts": ["{}", "set()", "[]", "empty()"], "a": 1},
    {"q": "Which of these is used for exception handling?", "opts": ["try/except", "do/catch", "check/except", "handle/error"], "a": 0},
    {"q": "What is the output: print(bool(0))?", "opts": ["True", "False", "0", "Error"], "a": 1},
    {"q": "Which function converts a string to an integer?", "opts": ["int()", "str()", "float()", "cast()"], "a": 0},
    {"q": "What is list slicing a[1:4] returns?", "opts": ["elements 1 to 4 inclusive", "elements at indices 1,2,3", "only index 4", "error"], "a": 1},
    {"q": "Which is used to iterate over indices and items?", "opts": ["zip()", "range()", "enumerate()", "iteritems()"], "a": 2},
    {"q": "Which built-in creates a range object?", "opts": ["range()", "xrange()", "list()", "loop()"], "a": 0},
    {"q": "How do you open a file for writing?", "opts": ["open('f','r')", "open('f','w')", "open('f','x')", "open('f','a')"], "a": 1},
]

# Shuffle copy so repeats are minimized each run
def get_questions_shuffled():
    q = QUESTION_BANK.copy()
    random.shuffle(q)
    return q

# -------------------------
# Classes: Snake, Apple
# -------------------------
class Snake:
    def __init__(self):
        mid_x, mid_y = COLS // 2, ROWS // 2
        self.positions = [(mid_x, mid_y), (mid_x-1, mid_y), (mid_x-2, mid_y)]
        self.direction = (1, 0)   # moving right by default (dx,dy) in grid coords
        self.grow = 0

    def head(self):
        return self.positions[0]

    def set_direction(self, dx, dy):
        # prevent immediate reverse
        if (dx, dy) == (-self.direction[0], -self.direction[1]):
            return
        self.direction = (dx, dy)

    def move(self):
        hx, hy = self.head()
        dx, dy = self.direction
        new = (hx + dx, hy + dy)
        self.positions.insert(0, new)
        if self.grow > 0:
            self.grow -= 1
        else:
            self.positions.pop()

    def grow_by(self, n=1):
        self.grow += n

    def shrink_tail(self, n=1):
        for _ in range(n):
            if len(self.positions) > 1:
                self.positions.pop()

    def draw(self, surf):
        for i, (x, y) in enumerate(self.positions):
            px, py = x * BLOCK, y * BLOCK
            rect = pygame.Rect(px+1, py+1, BLOCK-2, BLOCK-2)
            if i == 0:
                pygame.draw.rect(surf, NEON_GREEN, rect, border_radius=6)
            else:
                pygame.draw.rect(surf, (40, 180, 80), rect, border_radius=6)

class Apple:
    def __init__(self, snake_positions):
        self.pos = (0,0)
        self.spawn(snake_positions)
        self._pulse = random.random()*10

    def spawn(self, snake_positions):
        while True:
            x = random.randint(1, COLS-2)
            y = random.randint(1, ROWS-2)
            if (x,y) not in snake_positions:
                self.pos = (x, y)
                break

    def draw(self, surf, t):
        x, y = self.pos
        cx = x * BLOCK + BLOCK//2
        cy = y * BLOCK + BLOCK//2
        self._pulse += 0.15
        r = BLOCK//2 - 2 + int(math.sin(self._pulse)*2)
        # glow
        for glow_r in range(3, 8):
            a = max(10, 60 - glow_r*8)
            glow_surf = pygame.Surface((2*glow_r+1, 2*glow_r+1), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 80, 80, a), (glow_r, glow_r), glow_r)
            surf.blit(glow_surf, (cx-glow_r, cy-glow_r), special_flags=pygame.BLEND_PREMULTIPLIED)
        pygame.draw.circle(surf, APPLE_RED, (cx, cy), r)
        pygame.draw.circle(surf, (255,180,180), (cx-4, cy-4), max(2, r//4))

# -------------------------
# UI helpers
# -------------------------
def draw_vertical_gradient(surf, top_color, bottom_color):
    for y in range(HEIGHT):
        ratio = y / (HEIGHT - 1)
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(surf, (r, g, b), (0, y), (WIDTH, y))

def draw_neon_border(surf):
    pygame.draw.rect(surf, NEON_BLUE, (4, 4, WIDTH-8, HEIGHT-8), 3, border_radius=12)

# -------------------------
# Question overlay (blocks game loop until answered)
# -------------------------
def ask_question(screen, clock, fonts, question, timeout=20, sounds=None):
    """
    Displays question overlay; returns True if correct, False if wrong/time-out.
    fonts: dict with 'title' and 'small' fonts
    sounds: dict of optional sounds ('ding','buzz','eat')
    """
    start = time.time()
    selected = None
    width = WIDTH - 160
    height =320
    box_rect = pygame.Rect(80, (HEIGHT - height)//2, width, height)
    btns = []
    btn_w = width - 60
    btn_h = 50
    gap = 16
    # compute button rects
    for i in range(4):
        bx = box_rect.x + 30
        by = box_rect.y + 80 + i*(btn_h + gap)
        btns.append(pygame.Rect(bx, by, btn_w, btn_h))

    # overlay loop
    while True:
        dt = clock.tick(FPS) / 1000.0
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mpos = ev.pos
                for i, br in enumerate(btns):
                    if br.collidepoint(mpos):
                        selected = i
            elif ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_1, pygame.K_KP1):
                    selected = 0
                elif ev.key in (pygame.K_2, pygame.K_KP2):
                    selected = 1
                elif ev.key in (pygame.K_3, pygame.K_KP3):
                    selected = 2
                elif ev.key in (pygame.K_4, pygame.K_KP4):
                    selected = 3

        # draw dim background
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((6, 6, 10, 180))
        screen.blit(overlay, (0,0))

        # box
        box_surf = pygame.Surface((box_rect.w, box_rect.h), pygame.SRCALPHA)
        pygame.draw.rect(box_surf, (18, 20, 26, 240), (0,0,box_rect.w,box_rect.h), border_radius=12)
        # title
        title_text = fonts['title'].render("QUESTION", True, NEON_PINK)
        box_surf.blit(title_text, (20, 12))
        # question text (wrap if needed)
        qlines = wrap_text(question['q'], fonts['small'], box_rect.w - 40)
        for i, line in enumerate(qlines):
            txt = fonts['small'].render(line, True, WHITE)
            box_surf.blit(txt, (20, 42 + i*22))

        # draw buttons
        mx, my = pygame.mouse.get_pos()
        for i, br in enumerate(btns):
            btn_surf = pygame.Surface((br.w, br.h))
            # hover
            if br.collidepoint((mx,my)):
                pygame.draw.rect(btn_surf, (30, 30, 40), (0,0,br.w,br.h), border_radius=8)
                pygame.draw.rect(btn_surf, NEON_BLUE, (0,0,br.w,br.h), 2, border_radius=8)
            else:
                pygame.draw.rect(btn_surf, (24, 26, 34), (0,0,br.w,br.h), border_radius=8)
                pygame.draw.rect(btn_surf, (40,40,48), (0,0,br.w,br.h), 1, border_radius=8)
            opt_text = fonts['small'].render(f"{i+1}. {question['opts'][i]}", True, WHITE)
            btn_surf.blit(opt_text, (12, btn_h//2 - opt_text.get_height()//2))
            box_surf.blit(btn_surf, (br.x - box_rect.x, br.y - box_rect.y))

        # timer
        elapsed = time.time() - start
        remaining = max(0, int(timeout - elapsed))
        timer_text = fonts['small'].render(f"Time: {remaining}s", True, WHITE)
        box_surf.blit(timer_text, (box_rect.w - 110, 12))

        screen.blit(box_surf, (box_rect.x, box_rect.y))
        pygame.display.flip()

        if selected is not None:
            correct_index = question['a']
            if selected == correct_index:
                if sounds and sounds.get('ding'):
                    sounds['ding'].play()
                return True
            else:
                if sounds and sounds.get('buzz'):
                    sounds['buzz'].play()
                return False

        if elapsed >= timeout:
            # time out -> treat as wrong
            if sounds and sounds.get('buzz'):
                sounds['buzz'].play()
            return False

def wrap_text(text, font, max_width):
    """Simple word wrap returning lines list."""
    words = text.split(' ')
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if font.size(test)[0] <= max_width:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

# -------------------------
# Main Game
# -------------------------
def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Quiz Challenge - Machi Edition")
    clock = pygame.time.Clock()

    # fonts
    title_font = pygame.font.SysFont("freesansbold", 34)
    small_font = pygame.font.SysFont("freesansbold", 20)
    score_font = pygame.font.SysFont("freesansbold", 24)

    fonts = {'title': title_font, 'small': small_font}

    # sounds (optional)
    sounds = {
        'eat': load_sound("eat.wav"),
        'ding': load_sound("ding.wav"),
        'buzz': load_sound("buzz.wav")
    }

    # game variables
    snake = Snake()
    apple = Apple(snake.positions)
    moves_per_second = 6.0
    last_move_time = pygame.time.get_ticks()
    score = 0
    highscore = read_highscore()
    question_list = get_questions_shuffled()
    question_index = 0

    running = True
    paused = False
    game_over = False

    while running:
        dt = clock.tick(FPS)
        # input events (still allow quitting)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            if ev.type == pygame.KEYDOWN and not game_over:
                if ev.key in (pygame.K_LEFT, pygame.K_a):
                    snake.set_direction(-1, 0)
                elif ev.key in (pygame.K_RIGHT, pygame.K_d):
                    snake.set_direction(1, 0)
                elif ev.key in (pygame.K_UP, pygame.K_w):
                    snake.set_direction(0, -1)
                elif ev.key in (pygame.K_DOWN, pygame.K_s):
                    snake.set_direction(0, 1)
                elif ev.key == pygame.K_p:
                    paused = not paused

        if not paused and not game_over:
            now = pygame.time.get_ticks()
            interval = int(1000 / moves_per_second)
            if now - last_move_time >= interval:
                last_move_time = now
                snake.move()
                # collisions
                hx, hy = snake.head()
                # wall collision -> game over
                if hx < 0 or hx >= COLS or hy < 0 or hy >= ROWS:
                    game_over = True
                # self collision
                if snake.head() in snake.positions[1:]:
                    game_over = True
                # apple collision
                if snake.head() == apple.pos:
                    # play eat sound
                    if sounds and sounds.get('eat'):
                        sounds['eat'].play()
                    # immediate growth visually
                    snake.grow_by(1)
                    # Ask question - pause main loop until answered
                    if question_index >= len(question_list):
                        question_list = get_questions_shuffled()
                        question_index = 0
                    q = question_list[question_index]
                    question_index += 1
                    correct = ask_question(screen, clock, fonts, q, timeout=20, sounds=sounds)
                    if correct:
                        score += 10
                        moves_per_second = min(20.0, moves_per_second + 0.8)  # increase difficulty
                        # small extra growth for correct answer
                        snake.grow_by(1)
                    else:
                        score = max(0, score - 5)
                        snake.shrink_tail(2)
                        moves_per_second = max(4.0, moves_per_second - 0.6)
                    apple.spawn(snake.positions)

        # Draw
        draw_surface = pygame.Surface((WIDTH, HEIGHT))
        draw_vertical_gradient(draw_surface, (12, 8, 30), (18, 40, 40))
        # playfield grid lines (subtle)
        for gx in range(0, WIDTH, BLOCK):
            pygame.draw.line(draw_surface, (8,8,13), (gx,0), (gx,HEIGHT))
        for gy in range(0, HEIGHT, BLOCK):
            pygame.draw.line(draw_surface, (8,8,13), (0,gy), (WIDTH,gy))
        snake.draw(draw_surface)
        apple.draw(draw_surface, pygame.time.get_ticks()/1000.0)
        # HUD / top panel
        hud = pygame.Surface((WIDTH, 48), pygame.SRCALPHA)
        pygame.draw.rect(hud, (6, 8, 12, 180), (0,0,WIDTH,48))
        score_txt = score_font.render(f"Score: {score}", True, WHITE)
        high_txt = score_font.render(f"High: {highscore}", True, WHITE)
        speed_txt = small_font.render(f"Speed: {moves_per_second:.1f}", True, WHITE)
        hud.blit(score_txt, (14, 8))
        hud.blit(high_txt, (160, 8))
        hud.blit(speed_txt, (320, 12))
        draw_surface.blit(hud, (0,0))

        # border
        draw_neon_border(draw_surface)
        screen.blit(draw_surface, (0,0))

        # Game over overlay
        if game_over:
            if score > highscore:
                highscore = score
                write_highscore(highscore)
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((4,4,6,200))
            screen.blit(overlay, (0,0))
            go_box = pygame.Rect(WIDTH//2 - 240, HEIGHT//2 - 110, 480, 220)
            box_s = pygame.Surface((go_box.w, go_box.h), pygame.SRCALPHA)
            pygame.draw.rect(box_s, (18, 20, 28, 240), (0,0,go_box.w,go_box.h), border_radius=12)
            title = title_font.render("GAME OVER", True, NEON_PINK)
            box_s.blit(title, (go_box.w//2 - title.get_width()//2, 18))
            sc = score_font.render(f"Your score: {score}", True, WHITE)
            box_s.blit(sc, (go_box.w//2 - sc.get_width()//2, 70))
            hint = small_font.render("Press R to restart or Q to quit", True, WHITE)
            box_s.blit(hint, (go_box.w//2 - hint.get_width()//2, 120))
            screen.blit(box_s, (go_box.x, go_box.y))
            pygame.display.flip()

            # wait for restart or quit
            waiting = True
            while waiting:
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    if ev.type == pygame.KEYDOWN:
                        if ev.key == pygame.K_r:
                            # restart game
                            snake = Snake()
                            apple = Apple(snake.positions)
                            moves_per_second = 6.0
                            score = 0
                            question_list = get_questions_shuffled()
                            question_index = 0
                            game_over = False
                            waiting = False
                        elif ev.key == pygame.K_q:
                            pygame.quit(); sys.exit()
                clock.tick(15)
            continue

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
