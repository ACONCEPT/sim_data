import simpy

class School(object):
    def __init__(self,env):
        self.env = env
        self.class_ends = env.event()
        self.pupil_procs = [env.process(self.pupil()) for i in range(3)]
        self.bell_proc = env.process(self.bell())

    def bell(self):
        for i in range(2):
            yield self.env.timeout(45)
            if self.env.now != 0:
                print("bell rang at {}!".format(self.env.now))
                self.env.timeout(2)
                self.class_ends.succeed()
                self.class_ends = self.env.event()

    def pupil(self):
        for i in range(2):
            print(' \{}/'.format(self.env.now), end = '')
            yield self.class_ends
            print(" yielded class_ends {}".format(self.env.now))


class Test(object):
    def __init__(self,env):
        self.env = env
        self.trigger_time = 5
        self.trigger_event = env.event()
        self.main_proc = env.process(self.main_())
        self.secondary_proc = env.process(self.print_p_())

    def main_(self):
        while True:
            yield self.env.timeout(1)
            if self.env.now == self.trigger_time:
                self.trigger_event.succeed()

    def print_p_(self):
        while True:
            yield self.trigger_event
            print("trigger succeded at {}".format(self.env.now))
            yield env.timeout(1)

env = simpy.Environment()
#school = School(env)
test = Test(env)

env.run(until = 6)
