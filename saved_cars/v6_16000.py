from game_core.car import Car
from game_core.engine_curve import calculate_curve

name = "V6-17000"

'''
Engine type
$500 per cylinder
$2 per cc

More cylinders = more rpm & more torque
More displacement = more torque
'''
cylinders = 6
displacement_cc = 537
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
turbo_type = "M"
# ---------------------------------- #
'''
Transmission (Gearbox)

4-Speed transmission            : $500
5-Speed transmission            : $700
6-Speed transmission            : $900
7-Speed transmission            : $1100
8-Speed transmission            : $1300
'''
shift_at = 7000
gear_ratios = {
    'final_drive': 1.66,
    1: 5.721,
    2: 3.902,
    3: 2.60,
    4: 1.8,
    5: 1.30,
    6: 1.0
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
clutch_type = "Race"
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
weight_type = "Super-light"
# ---------------------------------- #
'''
Body kit (better body kit provides better drag coefficient)

"Stock":0.45                    : $500
"Street":0.43                   : $900
"Sport":0.41                    : $1400
"Performance":0.39              : $1800
"Race":0.37                     : $2200
'''
body_kit_type = "Street"
# ---------------------------------- #
'''
'2-wheel'                       : $0
'4-wheel'                       : $350
'''
drive_type = '2-wheel'
# ---------------------------------- #
'''
Tyre type (better tyres reduce roll resistance)

"H":r0.85, t0.72                     : $ 250
"V":r0.87  t0.79                     : $ 350
"Z":r0.89  t0.86                     : $ 450
"W":r0.91, t0.93                     : $ 550
"Y":r0.93, t1                        : $ 650
'''
tyre_type = "Z"
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
nos_type = "None"
# ---------------------------------- #

def create():
    return Car(name=name, cylinders=cylinders, displacement_cc=displacement_cc, turbo_type=turbo_type,
          clutch_type=clutch_type,
          shift_at=shift_at, weight_type=weight_type, gear_ratios=gear_ratios, body_kit_type=body_kit_type,
          tyre_type=tyre_type, nos_type=nos_type, drive=drive_type)

if __name__ == "__main__":
    car = create()
    print(f"Total cost: ${round(car.calculate_cost())}")
    # calculate_curve(car)
    create().dyno()
