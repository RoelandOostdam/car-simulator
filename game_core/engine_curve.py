import matplotlib.pyplot as plt
import game_core.helpers as helpers

def calculate_max(car):
    torque, power = {}, {}
    for x in range(1000, 12000, 100):
        car.rpm = x
        power[x] = helpers.watt_to_bhp(car.power())
        torque[x] = car.torque()

    return {'torque':round(max(torque.values())), 'power':round(max(power.values()))}

def calculate_curve(car):
    torque, power = {}, {}
    for x in range(1000,12000,100):
        car.rpm = x
        # power[x] =  helpers.watt_to_bhp(car.power())
        power[x] =  helpers.watt_to_bhp(car.power())
        torque[x] = car.torque()


    color = 'tab:red'
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('rpm*1000')
    ax1.set_ylabel('Power (bhp)', color=color)
    ax1.plot(power.keys(), power.values(), c=color)
    ax1.grid(axis='x')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:orange'
    ax2.set_xlabel('rpm*1000')
    ax2.set_ylabel('Torque (Nm)', color=color)
    ax2.plot(torque.keys(), torque.values(), c=color)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.xticks(range(1000,13000,1000), range(1,13,1))
    plt.show()
7