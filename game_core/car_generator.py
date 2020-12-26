from game_core import Car
import random
import pickle
import copy


def generate_car(max_cost, optimized_distance, intensity):
    eligible_cars = []
    counter = 0
    while len(eligible_cars) < intensity:
        counter += 1
        cylinders = random.choice([4, 6, 8, 10, 12])
        displacement_cc = random.randrange(300, 800)
        turbo_type = random.choice(
            ['None', 'S', 'M', 'L', 'H', 'Supercharger-V1', 'Supercharger-V2', 'Supercharger-V3'])
        clutch_type = random.choice(['Stock', 'Street', 'Race'])
        weight_type = random.choice(['Heavy', 'Medium', 'Light', 'Ultra-light'])
        body_kit = random.choice(['Stock', 'Street', 'Sport', 'Performance', 'Race'])
        tyre_type = random.choice(['H', 'V', 'Z', 'W', 'Y'])

        # TODO: Gear optimizer
        shift_at = 6000
        gear_ratios = {
            'final_drive': 3.716,
            1: 4.721,
            2: 1.802,
            3: 1.100,
            4: 0.8,
            5: 0.6,
            6: 0.5
        }

        random_car = Car(name=f"Car-{counter}", cylinders=cylinders, displacement_cc=displacement_cc, turbo_type=turbo_type,
                         clutch_type=clutch_type, weight_type=weight_type, body_kit_type=body_kit, tyre_type=tyre_type,
                         shift_at=shift_at, gear_ratios=gear_ratios)
        cost = random_car.calculate_cost()
        if cost <= max_cost and cost > max_cost - 1000:
            eligible_cars.append(random_car)

    scores = {}
    cars = {}
    for car in eligible_cars:
        cars[car.name] = copy.deepcopy(car)
        run = car.dyno(plot=False, r=10000)
        time_to_distance = (list({k: v for k, v in run.items() if k >= optimized_distance}.values())[0])
        # print(time_to_distance)
        scores[car.name] = time_to_distance

    # print(scores)
    best_car_index = max(scores, key=scores.get)
    # print(best_car_index)

    with open('next_car.pkl', 'wb') as output:
        pickle.dump(cars[best_car_index], output, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    generate_car(20000,300,100)