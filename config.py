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
FENCES={"Macy's":(41.8836188,-87.6276187,50),"Quincy":(41.8801376,-87.636684,50),"Roosevelt":(41.8680657,-87.6289568,50),"Evanston":(42.0617337,-87.6948626,50),"35th":(41.8304217,-87.6293915,50)}
NOTIFICATIONS=["RED","BEAUTY","STYLE","PARTY","SPRING"]
RUN_TIME = ONE_DAY * 365
RUNS = 50

number_of_users = 100
base_trigger_rate = 1
base_conversion_rate = 6/10
base_view_rate = 3/4
profile_proportions =[("sally",.25),\
                     ("jenny",.35),\
                     ("kim",.4)]

