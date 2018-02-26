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
                ONE_DAY

from helpers import\
            initialize,\
            status_report,\
            new_user_count

from user_proc import UserProcess

def day_process(env):
    global ALL_DAYS new_users = new_user_count()
    print("new day {} new users".format(new_users))
    ALL_DAYS += 1
    for uid, x in enumerate(range(new_users)):
        uid = len(USERS) + uid
#        new_user_proc(env, uid)

    for i in range(24):
        yield env.process(hour_process(env))
#        print("new hour")

def hour_process(env):
    for i in range(60):
        yield env.process(minute_process(env))

def minute_process(env):
    for i in range(60):
        yield env.process(second_process(env))


def second_process(env):
    yield env.timeout(1)


def new_user_proc(env,uid):
        new_user = UserProcess(env,uid)
        USERS.append(new_user)
        if len(USERS) % 100000 == 0:
            print("{} users created".format(len(USERS)))
        return env.process(new_user.user_process())


def simulation_run(env,**kwargs):
    global timedata
    global ALL_DAYS
    user_actions = []
    users = []

    with open(STREAM_DATA_FILE,"w+") as of:
        of.write("")
    initialize(STREAM_DATA_FILE,STREAM_COLS)

    usercount = kwargs.get("starting_users",False)
    print("about to create {} users".format(usercount))

    for uid, x in enumerate(range(usercount)):
        new_user = UserProcess(env,uid)
        USERS.append(new_user)
        env.process(new_user.user_process())
        if len(USERS) % 100000 == 0:
            print("{} users created".format(len(USERS)))

    status_report()
    while True:
        ALL_DAYS += 1
        yield env.process(day_process(env))
        status_report()

if __name__ == '__main__':
    env = simpy.Environment()
    print("Environment Generated, number of users is {}".format(number_of_users))
    env.process(simulation_run(env,starting_users = number_of_users))
    print("process started")
    env.run(until = (ONE_DAY * 5))
    print("environment ran")
