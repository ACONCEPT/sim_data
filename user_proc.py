#! usr/bin/env python3
import simpy
from simpy.events import AnyOf
import random as rd
from datetime import datetime, timedelta
import os
from config import\
            profile_proportions,\
            TRIGGERS,\
            USER_ACTIONS,\
            USERS,\
            STREAM_DATA_FILE,\
            STREAM_COLS,\
            FENCES,\
            NOTIFICATIONS

from helpers import\
        trigger_opportunity,\
        assign_profile_proportions,\
        profile_proportion,\
        ua_type,\
        trigger_fail_timeout,\
        trigger_success_timeout,\
        new_user_count,\
        view_opportunity,\
        conversion_opportunity,\
        view_success_timeout,\
        convert_success_timeout

class UserProcess(object):
    def __init__(self,env,userid):
        self.env = env
        self.profile = assign_profile_proportions(profile_proportions,1)[0]
        self.id = userid
#        self.action = env.process(self.user_process())
        self.my_triggers = []
        self.trigger_event = self.env.event()
        self.convert_event = self.env.event()
        self.view_event = self.env.event()

    def user_process(self):
        while True:
            yield self.env.process(self.life())

    def write(self):
        data = []
        for col in STREAM_COLS:
            data.append(str(getattr(self,col)))
        out = "{}\n".format(",".join(data))
#        print("writing row {} " .format(out))
        with open(STREAM_DATA_FILE,"a") as of:
            of.write(out)

    def convert_success(self):
        self.set_metadata()
        self.convertid = len(USER_ACTIONS) + 1
        USER_ACTIONS.append((self.triggerid,self.convertid,"convert",self.timestamp))
        self.type = "convert"
        self.convert_event.succeed()
        self.convert_event = self.env.event()
        self.write()

    def view_success(self):
        self.set_metadata()
        self.viewid = len(USER_ACTIONS) + 1
        USER_ACTIONS.append((self.triggerid,self.viewid,"view",self.timestamp))
        self.type = "view"
        self.view_event.succeed()
        self.view_event = self.env.event()
        self.write()

    def trigger_success(self):
        self.set_metadata()
        self.triggerid = len(TRIGGERS) + 1
        TRIGGERS.append((self.triggerid,self.type,self.timestamp))
        self.type = "trigger"
        self.trigger_event.succeed()
        self.trigger_event = self.env.event()
        self.write()

    def set_fence(self):
        self.fence_name = rd.choice(list(FENCES.keys()))

    def set_notification(self):
        self.notification_name = rd.choice(NOTIFICATIONS)

    def set_timestamp(self,wipe = False):
        if not wipe:
            self.timestamp = self.env.now
        else:
            self.timestamp = False

    def set_userid(self):
        self.userid = self.id

    def set_metadata(self):
        self.set_fence()
        self.set_notification()
        self.set_timestamp()
        self.set_userid()

    def life(self):
        while True:
            self.type = None
            self.set_timestamp(wipe = True)
            if self.env.now == 0:
                self.env.timeout(1)
            trigger = trigger_opportunity()
            if trigger:
#                print("trigger success timestamp {}, userid {} profile {}".format(self.env.now,self.id, self.profile))
                self.trigger_success()
                yield self.env.timeout(trigger_success_timeout())
                view = view_opportunity()
                if view:
#                    print("view success timestamp {}, userid {} profile {}".format(self.env.now,self.id, self.profile))
                    self.view_success()
                    yield self.env.timeout(view_success_timeout())
                    convert = conversion_opportunity()
                    if convert:
                        self.convert_success()
                        yield self.env.timeout(convert_success_timeout())
#                        print("convert success timestamp {}, userid {} profile {}".format(self.env.now,self.id, self.profile))
            else:
                yield self.env.timeout(trigger_fail_timeout())
