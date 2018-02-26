#! usr/bin/env python3
import os
ONE_SECOND = 1
ONE_MINUTE = 60
ONE_HOUR = 60 * 60
ONE_DAY = 60 * 60 * 24
HALF_DAY = ONE_DAY/2
USER_ACTIONS = []
TRIGGERS = []
USERS = []
ALL_DAYS = 0
STREAM_DATA_FILE = "{}/repos/sims/useractions.csv".format(os.environ['HOME'])
STREAM_COLS = ["type","timestamp","fence_name","notification_name","userid","triggerid"]

number_of_users = int()
base_trigger_rate = float()
base_conversion_rate = float()
base_view_rate = float()
profile_proportions = []

#number_of_users = 200000
#base_trigger_rate = 1/18000
#base_conversion_rate = 20/100
#base_view_rate = 50/100
#
profile_proportions =[("sally",.25),\
                     ("jenny",.35),\
                     ("kim",.4)]

number_of_users = 2
base_trigger_rate = 1/18
base_conversion_rate = 20/100
base_view_rate = 50/100
