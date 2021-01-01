from game_core.car import Car
from game_core.engine_curve import calculate_curve, calculate_max

name = "V8-17000"

'''
Engine type
$500 per cylinder
$2 per cc

More cylinders = more rpm & more torque
Each cylinder gives 500rpm + 5000 base
More displacement = more torque
'''
cylinders = 8
displacement_cc = 420
# ---------------------------------- #
'''
Aspiration (Boost)

"None"                          : $0
"SS": [2500, 5500, 30]          : $750
"S": [3000, 6000, 50]           : $1000
"M": [4000, 7000, 90]           : $1600
"L": [4500, 7500, 120]          : $2000
"XL": [5000, 8000, 150]         : $2250
"H": [5500, 8500, 200]          : $2500

"Supercharger-V1": 10% Boost    : $2000
"Supercharger-V2": 20% Boost    : $3500
"Supercharger-V3": 40% Boost    : $6000
}
'''
turbo_type = "L"
# ---------------------------------- #
'''
Transmission (Gearbox)

4-Speed transmission            : $500
5-Speed transmission            : $700
6-Speed transmission            : $900
7-Speed transmission            : $1100
8-Speed transmission            : $1300
'''
shift_at = 8000
gear_ratios = {
    'final_drive': 2.3,
    1: 8.021,
    2: 3.500,
    3: 2.405,
    4: 1.550,
    5: 1.150,
    6: 0.875,
    7: 0.675,
    8: 0.575,
}
# ---------------------------------- #
'''
Better clutch means faster shifting

"Stock": 0.3s                   : $100
"Street": 0.25s                 : $250
"Sport": 0.2s                   : $400
"Performance": 0.15s            : $550
"Race": 0.1s                    : $700
'''
clutch_type = "Street"
# ---------------------------------- #
'''
Weight type

"Super-heavy": 1600kg           : $1000
"Heavy": 1500kg                 : $1400
"Medium": 1400kg                : $1800
"Medium-light": 1300kg          : $2200
"Light": 1200kg                 : $2600
"Super-light": 1100kg           : $3000
"Ultra-light": 1000kg           : $3400
'''
weight_type = "Medium"
# ---------------------------------- #
'''
Body kit (better body kit provides better drag coefficient)

"Stock":0.45                    : $500
"Street":0.43                   : $900
"Sport":0.41                    : $1400
"Performance":0.39              : $1800
"Race":0.37                     : $2200
'''
body_kit_type = "Performance"
# ---------------------------------- #
'''
Tyre type (better tyres reduce roll resistance)

"H":0.85                        : $ 250
"V":0.87                        : $ 350
"Z":0.89                        : $ 450
"W":0.91                        : $ 550
"Y":0.93                        : $ 650
'''
tyre_type = "Y"
# ---------------------------------- #
'''
NOS (activate nitro with left/right arrow)
Burns for 4 seconds

"None"                           : $ 0
75HP                             : $ 750
100HP                            : $ 1000
125HP                            : $ 1250
150HP                            : $ 1500
'''
nos_type = "100HP"
# ---------------------------------- #

def create():
    return Car(name=name, cylinders=cylinders, displacement_cc=displacement_cc, turbo_type=turbo_type,
          clutch_type=clutch_type,
          shift_at=shift_at, weight_type=weight_type, gear_ratios=gear_ratios, body_kit_type=body_kit_type,
          tyre_type=tyre_type, nos_type=nos_type)

if __name__ == "__main__":
    car = create()
    print(f"Total cost: ${round(car.calculate_cost())}")
    # calculate_curve(car)
    print(calculate_max(car))
    create().dyno()
