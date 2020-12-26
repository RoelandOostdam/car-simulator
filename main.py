from game_core import car, calculate_curve, DragRacing
from game_core.car_generator import generate_car
from saved_cars import missile_20000, de_roelbak_13000_v3, missile_20000_v2
import pickle

# generate_car(15000,100,10)

with open('game_core/next_car.pkl', 'rb') as input:
    opponent_car = pickle.load(input)

# Start race
car1 = missile_20000_v2.create()
car2 = missile_20000.create()
DragRacing(car1, car2, 300)

# For dyno use car.dyno()
# For the torque chart use calculate_curve(car)
