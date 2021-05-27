import pygame as pg
import sys
import random
from time import *
from setting import *

# 시작할 때 누른 곳이 0 덩어리
# 클리어, 게임 오버 시 텀 둬서 바로 실행 안되게 하기
# 클리어, 게임 오버 이펙트 변경(지뢰 보이게 하기 등)
# 게임 새로 시작 만들기
# 깃발 그림 수정
# 깃발 다시 없애기 기능
# 숫자 누르기, 마우스 가운데 버튼 기능 구현
# 숫자별 색, 숫자 위치 지정
# 시간을 점수로
# 시작 화면 꾸미기
# 옵션등 생성

class game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SIZE)
        self.title = pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("arial", 48, True, False)
        self.m_font = pg.font.SysFont("arial", 30, True, False)
        self.new()

    def new(self):
        self.running = True
        self.state = 1 #select, ingame, option, gameover, clear
        self.level = [0, 0, 0, 0] #level, row, col, mine, block size
        self.screen.fill(WHITE)
        self.clicked = pg.image.load("clicked.png")
        self.unclicked = pg.image.load("unclicked.png")
        self.mine = pg.image.load("mine.png")
        self.flag = pg.image.load("flag.png")
        self.count = [0, 0, 0] #count, score, real score
        self.pos = [0, 0]
        self.check = []
        self.check_2 = []
        self.open = []
        self.first_click = [0, 0]
        
    def select(self):
        self.mouse_state = self.mouse_location()
        self.text_level = self.font.render("Level", True, BLACK)
        self.text_easy = self.font.render("easy", True, BLACK)
        self.text_normal = self.font.render("normal", True, BLACK)
        self.text_hard = self.font.render("hard", True, BLACK)
        if self.mouse_pre[0] == 0:
            if self.mouse_state == 1:
                self.text_easy = self.font.render("easy", True, RED)
            elif self.mouse_state == 2:
                self.text_normal = self.font.render("normal", True, RED)
            elif self.mouse_state == 3:
                self.text_hard = self.font.render("hard", True, RED)
            self.screen.blit(self.text_easy, [300, 120])
            self.screen.blit(self.text_normal, [300, 250])
            self.screen.blit(self.text_hard, [300, 380])
            self.screen.blit(self.text_level, [80, 250])
            pg.display.update()
        
        elif self.mouse_pre[0] == 1: #set level
            if self.mouse_state == 1:
                self.level = [1, 12, 10, 2, 50]
            elif self.mouse_state == 2:
                self.level = [2, 22, 18, 50, 25]
            elif self.mouse_state == 3:
                self.level = [3, 27, 22, 99, 20]
        
        if self.level[0] != 0:
            sleep(0.2)
            self.start()
                
    def start(self):
        self.s_font = pg.font.SysFont("arial", int(self.level[4] / 1.5), True, False)
        self.clicked = pg.transform.scale(self.clicked, [self.level[4], self.level[4]])
        self.unclicked = pg.transform.scale(self.unclicked, [self.level[4], self.level[4]])
        self.mine = pg.transform.scale(self.mine, [self.level[4], self.level[4]])
        self.flag = pg.transform.scale(self.flag, [self.level[4], self.level[4]])
        self.board = [[0 for i in range(self.level[2] + 4)] for j in range(self.level[1] + 4)]
        self.board_state = [[0 for i in range(self.level[2] + 4)] for j in range(self.level[1] + 4)]
        for i in range(self.level[3]): #spown mine
            x = random.randint(1, self.level[1] - 2)
            y = random.randint(1, self.level[2] - 2)
            while True:
                if self.board[x][y] < 0 or [self.pos[0], self.pos[1]] == [x, y]:
                    x = random.randint(1, self.level[1] - 2)
                    y = random.randint(1, self.level[2] - 2)
                elif self.board[x][y] == 0 and [self.pos[0], self.pos[1]] != [x, y]:
                    break
            self.board[x][y] = -1
            
        for i in range(1, self.level[1]): #count around mine
            for j in range(1, self.level[2]):
                if self.board[i][j] >= 0:
                    for x in range(-1, 2):
                        for y in range(-1, 2):
                            if self.board[i+x][j+y] < 0:
                                self.count[0] += 1
                    self.board[i][j] = self.count[0]
                    self.count[0] = 0
        self.state = 2

    def run(self):
        if self.state == 1: #select
            self.select()
            
        elif self.state == 2: #ingame
            self.update()
            self.draw()

##        elif self.state == 3:
            
        elif self.state == 4: #game_over
            self.gameover()
            
        elif self.state == 5: #clear
            self.clear()

    def update(self):
        self.pos = self.mouse_location()
        if self.mouse_pre[0] == 1: #mouse left click
            if self.board[self.pos[0]][self.pos[1]] < 0:
                self.state = 4
            elif self.board[self.pos[0]][self.pos[1]] > 0:
                self.board_state[self.pos[0]][self.pos[1]] = 1
            elif self.board[self.pos[0]][self.pos[1]] == 0:
                self.zero(self.pos[0], self.pos[1])
                self.zero_open()
                    
        if self.mouse_pre[2] == 1: #mouse right click
            if self.board_state[self.pos[0]][self.pos[1]] == 0:
                self.board_state[self.pos[0]][self.pos[1]] = 2
                
        for i in range(1, self.level[1] - 1): #count score
            for j in range(1, self.level[2] - 1):
                if self.board_state[i][j] == 0:
                    self.count[0] += 1
                if self.board_state[i][j] == 2:
                    self.count[1] += 1
        self.count[0] += self.count[1]
        self.count[2] = self.level[3] - self.count[1]
        if self.count[0] == self.level[3]:
            self.state = 5
        
        self.text_score = self.m_font.render("{}".format(self.count[2]), True, BLACK)
        self.count = [0, 0, 0]
            
    def draw(self):
        pg.draw.rect(self.screen, GRAY, [0, 0, 500, 100]) #background
        pg.draw.rect(self.screen, WHITE, [200, 25, 100, 50]) #score board
        self.screen.blit(self.text_score, [200, 25]) #score
        for i in range(1, self.level[1]):
            for j in range(1, self.level[2]):
                if self.board_state[i][j] == 0:
                    self.screen.blit(self.unclicked, [(i-1) * self.level[4], (j-1) * self.level[4] + 100])
                elif self.board_state[i][j] == 1:
                    self.screen.blit(self.clicked, [(i-1) * self.level[4], (j-1) * self.level[4] + 100])
                    if self.board[i][j] != 0:
                        self.board_text = self.s_font.render("{}".format(self.board[i][j]), True, BLACK)
                        self.screen.blit(self.board_text, [(i-1) * self.level[4], (j-1) * self.level[4] + 100])
                elif self.board_state[i][j] == 2:
                    self.screen.blit(self.flag, [(i-1) * self.level[4], (j-1) * self.level[4] + 100])
        pg.draw.rect(self.screen, BLACK, [(self.pos[0] - 1) * self.level[4], (self.pos[1] - 1) * self.level[4] + 100, self.level[4], self.level[4]], 5 - self.level[0])
        pg.display.update()

    def clear(self):
        self.mouse_state = self.mouse_location()
        pg.draw.rect(self.screen, GRAY, [85, 85, 330, 330])
        self.text_clear = self.font.render("CLEAR!", True, BLACK)
        if self.mouse_pre[0] == 0:
            if self.mouse_state == 1:
                self.text_newgame = self.font.render("New game", True, RED)
            else:
                self.text_newgame = self.font.render("New game", True, BLACK)
            self.screen.blit(self.text_clear, [150, 140])
            self.screen.blit(self.text_newgame, [160, 300])
        elif self.mouse_pre[0] == 1:
            if self.mouse_state == 1:
                self.new()
        pg.display.update()

    def gameover(self):
        self.mouse_state = self.mouse_location()
        pg.draw.rect(self.screen, GRAY, [85, 85, 330, 330])
        self.text_GO = self.font.render("Game Over", True, BLACK)
        if self.mouse_pre[0] == 0:
            if self.mouse_state == 1:
                self.text_newgame = self.font.render("New game", True, RED)
            else:
                self.text_newgame = self.font.render("New game", True, BLACK)
            self.screen.blit(self.text_GO, [150, 140])
            self.screen.blit(self.text_newgame, [160, 300])
        elif self.mouse_pre[0] == 1:
            if self.mouse_state == 1:
                self.new()
        pg.display.update()
        
    def mouse_location(self):
        self.mouse = pg.mouse.get_pos()
        self.mouse_pre = pg.mouse.get_pressed()
        if self.state == 1: #select
            if self.mouse[0] > 230 and self.mouse[0] <= 480 and self.mouse[1] > 70 and self.mouse[1] <= 170: #easy
                return 1
            elif self.mouse[0] > 230 and self.mouse[0] <= 480 and self.mouse[1] > 200 and self.mouse[1] <= 300: #normal
                return 2
            elif self.mouse[0] > 230 and self.mouse[0] <= 480 and self.mouse[1] > 330 and self.mouse[1] <= 430: #hard
                return 3
            else:
                return 4

        elif self.state == 2: #ingame
            return int(self.mouse[0] / self.level[4]) + 1, int(self.mouse[1] / self.level[4] + 1 - (100 / self.level[4]))
            
        elif self.state == 3: #spown mine
            return int(self.mouse[0] / self.level[4]) + 1, int(self.mouse[1] / self.level[4] + 1 - (100 / self.level[4]))

        elif self.state == 4: #gameover
            if self.mouse[0] > 150 and self.mouse[0] <= 350 and self.mouse[1] > 250 and self.mouse[1] <= 350:
                return 1
            else:
                return 2
            
        elif self.state == 5: #clear
            if self.mouse[0] > 150 and self.mouse[0] <= 350 and self.mouse[1] > 250 and self.mouse[1] <= 350:
                return 1
            else:
                return 2
            
    def zero(self, x, y):
        self.zero_check(x, y)

    def zero_check(self, x, y):
        if self.check.count([x, y]) == 0:
            self.check.append([x, y])
        if x - 1 > 0 and x - 1 < self.level[1] - 1 and y > 0 and y < self.level[2] - 1:
            if self.board[x - 1][y] == 0 and self.board_state[x - 1][y] == 0 and self.check.count([x - 1, y]) == 0:
                self.zero_check(x - 1, y)
                self.check.append([x - 1, y])

        if x + 1 > 0 and x + 1 < self.level[1] - 1 and y > 0 and y < self.level[2] - 1:
            if self.board[x + 1][y] == 0 and self.board_state[x + 1][y] == 0 and self.check.count([x + 1, y]) == 0:
                self.zero_check(x + 1, y)
                self.check.append([x + 1, y])

        if x > 0 and x < self.level[1] - 1 and y - 1 > 0 and y - 1 < self.level[2] - 1:
            if self.board[x][y - 1] == 0 and self.board_state[x][y - 1] == 0 and self.check.count([x, y - 1]) == 0:
                self.zero_check(x, y - 1)
                self.check.append([x, y - 1])

        if x > 0 and x < self.level[1] - 1 and y + 1 > 0 and y + 1 < self.level[2] - 1:
            if self.board[x][y + 1] == 0 and self.board_state[x][y + 1] == 0 and self.check.count([x, y + 1]) == 0:
                self.zero_check(x, y + 1)
                self.check.append([x, y + 1])

    def zero_open(self):
        for i in self.check:
            for a in range(-1, 2):
                for b in range(-1, 2):
                    self.board_state[i[0] + a][i[1] + b] = 1

        
g = game()                
while g.running:
    g.clock.tick(20)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            g.running = False
    g.run()
pg.quit()
sys.exit()
          
  
  
