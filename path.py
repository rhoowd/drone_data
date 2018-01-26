#! /usr/bin/env python
# encoding = utf-8
import logging

logger = logging.getLogger('Energy.path')


class Path(object):

    def __init__(self):
        self.path_mode = 0
        self.cnt = 0

        self.period_line = 100  # unit: 0.1 sec

        self.local_vel = dict()
        self.local_vel['fb'] = 0.0
        self.local_vel['lr'] = 0.0
        self.local_vel['ud'] = 0.0
        self.local_vel['a'] = 0.0

    def set_path_mode(self, mode):
        print mode
        self.cnt = 0
        try:
            self.path_mode = int(mode)
        except ValueError:
            logger.warning("input \'mode\' is not integer -> mode 0")
            self.path_mode = 0

    def get_action(self):

        self.update_action()
        return self.local_vel

    def update_action(self):
        if 10 < self.path_mode <= 20:
            self.act_line(float(self.path_mode % 10), 'fb')

        else:
            self.local_vel['fb'] = 0.0
            self.local_vel['lr'] = 0.0
            self.local_vel['ud'] = 0.0
            self.local_vel['a'] = 0.0

    def act_line(self, vel, dir):

        self.cnt += 1
        direction = ((self.cnt / self.period_line % 2)-0.5) *2
        pause_flag = self.cnt % self.period_line < 10

        self.local_vel['fb'] = 0.0
        self.local_vel['lr'] = 0.0
        self.local_vel['ud'] = 0.0
        self.local_vel['a'] = 0.0

        if not pause_flag:
            if dir == 'fb':
                self.local_vel['fb'] = vel * direction
            elif dir == 'lr':
                self.local_vel['lr'] = vel * direction

        print self.cnt, self.local_vel

    def act_circle(self, vel, dir):

        self.cnt += 1
        direction = ((self.cnt / self.period_line % 2)-0.5) *2
        pause_flag = self.cnt % self.period_line < 10

        self.local_vel['fb'] = 0.0
        self.local_vel['lr'] = 0.0
        self.local_vel['ud'] = 0.0
        self.local_vel['a'] = 0.0

        if not pause_flag:
            if dir == 'fb':
                self.local_vel['fb'] = vel * direction
            elif dir == 'lr':
                self.local_vel['lr'] = vel * direction

        print self.cnt, self.local_vel
