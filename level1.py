import random
import pygame
import os
import sys

score = 0
notworking = False
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def run_program(self, screen):
        for i in range(30):
            all_sprites.draw(screen)
            all_sprites.update()
            pygame.display.flip()
            clock.tick(11)

    def run_program2(self, screen):
        for i in range(9):
            all_sprites.draw(screen)
            all_sprites.update()
            pygame.display.flip()
            clock.tick(11)


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # рисуем клеточное поле
    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(255, 255, 255),
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                  self.cell_size,
                                  self.cell_size), 1)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # cell - кортеж (x, y)
    def on_click(self, cell):
        # заглушка для реальных игровых полей
        pass

    # проверка нажатия именно на клеточное поле
    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos, screen):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell, screen)


class Minesweeper(Board):
    def __init__(self, width, height, n):
        super().__init__(width, height)
        self.board = [[-1] * width for _ in range(height)]
        i = 0

        while i < n:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.board[y][x] == -1:
                self.board[y][x] = 10
                i += 1

    # рисуем красные клетки(бомбы) и цифры в конце игры
    def draw_red(self, screen):
        yesno = False
        global notworking
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 11:
                    pygame.draw.rect(screen, pygame.Color("red"),
                                     (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                      self.cell_size,
                                      self.cell_size))
                    yesno = True

        for y in range(self.height):
            for x in range(self.width):
                if yesno:
                    if self.board[y][x] != 11:
                        font = pygame.font.Font(None, self.cell_size)
                        text = font.render(str(self.board[y][x]), 1, (100, 255, 100))
                        screen.blit(text, (
                            x * self.cell_size + self.left + 10, y * self.cell_size + self.top + 5))
        if yesno:
            notworking = True
            return notworking

    # изменение списка с содержанием цифр(сколько бомб вокруг клетки)
    def numb(self):
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                if self.board[y][x] != 10:
                    s = 0
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                                continue
                            if self.board[y + dy][x + dx] == 10:
                                s += 1
                    self.board[y][x] = s

    # при единичном нажатии выводим цифру
    def open_cell(self, cell, screen):
        global score
        x, y = cell
        if self.board[y][x] >= 0 and self.board[y][x] != 10 and self.board[y][x] != 11:
            font = pygame.font.Font(None, self.cell_size)
            text = font.render(str(self.board[y][x]), 1, (100, 255, 100))
            screen.blit(text, (x * self.cell_size + self.left + 10, y * self.cell_size + self.top + 5))
            score += 1

        if self.board[y][x] == 10:
            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    if self.board[i][j] == 10:
                        self.board[i][j] = 11
        return score

    def on_click(self, cell, screen):
        self.open_cell(cell, screen)

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(255, 255, 255), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                    self.cell_size), 1)


def main():
    global score
    pygame.init()
    size = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Cапёр')
    board = Minesweeper(5, 5, 5)  # длина, ширина, кол-во бомб
    board.set_view(10, 10, 96)  # отступ справа, сверху, размер клетки
    board.numb()
    # Включено ли обновление поля

    time_on = False

    ticks = 0
    global notworking

    running = True
    screen.fill((0, 0, 0))
    board.render(screen)
    while running:
        if score < 20 and not notworking:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    board.get_click(event.pos, screen)
                    board.draw_red(screen)
            board.render(screen)
            pygame.display.flip()
            clock.tick(50)
            ticks += 1
        else:
            break

    if score == 20:
        f = open("results.txt", 'a')
        print(f.write(f'{str(score)}\n'))
        f.close()
        running = True
        runn = AnimatedSprite(load_image('zv.png'), 5, 6, 0, 0)
        runn.run_program(screen)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            f = open("resuls.txt", encoding="utf8")
            for i in range(1):
                lascore = f.readlines()
                lscore = lascore[-2].rstrip('\n')
                screen = pygame.display.set_mode((500, 500))
                screen.fill((0, 0, 0))
                font1 = pygame.font.Font(None, 70)
                font2 = pygame.font.Font(None, 70)
                font3 = pygame.font.Font(None, 70)
                text1 = font1.render(str("You win!"), 25, (92, 255, 92), (1, 41, 13))
                text2 = font2.render(str(f"Your score: {score}"), 25, (92, 255, 92), (1, 41, 13))
                text3 = font3.render(str(f"Your last score: {lscore}"), 25, (92, 255, 92), (1, 41, 13))
                screen.blit(text1, (145, 170))
                screen.blit(text2, (85, 230))
                screen.blit(text3, (45, 290))
            pygame.display.flip()

    if score != 20:
        f = open("results.txt", 'a')
        print(f.write(f'{str(score)}\n'))
        f.close()
        runn = AnimatedSprite(load_image('v.jpg'), 3, 3, 0, 0)
        runn.run_program2(screen)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            f = open("results.txt", encoding="utf8")
            for i in range(1):
                lascore = f.readlines()
                lscore = lascore[-2].rstrip('\n')
                screen = pygame.display.set_mode((500, 500))
                screen.fill((0, 0, 0))
                font1 = pygame.font.Font(None, 70)
                font2 = pygame.font.Font(None, 70)
                font3 = pygame.font.Font(None, 70)
                text1 = font1.render(str("You lose!"), 25, (92, 255, 92), (1, 41, 13))
                text2 = font2.render(str(f"Your score: {score}"), 25, (92, 255, 92), (1, 41, 13))
                text3 = font3.render(str(f"Your last score: {lscore}"), 25, (92, 255, 92), (1, 41, 13))
                screen.blit(text1, (145, 170))
                screen.blit(text2, (85, 230))
                screen.blit(text3, (45, 290))
            pygame.display.flip()


pygame.quit()

if __name__ == '__main__':
    main()