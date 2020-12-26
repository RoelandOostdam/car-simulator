from game_core import car, calculate_curve, DragRacing
from game_core.car_generator import generate_car
from saved_cars import stock_template, subaru_brz, de_roelbak
import pickle

# generate_car(15000,100,10)

# with open('game_core/next_car.pkl', 'rb') as input:
#     opponent_car = pickle.load(input)

# Start race
car1 = de_roelbak.create()
car2 = subaru_brz.create()
DragRacing(car1, car2, 200)

# For dyno use car.dyno()
# For the torque chart use calculate_curve(car)
