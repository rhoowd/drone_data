#!/usr/bin/env python
# coding=utf8
from drone.drone_test import Drone
# from drone.dji_drone import Drone
from energy_logging import Energy
from control import Control
import config
import logging

logger = logging.getLogger('Energy')

if __name__ == "__main__":
    drone = Drone()

    energy = Energy(drone)
    control = Control(drone, energy)
    control.run()

    logger.info("END")

