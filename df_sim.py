#! usr/bin/env python3

"""
process description for simulation:

RUN 
========================================================================
launch process of time 
========================================================================
launch process of users
========================================================================
"""
import simpy
from datetime import datetime, timedelta
import random as rd

number_of_users = 100
#since sim is run on seconds, this rate averages to 1 in 5 hours
base_trigger_rate = 1/18000
base_conversion_rate = 20/100
base_view_rate = 50/100

fences = ["Ogleview","Ravenswood","Quincy","Roosevelt","Macys"]
notifications =["SPRING","BEAUTY","STYLE","PARTY","RED" ]
profiles = ["sally","jenny","kim"]



#def classify(ctups):
#    ctups = sorted(ctups, key=lambda prob:prob[1])
#    p = rd.uniform(0,1)
#
#    def return_label(item):
#        return item[0]
#
#    def return_prob(item):
#        return item[1]
#
#    result = False
#    last_prob = 0
#    for x in ctups:
#        prob = return_prob(x)
#        ev = p >= prob
#        if ev:
#            result = return_label(x)
#        last_prob = prob
#    return result

def create_interval(interval,qty = 1):
    if interval == "seconds":
        return timedelta(seconds = qty)
    elif interval == "hours":
        return timedelta(hours = qty)
    elif interval == "days":
        return timedelta(days = qty)

class User(object):
    def __init__(self,profile,tolerance = timedelta(hours = 5),trigger_boost = 0):
        self.tolerance = tolerance
        self.profile = profile
        self._available()
        self.trigger_boost = trigger_boost
        self.messages = []
        self.actions = []

    def _available(self):
        self.status = True
        self.msgs_active = 0

    def _unavailable(self):
        self.status = False

    def _trigger(self)
        p = rd.uniform(0,1)
        if p <= base_trigger_rate + self.trigger_boost:
            self.


    def evaluate(self,time):
        if self.available:


class Simulation(object):
    def __init__(self,\
                 env,\
                 usercount= 100,\
                 start_time= datetime.utcnow(),\
                 sim_interval="seconds",\
                 new_daily_users = .03):

        self.new_daily_users = new_daily_users
        self.env = env
        self.users = assign_proportion(profile_proportion,usercount)
        self.interval = create_interval(sim_interval)
        self.start_date = start_time
        self.action = env.process(self.run())

    def add_new_users(self):
        new_users = len(self.users) * self.new_daily_users
        if new_users < 0:
            new_users = 1
        elif new_users > 30:
             new_users = 30 + rd.randint(-20,20)
        new_users = assign_proportion(profile_proportion,new_users)
        self.users.append(new_users)
    def day(self,env)

    def increment_time(self):
        self.new_time = self.current_time + self.interval
        new_day = self.current_time.day != self.new_time.day
#        new_week = self.current_time.week == self.new_time.week
        new_month = self.current_time.month == self.new_time.month

        if new_day:
            self.add_new_users()
            print("day {} has {} users".format(self.new_time.strftime("%d/%m/%y"),len(self.users)))
        self.current_time = self.new_time

    def process_users(self):
        for user in self.users:
            yield self.env.process(self.user.evaluate())

    def run(self):
        print("in run")
        self.current_time = self.start_date
        while True:
            self.increment_time()
            yield self.env.timeout(1)
#            print(self.current_time)

if __name__ == '__main__':
    env = simpy.Environment()
    sim = Simulation(env)
    runtil = 3 * (60 * 60 * 24)
    print("running til {}".format(runtil))
    env.run(until=(runtil))

