#! /usr/bin/env python
# encoding = utf-8

import datetime
import logging

logger = logging.getLogger('1Energy.logging')


class Energy(object):
    def __init__(self, drone):
        self.drone = drone
        # directory = "/home/nvidia/energy_log/"
        directory = "./log/"
        now = datetime.datetime.now()
        self.f = open(directory + now.strftime('%Y-%m-%d %H:%M:%S'), 'w')

    def write(self, sequence_num, activate, fb, lr, ud, a):
        logger.debug("%d %s %f %f %f %f" % (sequence_num, activate, fb, lr, ud, a))
        q = self.drone.attitude.quaternion
        battery = self.drone.battery_state
        vel = self.drone.velocity.vector
        logger.debug(str(self.drone.attitude))
        logger.debug(str(self.drone.battery_state))
        logger.debug(str(self.drone.gps_position.latitude))

        # print self.drone.attitude
        # print self.drone.battery_state
        # print self.drone.gps_position.latitude
        data = "%s\t%d\t%s\t%f\t%f\t%f\t%f\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" \
               % (datetime.datetime.now(), sequence_num, activate, fb, lr, ud, a, q.x, q.y, q.z, q.w,
                  battery.voltage, battery.current, battery.percentage,
                  vel.x, vel.y, vel.z,
                  self.drone.gps_position.latitude, self.drone.gps_position.longitude, self.drone.gps_position.altitude)

        self.f.write(data)


if __name__ == "__main__":
    energy = Energy()
    energy.write(1, True, 1, 2, 3, 4)
    energy.write(2, False, 3, 2, 5, 5)


