#! usr/bin/env python3
import simpy
from simpy.events import AnyOf
import random as rd
from datetime import datetime, timedelta
import os
from config import number_of_users,\
            base_view_rate,\
            base_trigger_rate,\
            base_conversion_rate,\
            profile_proportions,\
            ONE_MINUTE,\
            ONE_HOUR,\
            ONE_DAY,\
            HALF_DAY,\
            TRIGGERS,\
            USER_ACTIONS,\
            USERS,\
            ALL_DAYS,\
            STREAM_DATA_FILE,\
            STREAM_COLS

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
        self.action = env.process(self.user_process())
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
        print("writing row {} " .format(out))
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
        self.fence_name = "anyfence"

    def set_notification(self):
        self.notification_name = "testnotification"

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
#        self.env.process(self.stream_process())
        print("".join(["=" for x in range(100)]))
        print("".join(["=" for x in range(100)]))
        while True:
            self.type = None
            self.set_timestamp(wipe = True)
            if self.env.now == 0:
                self.env.timeout(1)

            trigger = trigger_opportunity()
            if trigger:
                print("trigger success timestamp {}, userid {} profile {}".format(self.env.now,self.id, self.profile))
                self.trigger_success()
                yield self.env.timeout(trigger_success_timeout())
                view = view_opportunity()
                if view:
                    print("view success timestamp {}, userid {} profile {}".format(self.env.now,self.id, self.profile))
                    self.view_success()
                    yield self.env.timeout(view_success_timeout())
                    convert = conversion_opportunity()
                    if convert:
                        self.convert_success()
                        yield self.env.timeout(convert_success_timeout())
                        print("convert success timestamp {}, userid {} profile {}".format(self.env.now,self.id, self.profile))
            else:
                yield self.env.timeout(trigger_fail_timeout())
#            self.env.process(self.stream_process())






#    def trigger_(self):
#        self.env.process(self.view_())
#        yield self.trigger_event
#        # create trigger tuple
#        self.trigger = len(TRIGGERS) + 1
#        # append trigger tuple to this objects list of actions
#        yield self.env.timeout(trigger_success_timeout())
#
#        # append trigger tuple to global list of triggers 
#        TRIGGERS.append((self.trigger,self.env.now))
#
#        print("streaming trigger out timestamp {}, userid {} profile {}".format(self.env.now,self.id, self.profile))
##        stream_data_out(type = "trigger",\
##                        timestamp = self.env.now,\
##                        fence_name = "default",\
##                        notification_name = "default",\
##                        userid = self.id)
#        self.type = "trigger"
#        self.timestamp = self.env.now
#        self.fence_name = "default"
#        self.notification_name = "default"
#        self.userid = self.id
#        view = view_opportunity()
#        if view:
#            self.view_event.succeed()
#            self.view_event = self.env.event()

#    def view_(self):
#        self.env.process(self.convert_())
#        while True:
#            yield self.view_event
#            self.view = (self.trigger,"view",self.env.now)
#            USER_ACTIONS.append(self.view)
#
##            stream_data_out(type = "view",\
##                            timestamp = self.env.now,\
##                            fence_name = "default",\
#                            notification_name = "default",\
#                            userid = self.id)
#
#            convert = conversion_opportunity()
#            if convert:
#                self.convert_event.succeed()
#                self.convert_event = self.env.event()
#            yield self.env.timeout(view_success_timeout())

#    def convert_(self):
#        while True:
#            yield self.convert_event
#            self.convert = (self.trigger,"conversion",self.env.now)
#            USER_ACTIONS.append(self.convert)
##            stream_data_out(type = "conversion",\
##                            timestamp = self.env.now,\
##                            fence_name = "default",\
##                            notification_name = "default",\
##                            userid = self.id)
#            yield self.env.timeout(convert_success_timeout())

