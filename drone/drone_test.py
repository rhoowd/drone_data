#!/usr/bin/env python
# encoding = utf-8

"""
    This is for test without connecting drone
"""
import logging

logger = logging.getLogger('Energy.drone_test')

class Q:
    x = 0
    y = 0
    z = 0
    w = 0


class Temp:
    quaternion = Q()
    vector = Q()

    voltage = 0
    current = 0
    percentage = 0

    latitude = 0
    longitude = 0
    altitude = 0


class Drone(object):

    def __init__(self):
        self.attitude = Temp()
        self.flight_status = 0
        self.battery_state = Temp()
        self.velocity = Temp()
        self.gps_health = 0
        self.gps_position = Temp()
        self.local_position = None

    """ Service functions """
    def activate(self):
        return True

    def drone_version(self):
        pass

    def arm(self):
        pass

    def disarm(self):
        pass

    def takeoff(self):
        print "take off"
        return 0

    def land(self):
        print "land"
        return 0

    def gohome(self):
        pass

    def request_sdk_control(self):
        return 0
        # result = self.sdkControlAuthorityService(control_enable=SDKControlAuthorityRequest.REQUEST_CONTROL)

    def release_sdk_control(self):
        return 0
        # result = self.sdkControlAuthorityService(control_enable=SDKControlAuthorityRequest.RELEASE_CONTROL)

    """ Flight control functions """
    def flight_control_generic(self):
        pass

    def flight_control_velocity(self, x_vel, y_vel, z_vel, yaw_rate):
        logger.debug("Flight control velocity %f %f %f %f" % (x_vel, y_vel, z_vel, yaw_rate))

    def flight_control_position(self, x_offset, y_offset, z, yaw):
        logger.debug("Flight control position (offset) %f %f %f %f" % (x_offset, y_offset, z, yaw))


if __name__ == "__main__":
    drone = Drone()
    result = drone.activate()
    print result
    result = drone.request_sdk_control()
    print result

    drone.takeoff()

    print drone.attitude
    print drone.flight_status
    print drone.battery_state
    print drone.velocity
    print drone.gps_position

    drone.flight_control_velocity(30, 30, 30)
    drone.flight_control_velocity(30, 30, 30)

    end_result = drone.release_sdk_control()
    print end_result
