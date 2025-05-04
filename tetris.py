import pygame
import copy
import random
import csv
from datetime import datetime

pygame.init()
pygame_screen = pygame.display.set_mode((800, 800))
font = pygame.font.SysFont("Arial", 30)
big_font = pygame.font.SysFont("Arial", 50)
clock = pygame.time.Clock()

DROP_EVENT = pygame.USEREVENT + 1
starting_speed = 500
pygame.time.set_timer(DROP_EVENT, starting_speed)


class GameStats:
    def __init__(self):
        self._score = 0
        self.level = 0
        self.lines_cleared = 0

    def update(self, cleared_lines):
        _score_table = [0, 100, 300, 500, 800]
        self._score += _score_table[cleared_lines] if cleared_lines < len(_score_table) else 1000
        self.lines_cleared += cleared_lines
        self.level = self.lines_cleared // 10

    def get_speed(self, base_speed):
        return max(100, base_speed - self.level * 40)


class Field:
    def __init__(self):
        self.screen = [[0 for _ in range(10)] for _ in range(20)]
        self.static_screen = copy.deepcopy(self.screen)
        self.positions = []
        self.stats = GameStats()

    def pygame_draw(self, score, next_piece, font, nickname, show_next=True):
        COLOR_MAP = {
    1: (180, 60, 60),   
    2: (60, 60, 180),     
    3: (60, 180, 60),     
    4: (200, 200, 80),    
    5: (180, 60, 180),    
    6: (60, 180, 180),    
    7: (200, 120, 60)     
}

        pygame_screen.fill((0, 0, 0))

        for y in range(21):
            pygame.draw.line(pygame_screen, (100, 100, 100), (10, y * 30 + 10), (310, y * 30 + 10))
        for x in range(11):
            pygame.draw.line(pygame_screen, (100, 100, 100), (x * 30 + 10, 10), (x * 30 + 10, 610))
        pygame.draw.rect(pygame_screen, (255, 255, 255), (10, 10, 300, 600), 2)

        for r in range(20):
            for c in range(10):
                value = self.screen[r][c]
                if value != 0:
                    color = COLOR_MAP.get(value, (255, 255, 255))
                    pygame.draw.rect(pygame_screen, color, (c * 30 + 11, r * 30 + 11, 28, 28))

        label = f"{nickname} | Score: {score}"
        text_surface = font.render(label, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.topleft = (350, 40)

        padding_x = 10
        padding_y = 6
        box_rect = pygame.Rect(
            text_rect.left - padding_x,
            text_rect.top - padding_y,
            text_rect.width + padding_x * 2,
            text_rect.height + padding_y * 2
        )
        pygame.draw.rect(pygame_screen, (255, 255, 255), box_rect, 2)
        pygame_screen.blit(text_surface, text_rect.topleft)

        if show_next:
            pygame.draw.rect(pygame_screen, (200, 200, 200), (350, 100, 100, 100), 2)
            for i, row in enumerate(next_piece):
                for j, cell in enumerate(row):
                    if cell:
                        color = COLOR_MAP.get(cell, (255, 255, 255))
                        pygame.draw.rect(pygame_screen, color, (360 + j * 20, 110 + i * 20, 18, 18))

    def terminal_draw(self, tetromino, x, y):
        print("\n \n \n \n")
        self.get_dxdy(tetromino, x, y)
        for row in self.screen:
            print(row)

    def get_dxdy(self, tetromino, x, y):
        self.positions.clear()
        for i, row in enumerate(tetromino):
            for j, cell in enumerate(row):
                if cell:
                    dx = x + j
                    dy = y + i
                    self.positions.append(dx)
                    self.positions.append(dy)
        return self.positions

    def update_position(self, tetromino, x, y):
        self.screen = copy.deepcopy(self.static_screen)
        self.get_dxdy(tetromino, x, y)
        for i in range(len(self.positions) // 2):
            dx = self.positions[i * 2]
            dy = self.positions[i * 2 + 1]
            if 0 <= dy < 20 and 0 <= dx < 10:
                tx = dx - x
                ty = dy - y
                if 0 <= ty < len(tetromino) and 0 <= tx < len(tetromino[0]):
                    self.screen[dy][dx] = tetromino[ty][tx]

    def check_colision_y(self):
        for i in range(len(self.positions) // 2):
            dx = self.positions[i * 2]
            dy = self.positions[i * 2 + 1]
            if dy >= 19 or self.static_screen[dy + 1][dx] != 0:
                return True
        return False

    def check_collision_x(self, direction):
        for i in range(len(self.positions) // 2):
            x = self.positions[i * 2]
            y = self.positions[i * 2 + 1]
            new_x = x + direction
            if new_x < 0 or new_x >= 10 or self.static_screen[y][new_x] != 0:
                return False
        return True

    def can_place(self, tetromino, x, y):
        for i, row in enumerate(tetromino):
            for j, cell in enumerate(row):
                if cell:
                    dx = x + j
                    dy = y + i
                    if dx < 0 or dx >= 10 or dy < 0 or dy >= 20 or self.static_screen[dy][dx] != 0:
                        return False
        return True

    def clear_full_lines(self):
        new_screen = []
        cleared_lines = 0
        for row in self.static_screen:
            if all(cell != 0 for cell in row):
                cleared_lines += 1
            else:
                new_screen.append(row)
        for _ in range(cleared_lines):
            new_screen.insert(0, [0 for _ in range(10)])
        self.static_screen = new_screen
        return cleared_lines

    def update_static_screen(self):
        self.static_screen = copy.deepcopy(self.screen)


class Tetromino:
    def __init__(self):
        self.shapes = {
            1: self._O, 2: self._I, 3: self._T,
            4: self._L, 5: self._J, 6: self._Z, 7: self._S
        }

    def create(self, number):
        return self.shapes.get(number, self._O)()

    def _O(self):
        return [[1, 1], [1, 1]]

    def _I(self):
        return [[1, 1, 1, 1]]

    def _T(self):
        return [[0, 1, 0], [1, 1, 1]]

    def _L(self):
        return [[1, 0], [1, 0], [1, 1]]

    def _J(self):
        return [[0, 1], [0, 1], [1, 1]]

    def _Z(self):
        return [[1, 1, 0], [0, 1, 1]]

    def _S(self):
        return [[0, 1, 1], [1, 1, 0]]


class ColorChanger(Tetromino):
    def create_colored(self, number):
        shape = super().create(number)
        return [[number if cell else 0 for cell in row] for row in shape]

    def rotate(self, shape):
        return [list(row) for row in zip(*shape[::-1])]


def get_nickname():
    _nickname = ""
    active = True
    while active:
        pygame_screen.fill((0, 0, 0))
        prompt = big_font.render("Enter your name:", True, (255, 255, 255))
        name_text = font.render(_nickname + "_", True, (255, 255, 255))
        prompt_rect = prompt.get_rect(center=(400, 300))
        name_rect = name_text.get_rect(center=(400, 360))
        pygame_screen.blit(prompt, prompt_rect)
        pygame_screen.blit(name_text, name_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and _nickname:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    _nickname = _nickname[:-1]
                elif len(_nickname) < 12 and event.unicode.isprintable():
                    _nickname += event.unicode
    return _nickname


def game_over_screen(score, nickname):
    pygame_screen.fill((0, 0, 0))

    highscore = 0
    try:
        with open("scores.csv", mode="r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 3:
                    try:
                        past_score = int(row[2])
                        if past_score > highscore:
                            highscore = past_score
                    except ValueError:
                        pass
    except FileNotFoundError:
        pass

    with open("scores.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), nickname, score])

    is_new_highscore = score > highscore
    game_over_text = big_font.render("Game Over", True, (255, 0, 0))
    final_score = font.render(f"Your score: {score}", True, (255, 255, 255))
    prompt = font.render("Press Enter to Exit", True, (255, 255, 255))

    if is_new_highscore:
        congrats = font.render("New High Score!", True, (0, 255, 0))
    else:
        congrats = font.render(f"High Score: {highscore}", True, (200, 200, 200))

    pygame_screen.blit(game_over_text, game_over_text.get_rect(center=(400, 280)))
    pygame_screen.blit(final_score, final_score.get_rect(center=(400, 330)))
    pygame_screen.blit(congrats, congrats.get_rect(center=(400, 370)))
    pygame_screen.blit(prompt, prompt.get_rect(center=(400, 420)))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                pygame.quit()
                exit()


def main():
    nickname = get_nickname()
    tetrominoes = ColorChanger()
    pf = Field()

    lock_delay, drop_counter = 0, 0
    drop_pressed = False
    current_piece_type = random.randint(1, 7)
    current_piece = tetrominoes.create_colored(current_piece_type)
    next_piece_type = random.randint(1, 7)
    next_piece = tetrominoes.create_colored(next_piece_type)
    x, y = 5, 0

    while True:
        clock.tick(60)
        drop = False
        hard_dropped = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and pf.check_collision_x(-1):
                    x -= 1
                elif event.key == pygame.K_RIGHT and pf.check_collision_x(1):
                    x += 1
                elif event.key == pygame.K_DOWN:
                    drop_pressed = True
                elif event.key == pygame.K_SPACE:
                    while not pf.check_colision_y():
                        y += 1
                        pf.update_position(current_piece, x, y)
                    pf.update_position(current_piece, x, y)
                    hard_dropped = True
                elif event.key == pygame.K_UP:
                    rotated = tetrominoes.rotate(current_piece)
                    for offset in [0, -1, 1, -2, 2]:
                        if pf.can_place(rotated, x + offset, y):
                            x += offset
                            current_piece = rotated
                            break

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    drop_pressed = False

            elif event.type == DROP_EVENT:
                drop = True

        if drop_pressed:
            drop_counter += 1
            if drop_counter >= 2:
                if not pf.check_colision_y():
                    y += 1
                drop_counter = 0
        elif drop:
            if not pf.check_colision_y():
                y += 1

        pf.update_position(current_piece, x, y)

        if pf.check_colision_y():
            if hard_dropped:
                lock_delay = 100
            else:
                lock_delay += 1

            if lock_delay > 15:
                pf.update_static_screen()
                cleared = pf.clear_full_lines()
                pf.stats.update(cleared)
                new_speed = pf.stats.get_speed(starting_speed)
                pygame.time.set_timer(DROP_EVENT, new_speed)

                x, y = 5, 0
                current_piece_type = next_piece_type
                current_piece = next_piece
                next_piece_type = random.randint(1, 7)
                next_piece = tetrominoes.create_colored(next_piece_type)
                lock_delay = 0

                if not pf.can_place(current_piece, x, y):
                    pf.update_position(current_piece, x, y)
                    pf.pygame_draw(pf.stats._score, next_piece, font, nickname)
                    pygame.display.update()
                    pygame.time.delay(1000)
                    game_over_screen(pf.stats._score, nickname)
        else:
            lock_delay = 0

        pf.pygame_draw(pf.stats._score, next_piece, font, nickname)
        pygame.display.update()
        pf.terminal_draw(current_piece, x, y)


if __name__ == "__main__":
    main()
