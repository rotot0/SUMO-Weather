#!/usr/bin/env python3
from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random

# import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
    # path to weather (!)
    sys.path.append(tools + '/weather_project/weather')
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary
# import weather
from weather import *
import traci


def generate_routefile():
    random.seed(42)
    N = 2000  # number of time steps
    # demand per second from different directions
    pWE = 1. / 20
    pEW = 1. / 21
    pNS = 1. / 30
    pUp = 1./ 20
    pSpec = 1. / 50

    # generates vehicles
    with open("data/cross.rou.xml", "w") as routes:
        print("""<routes>
        <vType id="typeWE" accel="3" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="55.55" emergencyDecel="10" \
guiShape="passenger"/>
        <vType id="typeNS" accel="1.2" decel="4" sigma="0.8" length="7" minGap="3" maxSpeed="30" guiShape="bus"/>

        <route id="right" edges="51o 1i 2o 52i" />
        <route id="new" edges="top1i top2o" />
        <route id="left" edges="52o 2i 1o 51i" />
        <route id="down" edges="updown 4i 3o 53i" />
        <route id="up" edges="53o 3i 4o upup" />
        <route id="new2" edges="top2i upup" />
        <route id="new3" edges="top2i 4i 3o 53i" />
        """, file=routes)
        vehNr = 0
        for i in range(N):
            if random.uniform(0, 1) < pWE:
                print('    <vehicle id="right_%i" type="typeWE" route="right" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pSpec:
                print('    <vehicle id="new2_%i" type="typeWE" route="new2" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pSpec:
                print('    <vehicle id="new3_%i" type="typeWE" route="new3" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pEW:
                print('    <vehicle id="left_%i" type="typeWE" route="left" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pNS:
                print('    <vehicle id="down_%i" type="typeNS" route="down" depart="%i" color="1,0,0"/>' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pWE:
                print('    <vehicle id="new_%i" type="typeWE" route="new" depart="%i"/>' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pUp:
                print('    <vehicle id="up_%i" type="typeNS" route="up" depart="%i"/>' % (
                    vehNr, i), file=routes)
                vehNr += 1
        print("</routes>", file=routes)

def run():
    weather_enable = 1 # weather_enable = 0 if you want to disable weather

    if weather_enable:
        weather_main()
    else:
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()

    traci.close()
    sys.stdout.flush()


if __name__ == "__main__":
    # start sumo as a server, then connect and run
    sumoBinary = checkBinary('sumo-gui')

    generate_routefile()

    # start sumo using traci
    traci.start([sumoBinary, "-c", "data/cross.sumocfg",
                             "--tripinfo-output", "tripinfo.xml",
                             "--collision.mingap-factor", "0",
                             "--no-warnings", "1",
                             "--ignore-route-errors", "1",])
    run()
