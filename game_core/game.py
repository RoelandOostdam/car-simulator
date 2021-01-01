import math
import time

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
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.clock = pygame.time.Clock()
        self.gameDisplay = None
        self.time_elapsed = 0
        self.time_finished = [0,0]
        self.sectors_passed = [0,0]
        self.sector_times = {
            '100':[0,0],
            '200':[0,0],
            '300':[0,0],
            '400':[0,0],
        }

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
        time_start = time.time()
        while not self.crashed:
            if helpers.mps_to_kph(self.car.speed_mps) > 75:
                self.car.nos_activated = True
            if helpers.mps_to_kph(self.car2.speed_mps) > 75:
                self.car2.nos_activated = True
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         self.crashed = True
            #
            #     if helpers.mps_to_kph(self.car.speed_mps) > 75:
            #         self.car.nos_activated = True
            #     if helpers.mps_to_kph(self.car2.speed_mps) > 75:
            #         self.car2.nos_activated = True
                # if (event.type == pygame.KEYDOWN):
                #     if (event.key == pygame.K_LEFT) and helpers.mps_to_kph(self.car.speed_mps) > 75:
                #         self.car.nos_activated = True
                #     if (event.key == pygame.K_RIGHT) and helpers.mps_to_kph(self.car2.speed_mps) > 75:
                #         self.car2.nos_activated = True
            # Car simulation
            self.car.accelerate(1/60/10)
            self.car2.accelerate(1/60/10)
            self.time_elapsed += 1/60

            # Background display
            self.bg_speed = self.car.speed_mps
            self.gameDisplay.fill(self.black)
            self.background_road()

            # Car display
            self.update_cars()

            for i, car in enumerate([self.car, self.car2]):

                if car.distance_traveled*10 >= self.target_distance:
                    if self.won == False:
                        self.won = car.name
                    if i == 0 and car.finished == False:
                        self.time_finished[0] = (time.time()-time_start)
                    elif i == 1 and car.finished == False:
                        self.time_finished[1] = (time.time()-time_start)

                    car.finished = True
                if i == 0:
                    text_x = 20
                else:
                    text_x = 650

                for sector in self.sector_times.keys():
                    if car.distance_traveled*10 >= int(sector) and int(self.sectors_passed[i]) < int(sector):
                        self.sectors_passed[i] = sector
                        self.sector_times[sector][i] = time.time() - time_start
                # HUD display
                font = pygame.font.SysFont("lucidaconsole", 14)
                # Car info
                if self.won != False:
                    if car.name == self.won:
                        text = font.render(f"Won", True, self.green)
                    else:
                        text = font.render(f"Lost", True, self.red)
                    self.gameDisplay.blit(text, (text_x, 20))

                else:
                    text = font.render(f"Distance: {round(max(self.car.distance_traveled*10, self.car2.distance_traveled*10))}/{self.target_distance}", True, self.white)
                    self.gameDisplay.blit(text, (text_x, 20))

                if self.won != False:
                    text = font.render(f"{round(self.time_finished[i],3)}s", True, self.white)
                else:
                    text = font.render(f"{round(self.time_elapsed,1)}s", True, self.white)
                self.gameDisplay.blit(text, (text_x, 40))

                if i==0:
                    i2 = 1
                else:
                    i2 = 0
                sector_ys = [60,80,100,120]
                for z, sector in enumerate(self.sector_times.keys()):
                    if self.sector_times[sector][i] != 0:
                        diff = round(self.sector_times[sector][i2]-self.sector_times[sector][i], 3)
                        c = self.green
                        if diff < 0:
                            c = self.red
                        text = font.render(f"{str(sector)}m: {diff}s", True, c)
                        self.gameDisplay.blit(text, (text_x, sector_ys[z]))

                if i == 0:
                    i2 = self.car2
                else:
                    i2 = self.car
                diff = round(car.distance_traveled - i2.distance_traveled, 2)
                c = self.green
                if diff < 0:
                    c = self.red
                text = font.render(f"Diff: {diff}m", True, c)
                self.gameDisplay.blit(text, (text_x, 140))

                # text = font.render(f"Distance traveled: {round(car.distance_traveled*10)}m", True, self.white)
                # self.gameDisplay.blit(text, (text_x, 150))
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
                text = f"Speed {round(helpers.mps_to_kph(car.speed_mps), 1)} kph"
                if car.tcs:
                    text += " [ TCS ]"
                text = font.render(text, True, self.white)
                self.gameDisplay.blit(text, (text_x, 480))
                # RPM
                txt = f"RPM   {round(car.rpm)}"
                if car.shifting != False:
                    txt += " [shifting]"
                text = font.render(txt, True, self.white)
                self.gameDisplay.blit(text, (text_x, 500))
                # RPM Bar
                percentage = round((car.rpm / car.max_rpm) * 20)
                pbar = "["+("-"*percentage)+("_"*(20-percentage))+"]"+f" {car.gear}"
                text = font.render(pbar, True, self.white)
                self.gameDisplay.blit(text, (text_x, 520))
                # Power bar
                car_pwr = car.power()
                percentage = round((helpers.watt_to_bhp(car_pwr) / car.dyno_max_power) * 8)
                pbar = "Power [" + (">" * percentage) + (
                            "_" * (8 - percentage)) + "]" + f" {round(helpers.watt_to_bhp(car_pwr), 1)} bhp"
                text = font.render(pbar, True, self.white)
                self.gameDisplay.blit(text, (text_x, 560))
                # Boost bar
                if car.aspiration:
                    percentage = math.floor((car.boost() / car.boost_nm) * 8)
                    pbar = "Boost [" + (">" * percentage) + ("_" * (8 - percentage)) + "]" + f" {round(helpers.watt_to_bhp(car.boost()))} bhp"
                else:
                    pbar = "No boost installed"
                text = font.render(pbar, True, self.white)
                self.gameDisplay.blit(text, (text_x, 540))

                if car.nos_type != False:
                    if car.nos_activated == False:
                        nos_percentage = 8
                    else:
                        nos_percentage = math.floor(car.nos() / helpers.bhp_to_watt(car.nos_type) * 8)
                    pbar = "[" + ("/" * nos_percentage) + (
                                "_" * (8 - nos_percentage)) + "]" + f" {round(helpers.watt_to_bhp(car.nos()))} bhp"

                else:
                    pbar = "Not installed"
                if pbar == "Not installed":
                    c = self.white
                else:
                    if car.nos_activated:
                        c = self.red
                    else:
                        if helpers.mps_to_kph(car.speed_mps) < 75:
                            c = self.white
                        else:
                            c = self.green
                text = font.render(f"NOS   {pbar}", True, c)
                self.gameDisplay.blit(text, (text_x, 580))

            # Pygame update
            pygame.display.update()
            self.clock.tick(60)

    def update_cars(self):
        if self.car.distance_traveled >= self.car2.distance_traveled:
            diff = (self.car.distance_traveled - self.car2.distance_traveled) * 10 * 4.5
            self.gameDisplay.blit(self.carImg, (self.car_x_coordinate, self.car_y_coordinate))
            self.gameDisplay.blit(self.car2Img, (self.car2_x_coordinate, self.car2_y_coordinate+diff))
        else:
            diff = (self.car2.distance_traveled - self.car.distance_traveled) * 10 * 4.5
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
