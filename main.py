"""
    Simple Snake Game
  created by Katzeminze.
"""

import pygame
import time
import random
from xml.dom import minidom


# global variables of text and texture paths
images = dict()


class Snake:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.game_over = False
        self.dis = None

        # Defining colors
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.white = (255, 255, 255)
        self.black = (1, 1, 1)
        self.yellow = (255, 255, 102)

        self.font_style = None

        # Defining initial coordinates and steps when keyboard keys are pressed
        self.x = self.width/2
        self.y = self.height/2
        self.x_step = 0
        self.y_step = 0

        self.snake_part = 10
        self.food_part = 10
        self.snake_speed = 10

        self.snake_list = []
        self.snake_length = 1

        # Position of the food
        self.food_x = round(random.randrange(0, self.width - self.food_part) / 10.0) * 10.0
        self.food_y = round(random.randrange(0, self.height - self.food_part) / 10.0) * 10.0

        # Fruit type
        try:
            self.fruits = [images["apple"], images["orange"]]
            self.fruit_number = 0
        except KeyError as err:
            print(f"Key {err} is missed in images dictionary")
            raise

    def start(self):
        pygame.init()
        pygame.font.init()
        self.dis = pygame.display.set_mode((self.width, self.height))
        try:
            self.font_style = pygame.font.Font(images["snake_font"], 50)
        except KeyError as err:
            print(f"Key {err} is missed in images dictionary")
            raise
        pygame.display.update()
        pygame.display.set_caption('Snake')

        clock = pygame.time.Clock()
        # change the snake position till game_over event (game over or quiting)
        while not self.game_over:
            self.x += self.x_step
            self.y += self.y_step
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    self.move(event)

            # self.dis.fill(self.white)
            # self.texture_snake = pygame.image.load(r".\snake\pics\green_snake_skin.jpg")  # .convert()
            try:
                texture_grass = self.create_texture(self.width, self.height, images["image_of_grass_texture"])
                self.dis.blit(texture_grass, (0, 0))
            except KeyError as err:
                print(f"Key {err} is missed in images dictionary")
                raise
            # pygame.display.update()

            # draw food
            random_fruit = self.fruits[self.fruit_number]
            fruit = pygame.image.load(random_fruit)
            fruit = pygame.transform.scale(fruit, (10, 10))
            rect = fruit.get_rect()
            rect = rect.move((self.food_x, self.food_y))
            self.dis.blit(fruit, rect)

            #pygame.draw.rect(self.dis, self.red, [self.food_x, self.food_y, self.snake_part, self.snake_part])
            # draw snake
            #pygame.draw.circle(self.dis, self.blue, [self.x, self.y], self.snake_part)
            pygame.draw.rect(self.dis, self.blue, [self.x, self.y, self.snake_part, self.snake_part])

            snake_head = [self.x, self.y]
            self.snake_list.append(snake_head)
            if len(self.snake_list) > self.snake_length:
                del self.snake_list[0]

            for x in self.snake_list[:-1]:
                if x == snake_head:
                    self.game_over_operation("Head-Tail! Game over!", 4)

            self.snake_extension()

            self.display_score(self.snake_length-1)

            pygame.display.update()

            if self.x == self.food_x and self.y == self.food_y:
                self.food_x = round(random.randrange(0, self.width - self.food_part) / 10.0) * 10.0
                self.food_y = round(random.randrange(0, self.height - self.food_part) / 10.0) * 10.0
                self.snake_length += 1
                self.fruit_number = random.randrange(len(self.fruits))
            clock.tick(self.snake_speed)

        self.exit()

    def move(self, event):
        # starting point of drawing is the upper left corner
        if event.key == pygame.K_LEFT:
            self.x_step = -self.snake_part
            self.y_step = 0
        elif event.key == pygame.K_RIGHT:
            self.x_step = self.snake_part
            self.y_step = 0
        elif event.key == pygame.K_DOWN:
            self.x_step = 0
            self.y_step = self.snake_part
        elif event.key == pygame.K_UP:
            self.x_step = 0
            self.y_step = -self.snake_part

        if self.x >= self.width or self.x < 0 or self.y >= self.height or self.y < 0:
            self.game_over_operation("Game over!")

        self.x += self.x_step
        self.y += self.y_step

    def display_message(self, msg, color):
        msg = self.font_style.render(msg, True, color)
        # centering the message
        text_position = msg.get_rect(center=self.dis.get_rect().center)
        self.dis.blit(msg, text_position)

    def display_score(self, score):
        score_text = self.font_style.render("Your score: " + str(score), True, self.black)
        self.dis.blit(score_text, [0, 0])

    def snake_extension(self):
        for x in self.snake_list:
            # pygame.draw.rect(self.dis, self.yellow, [x[0], x[1], self.snake_part, self.snake_part])
            try:
                skin = pygame.image.load(images["snake_skin"])
            except KeyError as err:
                print(f"Key {err} is missed in images dictionary")
                raise
            skin = pygame.transform.scale(skin, (10, 10))
            rect_skin = skin.get_rect()
            rect_skin = rect_skin.move((x[0], x[1]))
            self.dis.blit(skin, rect_skin)

    def game_over_operation(self, msg, sleep_period=2):
        self.display_message(msg, self.red)
        pygame.display.update()
        time.sleep(sleep_period)
        self.game_over = True

    def create_texture(self, width, height, image):
        texture = pygame.image.load(image)
        texture = pygame.transform.scale(texture, (width, height))
        return texture

    # @staticmethod
    def exit(self):
        pygame.quit()
        quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # reading xml files with textures and fonts
    xml_filename = r"C:\Users\Hpkate\PycharmProjects\Snake_game\images_list.xml"
    xmldoc = minidom.parse(xml_filename)
    itemlist = xmldoc.getElementsByTagName('image')
    for item in itemlist:
        images[item.attributes["tag"].value] = item.attributes["file"].value

    # starting the game
    cobra = Snake()
    cobra.start()

