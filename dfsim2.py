#! usr/bin/env python3
import simpy
import random as rd

number_of_users = 100
#since sim is run on seconds, this rate averages to 1 in 5 hours
base_trigger_rate = 1/18000
base_conversion_rate = 20/100
base_view_rate = 50/100

profile_proportion =[("sally",.25),\
                     ("jenny",.35),\
                     ("kim",.4)]

def trigger_opportunity(trigger_boost=0):
    return rd.uniform(0,1) < base_trigger_rate + trigger_boost

def assign_profile_proportions(cp,length):
    cp = sorted(cp, key=lambda prob:prob[1])
    result = []
    while len(result) < length:
        for x in cp:
            result.append(profile_proportion(x))
    return result

def profile_proportion(proftuple):
    return _proportion(profuple[0],proftuple[1])

def _proportion(prob, val):
    p = rd.uniform(0,1)
    if p <= a:
       return b

class UserProcess(object):
    def __init__(self):
        self.profile = assign_profile_proportions(profile_proportion,1)[0]
        self.trigger = simpy.events.Event(env)

        self.action = env.process(self.trigger())

    def trigger(self):
        while True:
            yield env.process(self.life())
            yield env.timeout()

    def life(self):
        while self.Active:
            trigger = trigger_opportunity()
            if trigger:
                self.trigger.succeed()
                self.trigger = simpy.events.Event(env)

    def _deactivate(self):
        self.Active = False

    def _activate(self):
        self.Active = True


def add_users(qty):
    for i in range(qty):
        new_user()
        yield env.timeout(180)

def simulation_run(env,**kwargs):
    global user_actions
    global users
    user_actions = []
    users = []
    env.process(User_process(env,profile))


def generate_trigger_timeout():
    # to be about 6 hours worth of seconds
    return 6 * 60 * 60
