import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (0,0,0)
RED = (200,0,00)
BLUE1 = (100, 100, 100)
BLUE2 = (175, 175, 175)
BLACK = (150,150,150)

BLOCK_SIZE = 40
SPEED = 100

class SnakeGameAI:

    def __init__(self, w=960, h=720):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()


    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0


    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()


    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score


    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False


    def _update_ui(self):
        bg = pygame.image.load('resources/background.jpg')
        self.display.blit(bg,(-300,-200))

        head_up = pygame.image.load('resources/head_up.png')
        head_down = pygame.image.load('resources/head_down.png')
        head_right = pygame.image.load('resources/head_right.png')
        head_left = pygame.image.load('resources/head_left.png')

        tail_up = pygame.image.load('resources/tail_up.png')
        tail_down = pygame.image.load('resources/tail_down.png')
        tail_right = pygame.image.load('resources/tail_right.png')
        tail_left = pygame.image.load('resources/tail_left.png')

        body_vertical = pygame.image.load('resources/body_vertical.png')
        body_horizontal = pygame.image.load('resources/body_horizontal.png')

        body_tr = pygame.image.load('resources/body_tr.png')
        body_tl = pygame.image.load('resources/body_tl.png')
        body_br = pygame.image.load('resources/body_br.png')
        body_bl = pygame.image.load('resources/body_bl.png')
        
        if(self.snake[1].x - self.head.x == BLOCK_SIZE) :
            self.display.blit(head_left,pygame.Rect(self.head.x, self.head.y, BLOCK_SIZE, BLOCK_SIZE))
        elif(self.snake[1].x - self.head.x == -BLOCK_SIZE):
            self.display.blit(head_right,pygame.Rect(self.head.x, self.head.y, BLOCK_SIZE, BLOCK_SIZE))
        elif(self.snake[1].y - self.head.y == BLOCK_SIZE):
            self.display.blit(head_up,pygame.Rect(self.head.x, self.head.y, BLOCK_SIZE, BLOCK_SIZE))
        else:
            self.display.blit(head_down,pygame.Rect(self.head.x, self.head.y, BLOCK_SIZE, BLOCK_SIZE))
            


        # for pt in self.snake[1:-1]:
        #     pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
        #     pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
        for i in range(1,len(self.snake)-1):
            curr = self.snake[i]
            prev = self.snake[i-1]
            next = self.snake[i+1]
            if(curr.x == prev.x == next.x):
                self.display.blit(body_vertical,pygame.Rect(curr.x, curr.y, BLOCK_SIZE, BLOCK_SIZE))
            elif(curr.y == prev.y == next.y):
                self.display.blit(body_horizontal,pygame.Rect(curr.x, curr.y, BLOCK_SIZE, BLOCK_SIZE))
            elif((prev.x < curr.x and next.y > curr.y) or (prev.y > curr.y and next.x < curr.x)):
                self.display.blit(body_bl, pygame.Rect(curr.x, curr.y, BLOCK_SIZE, BLOCK_SIZE))
            elif (prev.x > curr.x and next.y > curr.y) or (prev.y > curr.y and next.x > curr.x):
                self.display.blit(body_br, pygame.Rect(curr.x, curr.y, BLOCK_SIZE, BLOCK_SIZE))
            elif (prev.y < curr.y and next.x > curr.x) or (next.y < curr.y and prev.x > curr.x):
                self.display.blit(body_tr, pygame.Rect(curr.x, curr.y, BLOCK_SIZE, BLOCK_SIZE))
            else:
                self.display.blit(body_tl, pygame.Rect(curr.x, curr.y, BLOCK_SIZE,BLOCK_SIZE))

        tail = self.snake[-1]
        if(self.snake[-2].x - tail.x == BLOCK_SIZE) :
            self.display.blit(tail_left,pygame.Rect(tail.x, tail.y, BLOCK_SIZE, BLOCK_SIZE))
        elif(self.snake[-2].x - tail.x == -BLOCK_SIZE):
            self.display.blit(tail_right,pygame.Rect(tail.x, tail.y, BLOCK_SIZE, BLOCK_SIZE))
        elif(self.snake[-2].y - tail.y == BLOCK_SIZE):
            self.display.blit(tail_up,pygame.Rect(tail.x, tail.y, BLOCK_SIZE, BLOCK_SIZE))
        else:
            self.display.blit(tail_down,pygame.Rect(tail.x, tail.y, BLOCK_SIZE, BLOCK_SIZE))

        apple = pygame.image.load('resources/apple.png')
        self.display.blit(apple, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()


    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)