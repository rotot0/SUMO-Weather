import os, sys

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
    print();
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci
import traci.constants as tc

sumoBinary = "sumo-gui"
sumoCmd = [sumoBinary, "-c", "hello.sumocfg"]

import traci
traci.start(sumoCmd)
step = 0
while step < 1000:
   traci.simulationStep()
   if traci.inductionloop.getLastStepVehicleNumber("1") > 0:
       traci.trafficlight.setRedYellowGreenState("1", "GrGr")
   step += 1

traci.close()

