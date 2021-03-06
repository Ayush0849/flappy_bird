import pygame
from pygame.locals import *
from sys import exit


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        b_sur = pygame.Surface((15, 15))
        bird_img = pygame.transform.scale(pygame.image.load("flappy_bird.jpg"), (15, 15))
        bird_img = bird_img.convert_alpha()
        b_sur.blit(bird_img, (0, 0))

        # circ = pygame.draw.circle(circ_sur,(0,255,0),(15//2,15//2),15//2)
        b_sur = b_sur.convert()
        b_sur.set_colorkey((0, 0, 0))
        self.image = b_sur
        self.rect = self.image.get_rect()

    def update(self, pos):
        self.rect.topleft = pos
        pass

    def draw(self, a_screen):
        a_screen.blit(self.image, self.rect.topleft)
        pass


class Bat(pygame.sprite.Sprite):
    def __init__(self, a_color):
        pygame.sprite.Sprite.__init__(self)
        bat = pygame.Surface((10, 50))
        bat = bat.convert()
        bat.fill(a_color)
        self.image = bat
        self.rect = self.image.get_rect()

    def update(self, pos):
        self.rect.topleft = pos

    def draw(self, a_screen):
        a_screen.blit(self.image, self.rect.topleft)
        pass


def init_params():
    # some definitions
    global bar1_x, bar1_y, bar2_x, bar2_y, bar1_move, bar2_move
    global circle_x, circle_y, speed_circ
    global speed_x, speed_y, bar1_score, bar2_score

    bar1_x, bar2_x = 10., 620.
    bar1_y, bar2_y = 215., 215.
    circle_x, circle_y = 307.5, 232.5
    bar1_move, bar2_move = 0., 0.
    speed_x, speed_y, speed_circ = 250. / 1, 250. / 1, 250.
    bar1_score, bar2_score = 0, 0
    # clock and font objects


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 480), 0, 32)
    pygame.display.set_caption("Ping Pong Flappy Bird!")

    # Creating 2 bars, a ball and background.
    back = pygame.Surface((800, 480))
    background = back.convert()
    background.fill((0, 0, 0))

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("calibri", 40)

    init_params()
    ball = Ball()
    bat1 = Bat((0, 0, 255))
    bat2 = Bat((255, 0, 0))

    text1 = font.render(str("Press SPACE to start!"), True, (255, 255, 255))
    text2 = font.render(str("Winner: first one to win 4 set!"), True, (255, 255, 255))
    text3 = font.render(str("q,a for blue, up,down for red"), True, (255, 255, 255))
    disp_instruction = True
    while disp_instruction:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                disp_instruction = False

        screen.blit(background, (0, 0))
        frame = pygame.draw.rect(screen, (255, 255, 255), Rect((5, 5), (630, 470)), 2)
        middle_line = pygame.draw.aaline(screen, (255, 255, 255), (330, 5), (330, 475))

        bat1.update((bar1_x, bar1_y))
        bat1.draw(screen)
        bat2.update((bar2_x, bar2_y))
        bat2.draw(screen)
        ball.update((circle_x, circle_y))
        ball.draw(screen)

        screen.blit(text1, (80., 200.))
        screen.blit(text2, (80., 200 + font.get_height()))
        screen.blit(text3, (80., 200 + 2 * font.get_height()))

        clock.tick(30)
        pygame.display.update()

    init_params()
    set_over = False
    game_score_arr = [0, 0]
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if not set_over:
                    if event.key == K_q:
                        bar1_move = -ai_speed
                    elif event.key == K_a:
                        bar1_move = ai_speed
                    if event.key == K_UP:
                        bar2_move = -ai_speed
                    elif event.key == K_DOWN:
                        bar2_move = ai_speed
                else:
                    if event.key == K_SPACE:
                        if sum(game_score_arr) < 7 and game_score_arr[0] < 4 and game_score_arr[1] < 4:
                            set_over = False
                            init_params()

            elif event.type == KEYUP:
                if not set_over:
                    if event.key == K_q or event.key == K_a:
                        bar1_move = 0.
                    if event.key == K_UP or event.key == K_DOWN:
                        bar2_move = 0.

        score1 = font.render(str(bar1_score), True, (0, 0, 255))
        score2 = font.render(str(bar2_score), True, (255, 0, 0))
        game_score = font.render("%d:%d" % (game_score_arr[0], game_score_arr[1]), True, (255, 255, 255))

        screen.blit(background, (0, 0))
        frame = pygame.draw.rect(screen, (255, 255, 255), Rect((5, 5), (630, 470)), 2)
        middle_line = pygame.draw.aaline(screen, (255, 255, 255), (330, 5), (330, 475))

        bat1.update((bar1_x, bar1_y))
        bat1.draw(screen)
        bat2.update((bar2_x, bar2_y))
        bat2.draw(screen)
        ball.update((circle_x, circle_y))
        ball.draw(screen)

        screen.blit(score1, (700., 200.))
        screen.blit(score2, (700., 200 + font.get_height()))
        screen.blit(game_score, (700., 200 + 2 * font.get_height()))

        if game_score_arr[0] >= 4 or game_score_arr[1] >= 4:
            text = font.render(str("Game Over!"), True, (255, 255, 255))
            screen.blit(text, (250., 200.))

        time_passed = clock.tick(30)
        time_sec = time_passed / 1000.0

        if not set_over:
            bar1_y += bar1_move
            bar2_y += bar2_move

            circle_x += speed_x * time_sec
            circle_y += speed_y * time_sec
            ai_speed = speed_circ * time_sec

            if bar1_y >= 420.:
                bar1_y = 420.
            elif bar1_y <= 10.:
                bar1_y = 10.
            if bar2_y >= 420.:
                bar2_y = 420.
            elif bar2_y <= 10.:
                bar2_y = 10.

            if pygame.sprite.collide_rect(ball, bat1):
                circle_x = 20.
                speed_x = -speed_x

            if pygame.sprite.collide_rect(ball, bat2):
                circle_x = 605.
                speed_x = -speed_x

            if circle_x < 5.:
                bar2_score += 1
                circle_x, circle_y = 320., 232.5
                ##        bar1_y,bar_2_y = 215., 215.
            elif circle_x > 620.:
                bar1_score += 1
                circle_x, circle_y = 307.5, 232.5
                ##        bar1_y, bar2_y = 215., 215.
            if circle_y <= 10.:
                speed_y = -speed_y
                circle_y = 10.
            elif circle_y >= 457.5:
                speed_y = -speed_y
                circle_y = 457.5

        pygame.display.update()
        if not set_over and (bar1_score == 11 or bar2_score == 11):
            if bar1_score == 11:
                game_score_arr[0] += 1
            else:
                game_score_arr[1] += 1
            set_over = True

