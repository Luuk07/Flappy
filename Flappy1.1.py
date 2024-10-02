import pickle
import random
import pygame


class Game:
    def __init__(self, window_x, window_y):
        pygame.init()
        self.window_x = window_x
        self.window_y = window_y
        self.screen = pygame.display.set_mode((window_x, window_y))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.bird = Bird(self)
        self.hinternisse = Hinternisse(self, self.bird)
        self.saveandloade = Saveandloade(self.hinternisse, 0)
        self.hintergrund = pygame.image.load("7483159-eine-grosse-wiese-im-hintergrund-ist-der-himmel-natur-hintergrundbildkonzept-foto.jpg")
        self.hintergrund = pygame.transform.scale(self.hintergrund, (self.window_x, self.window_y))
        self.run()



    def run(self):
        run = True
        while run:
            pygame.time.delay(100)
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
              
            self.screen.fill(0)
            self.saveandloade.writescore()
            self.bird.movement()
            self.hinternisse.generate()
            self.hinternisse.movement()
            self.hinternisse.remove()
            self.hinternisse.draw_score_line()
            self.saveandloade.score = self.hinternisse.score
            self.bird.draw()
            self.screen.blit(self.hintergrund, (0, 0))
            self.hinternisse.draw_score()
            self.saveandloade.draw_highscore()
            self.hinternisse.draw()
            self.bird.draw_bird_image()







            pygame.display.update()






class Bird:
    def __init__(self, game):
        self.x_size = 70
        self.y_size = 70
        self.game = game
        self.surface = game.screen
        self.x_cor = game.window_x/3
        self.y_cor = game.window_y/3
        self.game = game
        self.surface = game.screen
        self.vogel = pygame.image.load("vogel-mit-roten-federn_1308-106864-removebg-preview.png")
        self.vogel = pygame.transform.scale(self.vogel, (self.x_size, self.y_size))




    def draw(self):
        self.object = pygame.draw.rect(self.surface, (255, 255, 255), (self.x_cor, self.y_cor, self.x_size, self.y_size))


    def draw_bird_image(self):
        self.surface.blit(self.vogel, (self.x_cor, self.y_cor))



    def movement(self):
        keys = pygame.key.get_pressed()
        vel = 20

        if keys[pygame.K_SPACE]:
            vel -= 40

        self.y_cor += vel









class Hinternisse:
    def __init__(self, game, bird):
        self.bird = bird
        self.game = game
        self.x_size = 50
        self.surface = game.screen
        self.window_x = game.window_x
        self.window_y = game.window_y
        self.speed = 10
        self.x_cor = 700
        self.score = 0
        self.wall = pygame.image.load("103250191-seamless-brown-brick-wall-background-in-cartoon-style-vector-illustration.jpg")
        self.schriftart = pygame.font.SysFont("Arial", 45)
        self.timer = pygame.time.get_ticks()
        self.timer_two = pygame.time.get_ticks()

        self.line_hit = pygame.Rect(self.x_cor + self.x_size, 1, 2, 800)

        self.one_u = pygame.Rect(self.x_cor, 400, self.x_size, 400)
        self.one_d = pygame.Rect(self.x_cor, 0, self.x_size, 200)
        self.two_u = pygame.Rect(self.x_cor, 600, self.x_size, 200)
        self.two_d = pygame.Rect(self.x_cor, 0, self.x_size, 400)
        self.three_u = pygame.Rect(self.x_cor, 700, self.x_size, 100)
        self.three_d = pygame.Rect(self.x_cor, 0, self.x_size, 500)
        self.four_u = pygame.Rect(self.x_cor, 200, self.x_size, 600)
        self.four_d = pygame.Rect(self.x_cor, 0, self.x_size, 0)
        self.five_u = pygame.Rect(self.x_cor, 800, self.x_size, 0)
        self.five_d = pygame.Rect(self.x_cor, 0, self.x_size, 600)
        self.six_u = pygame.Rect(self.x_cor, 300, self.x_size, 500)
        self.six_d = pygame.Rect(self.x_cor, 0, self.x_size, 100)

        self.active_rects = []
        self.active_line = []







    def generate(self):
        liste = [(self.one_d, self.one_u), (self.two_u, self.two_d), (self.three_u, self.three_d), (self.three_u, self.three_d), (self.four_u, self.four_d), (self.five_u, self.five_d), (self.six_u, self.six_d)]
        current_time = pygame.time.get_ticks()
        if current_time - self.timer >= 4000:
            rd_chose = random.choice(liste)
            new_rects = (rd_chose[0].copy(), rd_chose[1].copy()) # .copy(), damit Änderungen keine Auswirkungen auf die ursprünglichen rechtecke in der sel.liste haben(ohne Kopie bekommt es speed boost)
            new_line = self.line_hit.copy()
            self.active_rects.append(new_rects)
            self.active_line.append(new_line)
            self.timer = current_time




    def draw(self):
        current_time = pygame.time.get_ticks()
        for rect_pair in self.active_rects:
            first_rect = pygame.draw.rect(self.surface, (255, 255, 255), rect_pair[0]) # es wird der erste index(paar 1) und der zweite index (paar 2) von dem ersten tuple der liste aktive rects gezeichnet
            second_rect = pygame.draw.rect(self.surface, (255, 255, 255), rect_pair[1])
            self.wall_one = pygame.transform.scale(self.wall, (self.x_size, first_rect.h))
            self.wall_two = pygame.transform.scale(self.wall, (self.x_size, second_rect.h))
            self.surface.blit(self.wall_one, (first_rect.x, first_rect.y))
            self.surface.blit(self.wall_two, (second_rect.x, second_rect.y))
            if ((first_rect.colliderect(self.bird.object) or second_rect.colliderect(self.bird.object) or self.bird.y_cor >= self.window_y
                 or self.bird.y_cor <= 0 and current_time - self.timer_two >= 2000)):
                self.score = 0
                self.bird.y_cor = 100
                self.timer_two = current_time
                self.active_rects.pop(0)
                self.active_line.pop(0)
                if len(self.active_rects) >= 1:
                    self.active_rects.pop(0)

    def draw_score_line(self):
        current_time = pygame.time.get_ticks()
        for line in self.active_line:
            line_goal = pygame.draw.rect(self.surface, (0, 0, 0), line)
            if (line_goal.colliderect(self.bird.object)) and current_time - self.timer_two >= 2000:
                self.score += 1
                self.timer_two = current_time



    def movement(self):
        for rect_pair in self.active_rects:
            rect_pair[0].x -= self.speed
            rect_pair[1].x -= self.speed
        for line in self.active_line:
            line.x -= self.speed




    def remove(self):
        for rect_pair in self.active_rects:
            if rect_pair[0].x == -10:
                self.active_rects.pop(0) # es wird das erste element bzw. tuple gelöscht
        for line in self.active_line:
            if line.x == 1:
                self.active_line.pop(0)



    def draw_score(self):
        text = self.schriftart.render(f"Score:{self.score}", True, (255, 255, 255))
        self.surface.blit(text, (1, 10))


class Saveandloade:
    def __init__(self, hinternisse, highscore):
        self.hinternisse = hinternisse
        self.schriftart = pygame.font.SysFont("Arial", 45)
        self.score = hinternisse.score
        self.surface = hinternisse.surface
        self.highscore = highscore

    def writescore(self):
        with open("data.pickle", "rb") as f:
            self.highscore = pickle.load(f)
            if self.score >= self.highscore:
                self.highscore = self.score
        with open("data.pickle", "wb") as f:
            pickle.dump(self.highscore, f)

    def draw_highscore(self):
        text = self.schriftart.render(f"Highscore:{self.highscore}", True, (255, 255, 255))
        self.surface.blit(text, (250, 10))








game = Game(800, 800)

