import pygame as pg
import sys
import random
from time import *
from setting import *

class game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SIZE)
        self.title = pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("arial", 48, True, False)
        self.s_font = pg.font.SysFont("arial", 20, True, False)
        self.new()

    def new(self):
        self.running = True
        self.state = 1
        self.level = [0, 0, 0, 0] #level, row, col, mine
        self.screen.fill(WHITE)
        self.clicked = pg.image.load("clicked.png")
        self.unclicked = pg.image.load("unclicked.png")
        self.opening = False
        self.block = 0
        self.count = 0
        self.score = 0
        self.mouse_pos = [0, 0]
        self.check = []
        self.check_2 = []
        
    def select(self):
        self.mouse_state = self.mouse_location()
        self.text_level = self.font.render("Level", True, BLACK)
        
        if self.mouse_pre[0] == 0:
            if self.mouse_state == 1:
                self.text_easy = self.font.render("easy", True, RED)
            elif self.mouse_state == 2:
                self.text_normal = self.font.render("normal", True, RED)
            elif self.mouse_state == 3:
                self.text_hard = self.font.render("hard", True, RED)
            else:
                self.text_easy = self.font.render("easy", True, BLACK)
                self.text_normal = self.font.render("normal", True, BLACK)
                self.text_hard = self.font.render("hard", True, BLACK)
                
            self.screen.blit(self.text_easy, [300, 120])
            self.screen.blit(self.text_normal, [300, 250])
            self.screen.blit(self.text_hard, [300, 380])
            self.screen.blit(self.text_level, [80, 250])
        
        elif self.mouse_pre[0] == 1:
            if self.mouse_state == 1:
                self.level = [1, 12, 10, 2]
                self.block = 50
                
            elif self.mouse_state == 2:
                self.level = [2, 22, 18, 50]
                self.block = 25
                
            elif self.mouse_state == 3:
                self.level = [3, 27, 22, 99]
                self.block = 20

        if self.level[0] != 0:
            self.board = [[0 for i in range(self.level[2] + 4)] for j in range(self.level[1] + 4)]
            self.board_state = [[0 for i in range(self.level[2] + 4)] for j in range(self.level[1] + 4)]
            self.start()
                
    def start(self):
        if self.opening == False:
            sleep(0.5)
            self.opening = True
        self.clicked = pg.transform.scale(self.clicked, [self.block, self.block])
        self.unclicked = pg.transform.scale(self.unclicked, [self.block, self.block])
        for i in range(self.level[3]):
            x = random.randint(1, self.level[1] - 1)
            y = random.randint(1, self.level[2] - 1)
            while True:
                if self.board[x][y] < 0:
                    x = random.randint(0, self.level[1] - 1)
                    y = random.randint(0, self.level[2] - 1)
                elif self.board[x][y] == 0:
                    break
            self.board[x][y] = -1
        
        for i in range(1, self.level[1]):
            for j in range(1, self.level[2]):
                if self.board[i][j] >= 0:
                    for x in range(-1, 1):
                        for y in range(-1, 1):
                            if self.board[i+x][j+y] < 0:
                                self.count += 1
                    self.board[i][j] = self.count
                    self.count = 0
        self.state = 2

    def run(self):
        if self.state == 1:
            self.select()
            pg.display.update()

        elif self.state == 2:
            self.update()
            self.draw()
            
        elif self.state == 4:
            self.gameover()
            
##        elif self.state == 5:

    def update(self):
        self.mouse_pos = self.mouse_location()
        if self.mouse_pre[0] == 1:
            if self.board[self.mouse_pos[0]][self.mouse_pos[1]] < 0:
                self.state = 4
                
            elif self.board[self.mouse_pos[0]][self.mouse_pos[1]] > 0:
                self.board_state[self.mouse_pos[0]][self.mouse_pos[1]] = 1
                
            elif self.board[self.mouse_pos[0]][self.mouse_pos[1]] == 0:
                self.check.append([self.mouse_pos[0], self.mouse_pos[1]])
                while len(self.check) != 0:
                    for i in self.check:
                        self.zero_check(i[0], i[1])

                self.zero_open()
                
        if self.mouse_pre[2] == 1:
            if self.board_state[self.mouse_pos[0]][self.mouse_pos[1]] == 0:
                self.board_state[self.mouse_pos[0]][self.mouse_pos[1]] = 2
                
        for i in range(1, self.level[1]):
            for j in range(1, self.level[2]):
                if self.board[i][j] < 0 and self.board_state[i][j] == 0:
                    self.score += 1
        self.text_score = self.s_font.render("{}".format(self.score), True, BLACK)
        self.score = 0
            
    def draw(self):
        pg.draw.rect(self.screen, GRAY, [0, 0, 500, 100])
        pg.draw.rect(self.screen, WHITE, [200, 25, 100, 50])
        self.screen.blit(self.text_score, [200, 25])
        for i in range(1, self.level[1]):
            for j in range(1, self.level[2]):
                if self.board_state[i][j] == 0:
                    self.screen.blit(self.unclicked, [(i-1) * self.block, (j-1) * self.block + 100])
                    
                elif self.board_state[i][j] == 1:
                    self.screen.blit(self.clicked, [(i-1) * self.block, (j-1) * self.block + 100])
                    self.board_text = self.s_font.render("{}".format(self.board[i][j]), True, BLACK)
                    self.screen.blit(self.board_text, [(i-1) * self.block, (j-1) * self.block + 100])

                elif self.board_state[i][j] == 2:
                    pg.draw.rect(self.screen, RED, [(i-1) * self.block, (j-1) * self.block + 100, self.block, self.block])
                    
        pg.display.update()

##    def clear(self):

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
        if self.state == 1: #opening
            if self.mouse[0] > 230 and self.mouse[0] <= 480 and self.mouse[1] > 70 and self.mouse[1] <= 170: #easy
                return 1
            elif self.mouse[0] > 230 and self.mouse[0] <= 480 and self.mouse[1] > 200 and self.mouse[1] <= 300: #normal
                return 2
            elif self.mouse[0] > 230 and self.mouse[0] <= 480 and self.mouse[1] > 330 and self.mouse[1] <= 430: #hard
                return 3
            else:
                return 4

        elif self.state == 2: #ingame
            return int(self.mouse[0] / self.block) + 1, int(self.mouse[1] / self.block + 1 - (100 / self.block))
            
##        elif self.state == 3: #

        elif self.state == 4: #gameover
            if self.mouse[0] > 150 and self.mouse[0] <= 350 and self.mouse[1] > 250 and self.mouse[1] <= 350:
                return 1
            else:
                return 2
##        elif self.state == 5: #clear
            
    def zero_check(self, x, y):
        self.board_state[x][y] = 3 
        for a in [-1, 1]:
            if x + a > 0 and x + a < self.level[1]:
                if self.board[x + a][y] == 0 and self.board_state[x + a][y] == 0:
                    self.check.append([x + a, y])
                    self.board_state[x + a][y] = 3
                    
            if y + a > 0 and y + a < self.level[1]:  
                if self.board[x][y + a] == 0 and self.board_state[x][y + a] == 0:
                    self.check.append([x, y + a])
                    self.board_state[x][y + a] = 3
        del self.check[0]

    def zero_open(self):
        for i in range(1, self.level[1]):
            for j in range(1, self.level[2]):
                if self.board_state[i][j] == 3:
                    for a in range(-1, 1):
                        for b in range(-1, 1):
                            self.board_state[i + a][j + b] == 3
        
g = game()                
while g.running:
    g.clock.tick(20)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            g.running = False
    g.run()
    print(g.check)
pg.quit()
sys.exit()
          
  
  
