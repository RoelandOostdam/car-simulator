from game_core import car, calculate_curve, DragRacing
from game_core.car_generator import generate_car
from saved_cars import custom_10000_1 as c1
from saved_cars import custom_10000_2 as c2
import pickle

# generate_car(15000,100,10)

with open('game_core/next_car.pkl', 'rb') as input:
    opponent_car = pickle.load(input)

# Start race
car1 = c1.create()
car2 = c2.create()
DragRacing(car1, car2, 300)

# For dyno use car.dyno()
# For the torque chart use calculate_curve(car)
