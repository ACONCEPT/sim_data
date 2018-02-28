#! usr/bin/env python3
import random as rd
from decimal import Decimal
from config import\
            number_of_users,\
            base_view_rate,\
            base_trigger_rate,\
            base_conversion_rate,\
            profile_proportions,\
            ONE_HOUR,\
            ONE_DAY,\
            ONE_MINUTE,\
            ALL_DAYS ,\
            USERS,\
            USER_ACTIONS,\
            STREAM_DATA_FILE,\
            STREAM_COLS


def initialize(filename, headers):
    out = "{}\n".format(",".join(headers))
    print("writing headers {} ".format(out))
    with open(filename,"w+") as of:
        of.write(out)


def _opportunity(q):
    p = rd.uniform(0,1)
    result = p < q
    return result

def trigger_opportunity(trigger_boost=0):
    return _opportunity(base_trigger_rate + trigger_boost)

def view_opportunity(view_boost=0):
    return _opportunity(base_view_rate + view_boost)

def conversion_opportunity(conversion_boost=0):
    return _opportunity(base_conversion_rate + conversion_boost)

def assign_profile_proportions(cp,length):
    cp = sorted(cp, key=lambda prob:prob[1])
    result = []
    while len(result) < length:
        for x in cp:
            nr = profile_proportion(x)
            if nr is not None:
                result.append(nr)
    return result

def profile_proportion(proftuple):
    result = _proportion(proftuple[0],proftuple[1])
    if result:
        return result

def _proportion(val,prob):
    p = rd.uniform(0,1)
    if p <= prob:
       return val

def create_interval(interval,qty = 1):
    if interval == "seconds":
        return timedelta(seconds = qty)
    elif interval == "hours":
        return timedelta(hours = qty)
    elif interval == "days":
        return timedelta(days = qty)

def ua_type():
    return "trigger"

def new_user_count():
    return rd.randint(0,10)

def trigger_fail_timeout():
    return rd.randint(0 , ONE_HOUR*2 + ONE_MINUTE*30)

def trigger_success_timeout():
    p = rd.randint(0,50)
    if p >= 45:
        p = rd.randint(ONE_HOUR,ONE_HOUR*3)
    return p

def view_success_timeout():
    return rd.randint(ONE_MINUTE/2,ONE_MINUTE*15) 

def convert_success_timeout():
    return rd.randint(ONE_HOUR,ONE_HOUR *6)


