#! usr/bin/env python3
import simpy
import random as rd



class test(object):
    def __init__(self,env):
        self.env = env
        self.action = self.env.process(self.main_proc())


    def sub_proc1(self):
        while True:
            yield self.event1
            msg = "sp1 :\np1 {}".format(getattr(self,"p",None))
            print(msg)
#            print("{}\n{}\n{}".format(msg1,msg2,msg3))

    def sub_proc2(self):
        while True:
            yield self.event2
            msg = "sp2 :\np2 {}".format(getattr(self,"p2",None))
            print(msg)

    def main_proc(self):
        self.env.process(self.sub_proc1())
        self.env.process(self.sub_proc2())
        self.event1 = self.env.event()
        self.event2 = self.env.event()
        for x in range(100):
            self.p = rd.randint(0,10)
            if self.p == 9:
                self.event1.succeed()
                self.event1 = self.env.event()
                yield self.env.timeout(1)
                self.p2 = rd.randint(0,5)
                if self.p2 == 4:
                    self.event2.succeed()
                    self.event2 = self.env.event()
                    yield self.env.timeout(1)

                
            yield self.env.timeout(1)


env = simpy.Environment()
test = test(env)
env.run()
