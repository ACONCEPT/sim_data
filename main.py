#! usr/bin/env python3
import simpy
import random as rd
from datetime import datetime, timedelta
import os
from config import ALL_DAYS,\
                USERS,\
                STREAM_DATA_FILE,\
                STREAM_COLS,\
                number_of_users,\
                ONE_DAY,\
                RUN_TIME,\
                RUNS

from helpers import\
            initialize,\
            new_user_count

from user_proc import UserProcess, USER_ACTIONS, TRIGGERS

def status_report():
    print("day:{}\nusers:{}\nactions:{}".format(str(ALL_DAYS),len(USERS),len(USER_ACTIONS)))

class RegularProcess(object):
    def __init__(self,env) :
        self.env = env
#        self.active = self.env.process(self.day_process())


    def day_process(self):
        new_users = new_user_count()
        print("new day {} new users".format(new_users))
        self.newusers = []
        for uid, x in enumerate(range(new_users)):
            uid = len(USERS) + uid
            new_user = UserProcess(env,uid)
            USERS.append(new_user)
            self.newusers.append(new_user)
 
        for i in range(24):
            yield self.env.process(self.hour_process())

    def hour_process(self):
        for i in range(60):
            yield self.env.process(self.minute_process())

    def minute_process(self):
        for i in range(60):
            yield self.env.process(self.second_process())

    def second_process(self):
        p = rd.randint(0,100)
        if p <= 20:
            n = rd.randint(0,200)
            if n <= len(self.newusers):
                for x in range(n):
                    user = self.newusers.pop()
                    self.env.process(user.user_process())
            else:
                for x in range(len(self.newusers)):
                    user = self.newusers.pop()
                    self.env.process(user.user_process())
        yield env.timeout(1)


def simulation_run(env,**kwargs,reinit = True):
    global timedata
    global ALL_DAYS
    global USERS
    global USER_ACTIONS
    USERS = []
    USER_ACITONS = []
    user_actions = []
    users = []

    if reinit:
        with open(STREAM_DATA_FILE,"w+") as of:
            of.write("")
        initialize(STREAM_DATA_FILE,STREAM_COLS)
    
        usercount = kwargs.get("starting_users",False)

    for uid, x in enumerate(range(usercount)):
        new_user = UserProcess(env,uid)
        USERS.append(new_user)
        env.process(new_user.user_process())
        if len(USERS) % 100000 == 0:
            print("{} users created".format(len(USERS)))

    status_report()
    while True:
        ALL_DAYS += 1
        yield env.process(RegularProcess(env).day_process())
        status_report()

if __name__ == '__main__':
    for i in range(RUNS):
        env = simpy.Environment()
        print("Environment Generated, number of users is {}".format(number_of_users))
        env.process(simulation_run(env,starting_users = number_of_users))
        print("process started")
        env.run(until = RUN_TIME)
        print("environment ran")
