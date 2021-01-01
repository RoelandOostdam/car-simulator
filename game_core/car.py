import game_core.helpers as helpers
import matplotlib.pyplot as plt
from game_core.engine_curve import calculate_max

class Car:
    def __init__(self, name, cylinders, displacement_cc, turbo_type, clutch_type, shift_at, weight_type, gear_ratios, body_kit_type, tyre_type, nos_type, drive):
        # Specs
        self.name = name

        # Engine
        self.cylinders = cylinders
        self.displacement_cc = displacement_cc
        self.max_torque = (self.displacement_cc/9) * self.cylinders
        self.max_rpm = 5000 + (self.cylinders * 500)

        # Aspiration
        self.turbo_type = turbo_type
        turbo_types = {
            "SS": [2500,6000,30],
            "S": [3000,6000,50],
            "M": [4000,7000,90],
            "L": [4500,7500,120],
            "XL": [5000,8000,150],
            "H": [5500,8500,200],
            "Supercharger-V1": self.max_torque*0.1,
            "Supercharger-V2": self.max_torque*0.2,
            "Supercharger-V3": self.max_torque*0.4,
        }
        if self.turbo_type == "None":
            self.aspiration = False
        elif "Supercharger" in self.turbo_type:
            self.aspiration = 'Supercharged'
            self.boost_nm = helpers.bhp_to_watt(turbo_types[self.turbo_type])
        else:
            self.aspiration = 'Turbo'
            self.turbo_rpm_min = turbo_types[self.turbo_type][0]
            self.turbo_rpm_max = turbo_types[self.turbo_type][1]
            self.boost_nm = helpers.bhp_to_watt(turbo_types[self.turbo_type][2])

        # Transmission
        self.shift_at = shift_at
        self.gear_ratios = gear_ratios
        self.gear_count = len(self.gear_ratios)-1

        # Clutch
        self.clutch_type = clutch_type
        clutch_types = {
            "Stock": 0.3,
            "Street": 0.25,
            "Sport": 0.20,
            "Performance": 0.15,
            "Race": 0.1,
        }
        self.clutch_time = clutch_types[self.clutch_type]

        # Chassis
        self.weight_type = weight_type
        weight_options = {
            "Super-heavy": 1600,
            "Heavy": 1500,
            "Medium-light": 1400,
            "Medium": 1300,
            "Light": 1200,
            "Super-light": 1100,
            "Ultra-light": 1000,
        }
        self.weight_kg = weight_options[self.weight_type]

        self.body_kit_type = body_kit_type
        body_kits = {
            "Stock":0.45,
            "Street":0.43,
            "Sport":0.41,
            "Performance":0.39,
            "Race":0.37,
        }
        self.drag_coefficient = body_kits[self.body_kit_type]

        #
        self.drive = drive
        self.drive_types = {
            '2-wheel':2,
            '4-wheel':4,
        }
        self.drive = self.drive_types[self.drive]

        # Tyres
        self.tyre_type = tyre_type
        tyre_types = {
            "H":[0.85, 0.72],
            "V":[0.87, 0.79],
            "Z":[0.89, 0.86],
            "W":[0.91, 0.93],
            "Y":[0.93, 1],
        }
        self.roll_resistance = tyre_types[self.tyre_type][0]
        self.tyre_traction = tyre_types[self.tyre_type][1]
        # ----------------------------------------------
        # NOS
        self.nos_type = nos_type
        nos_types = {
            'None':0,
            '75HP':75,
            '100HP':100,
            '125HP':125,
            '150HP':150,
        }
        self.nos_type = nos_types[nos_type]
        # ----------------------------------------------
        # Internal variables
        # Naming
        if self.cylinders == 4:
            engine_type = '4-inline'
        else:
            engine_type = f"V{self.cylinders}"
        self.name_engine_type = f"{self.displacement_cc * self.cylinders / 1000}L {engine_type}"
        if self.aspiration == 'Turbo':
            self.name_engine_type += f" {self.turbo_type}-Turbo"
        elif self.aspiration == 'Supercharged':
            self.name_engine_type = f"Supercharged({self.turbo_type[-2:]}) {self.name_engine_type}"
        self.name_transmission = f"{self.gear_count}-speed transmission"
        self.name_chassis = f"{self.weight_type}"
        self.name_tyres = f"Type-{self.tyre_type}"
        self.name_body_kit = f"{self.body_kit_type}"
        # local parameters
        self.gear = 0
        self.rpm = 1000
        self.min_rpm = 2500
        self.speed_mps = 0
        self.distance_traveled = 0
        self.shifting = False
        x = calculate_max(self)
        self.dyno_max_power = x['power']
        self.dyno_max_torque = x['torque']
        self.total_cost = self.calculate_cost()
        self.finished = False
        self.nos_time = 0
        self.nos_activated = False
        self.tcs = False

    def torque(self):
        rpm_percentage = (max(self.min_rpm,self.rpm) / self.max_rpm) * 100
        torque = ((100 + (-(rpm_percentage-50)**2)/25) / 100) * self.max_torque
        return max(0,torque)

    def power(self):
        if self.shifting != False:
            return 0
        return self.torque() * self.rpm / 9.5488 + self.boost()

    def boost(self):
        if self.aspiration == False:
            return 0
        elif self.aspiration == 'Turbo':
            if self.rpm < self.turbo_rpm_min:
                return 0
            return min(1,((self.rpm - self.turbo_rpm_min) / (self.turbo_rpm_max - self.turbo_rpm_min))) * self.boost_nm
        elif self.aspiration == 'Supercharged':
            return self.boost_nm

    def nos(self):
        if self.nos_type == False or self.nos_activated == False:
            return 0
        if self.nos_time*10 >= 4:
            return 0
        return helpers.bhp_to_watt(self.nos_type) * (4-(min(4,self.nos_time*10)))/4

    def air_drag(self):
        return (0.9 * self.drag_coefficient * 2 * 2.0 * ((self.speed_mps**2)))

    def traction(self):
        return 0.7 * ((self.weight_kg * 9.81)/4) * self.drive

    def accelerate(self, seconds):
        if self.shifting != False:
            self.shifting -= seconds * 10 / self.clutch_time
        if self.shifting <= 0:
            self.shifting = False
        if self.rpm >= self.shift_at and self.gear < self.gear_count:
            self.gear += 1
            self.shifting = 1
        power = self.power() + self.nos()
        self.tcs = False
        if self.power() / self.weight_kg / 60 > self.traction() / self.weight_kg:
            self.tcs = True
            power = self.traction() * 60

        # print(self.power() / self.weight_kg / 60, self.traction() / self.weight_kg, self.tcs)

        speed_delta = power / self.weight_kg * seconds * self.roll_resistance - (self.air_drag() * seconds / 60)
        self.speed_mps += speed_delta
        self.rpm = min(self.max_rpm,max(self.min_rpm,min(self.max_rpm,self.speed_mps * self.gear_ratios['final_drive'] * self.gear_ratios[self.gear]) * 60))
        self.distance_traveled += self.speed_mps * seconds
        if self.nos_activated:
            self.nos_time += seconds
        # if helpers.mps_to_kph(self.speed_mps) >= 100:
        #     self.nos_activated = True

    def dyno(self, plot=True, r=250, verbose=False):
        speed, rpm, distance_traveled = {}, {}, {}
        hit100, zero100_time = False, 999
        for x in range(1, r):
            x /= 10
            self.accelerate(0.01)
            if helpers.mps_to_kph(self.speed_mps) >= 100 and hit100 == False:
                zero100_time = x
                hit100 = True
            if verbose:
                print(
                f"{x}, {round(helpers.mps_to_kph(self.speed_mps))} KPH, {round(self.rpm)} RPM, {round(helpers.watt_to_bhp(self.power()))} HP, Gear: {self.gear}")
            speed[x] = helpers.mps_to_kph(self.speed_mps)
            rpm[x] = self.rpm
            distance_traveled[x] = self.distance_traveled

        if plot:
            fig, ax1 = plt.subplots()
            plt.title(f"0-100 in {zero100_time}s")

            color = 'tab:red'
            ax1.set_xlabel('tijd (s)')
            ax1.set_ylabel('km/u', color=color)
            ax1.plot(speed.keys(), speed.values(), color=color, linewidth=2)
            ax1.tick_params(axis='y', labelcolor=color)

            ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

            color = 'tab:blue'
            ax2.set_ylabel('RPM', color=color)  # we already handled the x-label with ax1
            ax2.plot(rpm.keys(), rpm.values(), color=color, linewidth=2)
            ax2.tick_params(axis='y', labelcolor=color)
            ax2.grid(axis='y')
            plt.show()

        return distance_traveled

    def calculate_cost(self):
        total_cost = 0
        total_cost += self.cylinders * 500
        total_cost += self.displacement_cc * self.cylinders * 2
        total_cost += \
        {'None': 0, 'SS':750, 'S': 1000, 'M': 1600, 'L': 2000, 'XL':2250,'H': 2500, 'Supercharger-V1': 2000, 'Supercharger-V2': 3500,
         'Supercharger-V3': 6000}[self.turbo_type]
        total_cost += 500 + ((len(self.gear_ratios) - 1 - 4) * 200)
        total_cost += {'Stock': 100, 'Street': 250, 'Sport': 400, 'Performance': 550, 'Race': 700}[self.clutch_type]
        total_cost += {'Super-heavy': 1000, 'Heavy':1400, 'Medium': 1800, 'Medium-light':2200, 'Light': 2600,'Super-light':3000, 'Ultra-light': 3400}[self.weight_type]
        total_cost += {'Stock': 500, 'Street': 900, 'Sport': 1400, 'Performance': 1800, 'Race': 2200}[
            self.body_kit_type]
        total_cost += {'H': 250, 'V': 350, 'Z': 450, 'W': 550, 'Y': 650}[self.tyre_type]
        total_cost += {2:0, 4:350}[self.drive]
        total_cost += {0:0, 75: 750, 100: 1000, 125: 1250, 150: 1500}[self.nos_type]
        return total_cost
