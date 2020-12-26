from game_core.car import Car

name = "De Roelhand V1"

'''
Engine type
$1000 per cylinder
$1.5 per cc

More cylinders = more rpm & more torque
More displacement = more torque
'''
cylinders = 4
displacement_cc = 800
# ---------------------------------- #
'''
Aspiration (Boost)

"None"                          : $0
"S": [3000, 6000, 40]           : $1000
"M": [4000, 7000, 65]           : $1600
"L": [5000, 8000, 100]          : $2250
"H": [6000, 9000, 150]          : $3000

"Supercharger-V1": 10% Boost    : $2000
"Supercharger-V2": 20% Boost    : $3500
"Supercharger-V3": 40% Boost    : $6000
}
'''
turbo_type = "S"
# ---------------------------------- #
'''
Transmission (Gearbox)

4-Speed transmission            : $500
5-Speed transmission            : $700
6-Speed transmission            : $900
7-Speed transmission            : $1100
8-Speed transmission            : $1300
'''
shift_at = 6350
gear_ratios = {
    'final_drive': 3.716,
    1: 4.721,
    2: 2.802,
    3: 1.700,
    4: 1.2,
    5: 0.86,
    6: 0.65
}
# ---------------------------------- #
'''
Better clutch means faster shifting

"Stock": 0.3s                   : $100
"Street": 0.175s                : $225
"Race": 0.1s                    : $350
'''
clutch_type = "Stock"
# ---------------------------------- #
'''
Weight type

"Heavy": 1600kg                 : $1000
"Medium": 1400kg                : $1500
"Light": 1200kg                 : $2000
"Ultra-light": 1000kg           : $2500
'''
weight_type = "Medium"
# ---------------------------------- #
'''
Body kit (better body kit provides better drag coefficient)

"Stock":0.45                    : $500
"Street":0.40                   : $1000
"Sport":0.35                    : $1500
"Performance":0.30              : $2000
"Race":0.25                     : $2500
'''
body_kit_type = "Street"
# ---------------------------------- #
'''
Tyre type (better tyres reduce roll resistance)

"H":0.85                        : $ 250
"V":0.87                        : $ 350
"Z":0.89                        : $ 450
"W":0.91                        : $ 550
"Y":0.93                        : $ 650
'''
tyre_type = "Z"
# ---------------------------------- #
def create():
    return Car(name=name, cylinders=cylinders, displacement_cc=displacement_cc, turbo_type=turbo_type,
          clutch_type=clutch_type,
          shift_at=shift_at, weight_type=weight_type, gear_ratios=gear_ratios, body_kit_type=body_kit_type,
          tyre_type=tyre_type)

if __name__ == "__main__":
    car = create()
    print(f"Total cost: ${round(car.calculate_cost())}")
    create().dyno()
