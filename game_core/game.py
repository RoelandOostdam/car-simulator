import pygame
from game_core.car import Car
import game_core.helpers as helpers

class DragRacing:
    def __init__(self, car1, car2, target_distance):

        pygame.init()
        self.display_width = 900
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.gameDisplay = None

        self.crashed = False

        self.target_distance = target_distance
        self.won = False

        # Load cars
        self.car = car1
        self.car2 = car2

        # Car prop
        self.carImg = pygame.image.load('game_core/img/car.png')
        self.car_x_coordinate = (self.display_width * 0.41)
        self.car_y_coordinate = (self.display_height * 0.5)
        self.car_width = 49

        # Car2 prop
        self.car2Img = pygame.image.load('game_core/img/enemy_car_1.png')
        self.car2_x_coordinate = (self.display_width * 0.53)
        self.car2_y_coordinate = (self.display_height * 0.5)
        self.car2_width = 49

        # enemy_car
        # self.enemy_car = pygame.image.load('.\\img\\enemy_car_1.png')
        # self.enemy_car_startx = random.randrange(310, 450)
        # self.enemy_car_starty = -600
        # self.enemy_car_speed = 5
        # self.enemy_car_width = 49
        # self.enemy_car_height = 100

        # Background
        self.bgImg = pygame.image.load("game_core/img/back_ground.jpg")
        self.bg_x1 = (self.display_width / 2) - (360 / 2)
        self.bg_x2 = (self.display_width / 2) - (360 / 2)
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 3
        self.count = 0

        # Window
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Drag Racing')
        self.game_engine()

    def game_engine(self):
        while not self.crashed:
            # Car simulation
            self.car.accelerate(1/60/10)
            self.car2.accelerate(1/60/10)

            # Background display
            self.bg_speed = self.car.speed_mps
            self.gameDisplay.fill(self.black)
            self.background_road()

            # Car display
            self.update_cars()

            for i, car in enumerate([self.car, self.car2]):
                if car.distance_traveled*10 >= self.target_distance and self.won == False:
                    self.won = car.name
                if i == 0:
                    text_x = 20
                else:
                    text_x = 650
                # HUD display
                font = pygame.font.SysFont("lucidaconsole", 14)
                # Car info
                if self.won != False:
                    text = font.render(f"{self.won} won", True, self.white)
                    self.gameDisplay.blit(text, (20, 20))
                else:
                    text = font.render(f"Distance: {round(max(self.car.distance_traveled*10, self.car2.distance_traveled*10))}/{self.target_distance}", True, self.white)
                    self.gameDisplay.blit(text, (20, 20))

                text = font.render(f"Distance traveled: {round(car.distance_traveled*10)}m", True, self.white)
                self.gameDisplay.blit(text, (text_x, 150))
                text = font.render(car.name, True, self.white)
                self.gameDisplay.blit(text, (text_x, 220))
                text = font.render(f"Total cost: ${car.total_cost}", True, self.white)
                self.gameDisplay.blit(text, (text_x, 240))
                text = font.render(car.name_engine_type, True, self.white)
                self.gameDisplay.blit(text, (text_x, 260))
                text = font.render(f"{car.dyno_max_power} HP, {car.dyno_max_torque} Nm", True, self.white)
                self.gameDisplay.blit(text, (text_x, 280))
                text = font.render(car.name_transmission, True, self.white)
                self.gameDisplay.blit(text, (text_x, 300))
                text = font.render(f"{car.clutch_type} clutch", True, self.white)
                self.gameDisplay.blit(text, (text_x, 320))
                text = font.render(f"{car.weight_type} chassis: {car.weight_kg}kg", True, self.white)
                self.gameDisplay.blit(text, (text_x, 360))
                text = font.render(f"Body kit: {car.name_body_kit}", True, self.white)
                self.gameDisplay.blit(text, (text_x, 380))
                text = font.render(f"{car.name_tyres} tyres", True, self.white)
                self.gameDisplay.blit(text, (text_x, 400))
                # Metrics
                text = font.render(f"{round(helpers.mps_to_kph(car.speed_mps), 1)} kph", True, self.white)
                self.gameDisplay.blit(text, (text_x, 500))
                # RPM
                txt = f"{round(car.rpm)} rpm"
                if car.shifting != False:
                    txt += " [shifting]"
                text = font.render(txt, True, self.white)
                self.gameDisplay.blit(text, (text_x, 520))
                # RPM Bar
                percentage = round((car.rpm / car.max_rpm) * 20)
                pbar = "["+("-"*percentage)+("_"*(20-percentage))+"]"
                text = font.render(pbar, True, self.white)
                self.gameDisplay.blit(text, (text_x, 540))
                # Boost bar
                if car.aspiration:
                    percentage = round((car.boost() / car.boost_nm) * 6)
                    pbar = "Boost [" + ("-" * percentage) + ("_" * (6 - percentage+1)) + "]"
                else:
                    pbar = "No boost installed"
                text = font.render(pbar, True, self.white)
                self.gameDisplay.blit(text, (text_x, 560))
                text = font.render(f"gear {car.gear}", True, self.white)
                self.gameDisplay.blit(text, (text_x, 580))

            # Pygame update
            pygame.display.update()
            self.clock.tick(60)

    def update_cars(self):
        if self.car.distance_traveled >= self.car2.distance_traveled:
            diff = (self.car.distance_traveled - self.car2.distance_traveled) * 100 * 4.5
            self.gameDisplay.blit(self.carImg, (self.car_x_coordinate, self.car_y_coordinate))
            self.gameDisplay.blit(self.car2Img, (self.car2_x_coordinate, self.car2_y_coordinate+diff))
        else:
            diff = (self.car2.distance_traveled - self.car.distance_traveled) * 100 * 4.5
            self.gameDisplay.blit(self.carImg, (self.car_x_coordinate, self.car_y_coordinate+diff))
            self.gameDisplay.blit(self.car2Img, (self.car2_x_coordinate, self.car2_y_coordinate))
    def background_road(self):
        self.gameDisplay.blit(self.bgImg, (self.bg_x1, self.bg_y1))
        self.gameDisplay.blit(self.bgImg, (self.bg_x2, self.bg_y2))

        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        if self.bg_y1 >= self.display_height:
            self.bg_y1 = -600

        if self.bg_y2 >= self.display_height:
            self.bg_y2 = -600

if __name__ == '__main__':
    instance = DragRacing()
