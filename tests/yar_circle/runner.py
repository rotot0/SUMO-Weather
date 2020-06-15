#!/usr/bin/env python3
from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
    sys.path.append(tools + '/weather_project')
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary
from weather import *
import traci

def run():
    weather_enable = 1 # weather_enable = 0 if you want to disable weather

    if weather_enable:
        weather_main()
    else:
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
    traci.close()
    sys.stdout.flush()


# this is the main entry point of this script
if __name__ == "__main__":
    sumoBinary = checkBinary('sumo-gui')

    # start sumo using traci
    traci.start([sumoBinary, "-c", "data/models/yar.sumocfg",
                 "--tripinfo-output", "tripinfo.xml",
                 "--collision.mingap-factor", "0",
                 "--fcd-output", "data/result_rain.xml",
                 "--ignore-route-errors", "1",
                 "--no-warnings", "1"])
    # runs simulation
    run()
