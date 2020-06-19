import sys, os

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci


# SNOW DEFAULT FUNCTIONS
def SnowChangeAccelD(weather_val, veh_id, param):
    if weather_val <= 35:
        traci.vehicle.setAccel(veh_id, param * 0.90)
    elif weather_val <= 70:
        traci.vehicle.setAccel(veh_id, param * 0.80)
    else:
        traci.vehicle.setAccel(veh_id, param * 0.70)

def SnowChangeDecelD(weather_val, veh_id, param):
    if weather_val <= 35:
        traci.vehicle.setDecel(veh_id, param * 0.90)
    elif weather_val <= 70:
        traci.vehicle.setDecel(veh_id, param * 0.80)
    else:
        traci.vehicle.setDecel(veh_id, param * 0.70)

def SnowChangeMaxSpeedD(weather_val, veh_id, param):
    pass

def SnowChangeMinGapD(weather_val, veh_id, param):
    if weather_val <= 35:
        traci.vehicle.setMinGap(veh_id, param * 1.3)
    elif weather_val <= 70:
        traci.vehicle.setMinGap(veh_id, param * 1.5)
    else:
        traci.vehicle.setMinGap(veh_id, param * 1.7)

def SnowChangeHeadwayTimeD(weather_val, veh_id, param):
    if weather_val <= 35:
        traci.vehicle.setTau(veh_id, param * 1.8)
    elif weather_val <= 70:
        traci.vehicle.setTau(veh_id,  param * 3.9)
    else:
        traci.vehicle.setTau(veh_id, param * 7)

def SnowChangeSpeedFactorD(weather_val, veh_id, param):
    if weather_val <= 35:
        traci.vehicle.setSpeedFactor(veh_id, 0.9)
    elif weather_val <= 70:
        traci.vehicle.setSpeedFactor(veh_id, 0.75)
    else:
        traci.vehicle.setSpeedFactor(veh_id, 0.6)

def SnowChangeColorD(weather_val, veh_id, param):
    color_values = list(param)
    color_values[0] = 181
    color_values[1] = 211
    color_values[2] = 231
    traci.vehicle.setColor(veh_id, tuple(color_values))


# RAIN DEFAULT FUNCTIONS
def RainChangeAccelD(weather_val, veh_id, param):
    if weather_val <= 35:
        traci.vehicle.setAccel(veh_id, param * 0.95)
    elif weather_val <= 70:
        traci.vehicle.setAccel(veh_id, param * 0.85)
    else:
        traci.vehicle.setAccel(veh_id, param * 0.75)


def RainChangeDecelD(weather_val, veh_id, param):
    if weather_val <= 35:
        traci.vehicle.setDecel(veh_id, param * 0.95)
    elif weather_val <= 70:
        traci.vehicle.setDecel(veh_id, param * 0.85)
    else:
        traci.vehicle.setDecel(veh_id, param * 0.75)


def RainChangeMaxSpeedD(weather_val, veh_id, param):
    pass


def RainChangeMinGapD(weather_val, veh_id, param):
    if weather_val <= 35:
        traci.vehicle.setMinGap(veh_id, param * 1.15)
    elif weather_val <= 70:
        traci.vehicle.setMinGap(veh_id, param * 1.3)
    else:
        traci.vehicle.setMinGap(veh_id, param * 1.5)


def RainChangeHeadwayTimeD(weather_val, veh_id, param):
    if weather_val <= 35:
        traci.vehicle.setTau(veh_id, param * 1.5)
    elif weather_val <= 70:
        traci.vehicle.setTau(veh_id, param * 2)
    else:
        traci.vehicle.setTau(veh_id, param * 2.5)


def RainChangeSpeedFactorD(weather_val, veh_id, param):
    if weather_val <= 35:
        traci.vehicle.setSpeedFactor(veh_id, 0.96)
    elif weather_val <= 70:
        traci.vehicle.setSpeedFactor(veh_id, 0.92)
    else:
        traci.vehicle.setSpeedFactor(veh_id, 0.88)


def RainChangeColorD(weather_val, veh_id, param):
    color_values = list(param)
    color_values[0] /= 2
    color_values[1] /= 3
    color_values[2] = 255
    traci.vehicle.setColor(veh_id, tuple(color_values))
