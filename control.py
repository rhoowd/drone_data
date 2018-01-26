#! /usr/bin/env python
# encoding = utf-8
import time
from Queue import Queue
import threading
import sys
from path import Path
import math
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
        while True:
            self.seq_num += 1
            time.sleep(0.1)
            if not self.command_queue.empty():
                command = self.command_queue.get()
                if command is 'q':
                    break
                elif command is 'h':
                    print "Help:"
                    print "\t  0: stop"
                    print "\t  1: rotate at the fixed point clockwise"
                    print "\t  2: rotate at the fixed point counter-clockwise"
                    print "\t 1x: move forward and backward with vel x"
                    print "\t 2x: move left and right with vel x"
                else:
                    self.path.set_path_mode(command)

            # TODO: Something related to activation

            local_vel = self.path.get_action()
            global_vel = self.convert_local_to_global(local_vel)
            self.drone.flight_control_velocity(global_vel['x'], global_vel['y'], global_vel['z'], global_vel['yaw'])

            # TODO: update self.is_activate
            self.energy.write(self.seq_num, self.is_activate,
                              local_vel['fb'], local_vel['lr'], local_vel['ud'], local_vel['a'])

            self.print_progress()

        return 0

    def convert_local_to_global(self, l_vel):
        # TODO: Implement this function
        yaw = self.get_yaw()

        g_vel = dict()
        g_vel['x'] = l_vel['fb']*math.cos(math.radians(yaw)) - l_vel['lr']*math.sin(math.radians(yaw))
        g_vel['y'] = l_vel['fb']*math.sin(math.radians(yaw)) + l_vel['lr']*math.cos(math.radians(yaw))
        g_vel['z'] = l_vel['ud']
        g_vel['yaw'] = l_vel['a']

        return g_vel

    def get_yaw(self, q):
        ret = math.degrees(math.atan2(2.0 * (q.w * q.x + q.y * q.z),
                                      -1.0 + 2.0 * (q.x * q.x + q.y * q.y)))
        return ret

    def print_progress(self):
        if self.seq_num % 10 == 0:
            print ".",
            sys.stdout.flush()
