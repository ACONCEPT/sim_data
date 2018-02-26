#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 23:43:39 2018

@author: joe
"""
import simpy
from datetime import datetime, timedelta


#run = number of seconds
#run = 365 * 24 * 60 * 60
run = 500 

start_time = datetime.utcnow()
increment = timedelta(seconds = 1)

class Car(object):
    def __init__(self, env):
        self.env = env
        # Start the run process everytime an instance is created.
        self.action = env.process(self.run())
#        self.current_time = start_time
#        print("starting at {} moving {} units forward".format(start_time,run))

    def run(self):
        while True:
            print('Start parking and charging at %d' % self.env.now)
            charge_duration = 5
            yield self.env.process(self.charge(charge_duration))
            print('Start driving at %d' % self.env.now)
            trip_duration = 2
            yield self.env.timeout(trip_duration)

    def charge(self, duration):
        yield self.env.timeout(duration)

env = simpy.Environment()
car = Car(env)
print("about to run env")
env.run(until=15)

