#! /usr/bin/env python
# encoding = utf-8

import sys
import time
import math
import threading
from Queue import Queue
from path import Path
import logging

logger = logging.getLogger('Energy.control')


class Control(object):
    def __init__(self, drone, energy):
        self.drone = drone
        self.energy = energy
        self.path = Path()
        self.command_queue = Queue()
        self.seq_num = 0
        self.is_activate = False
        threading._start_new_thread(self.get_command_from_keyboard, ())

    def get_command_from_keyboard(self):
        while True:
            command = raw_input("type or (q)uit> ")
            self.command_queue.put(command)
            if command is 'q':
                break

    def run(self):
        result = self.drone.activate()
        logger.debug("Activate: " + str(result))
        print "Press any key to start"
        self.command_queue.get()
        print "start"
        while True:
            self.seq_num += 1
            time.sleep(0.1)
            if not self.command_queue.empty():
                command = self.command_queue.get()
                if command is 'q':
                    break
                elif command is 's':
                    self.drone.takeoff()
                    time.sleep(10)
                elif command is 'l':
                    self.drone.land()
                    time.sleep(10)
                elif command is 'h':
                    print "Help:"
                    print "\t  0: stop"
                    print "\t 1x: move forward and backward with vel x"
                    print "\t 2x: move left and right with vel x"
                    print "\t 3x: rotate at the fixed point clockwise"
                    print "\t 4x: rotate at the fixed point counter-clockwise"
                else:
                    self.path.set_path_mode(command)

            # TODO: Something related to activation
            result = self.drone.request_sdk_control()
            logger.debug("Request sdk control: " + str(result) + " yaw: "+ str(self.get_yaw()))
            local_vel = self.path.get_action()
            global_vel = self.convert_local_to_global(local_vel)

            self.drone.flight_control_velocity(global_vel['x'], global_vel['y'], global_vel['z'], global_vel['yaw'])

            print local_vel, "->", global_vel
            # TODO: update self.is_activate
            self.energy.write(self.seq_num, self.is_activate,
                              local_vel['fb'], local_vel['lr'], local_vel['ud'], local_vel['a'])

            self.print_progress()

        return 0

    def convert_local_to_global(self, l_vel):
        # TODO: Implement this function
        yaw = self.get_yaw()

        g_vel = dict()

        # g_vel['x'] = l_vel['fb']
        # g_vel['y'] = l_vel['lr']
        g_vel['x'] = l_vel['fb']*math.cos(math.radians(yaw)) - l_vel['lr']*math.sin(math.radians(yaw))
        g_vel['y'] = l_vel['fb']*math.sin(math.radians(yaw)) + l_vel['lr']*math.cos(math.radians(yaw))
        g_vel['z'] = l_vel['ud']
        g_vel['yaw'] = l_vel['a']

        return g_vel

    def get_yaw(self):

        q = self.drone.attitude.quaternion
        q1 = q.w
        q2 = q.x
        q3 = q.y
        q4 = q.z
        
        ret = math.degrees(math.atan2(2.0 * (q4 * q1 + q2 * q3),
                                      -1.0 + 2.0 * (q1 * q1 + q2 * q2)))
        return ret

    def print_progress(self):
        if self.seq_num % 10 == 0:
            print ".",
            sys.stdout.flush()
