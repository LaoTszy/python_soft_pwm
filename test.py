__author__ = 'Lao'

import time
import unittest

from pwm import PulseWidthModulator

class Foo(object):
    def __init__(self):
        self._on_sum=0.0
        self._off_sum=0.0
        self._last_change=None
        self._state=False
        self.states=None

    def reset(self):
        self._last_change=time.time()
        self.states=[]

    def _sum(self):
        t=time.time()
        dt=t-self._last_change
        self._last_change=t
        if self._state:
            self._on_sum+=dt
        else:
            self._off_sum+=dt

    def on_fun(self):
        self.states.append(1)
        if not self._state:
            self._sum()
            self._state=True

    def off_fun(self):
        self.states.append(0)
        if self._state:
            self._sum()
            self._state=False

    def stop(self):
        self._sum()

class Test(unittest.TestCase):

    def test_ratio(self):
        foo=Foo()
        reg=PulseWidthModulator(foo.on_fun, foo.off_fun)
        foo.reset()

        reg.set_power(33)

        time.sleep(1)
        reg.set_power(0)
        foo.stop()

        self.assertAlmostEqual((reg.Max-33.0)/33.0, foo._off_sum/foo._on_sum, 1)

        reg.set_power(reg.Max-33)

        time.sleep(1)
        reg.set_power(0)
        foo.stop()

        self.assertAlmostEqual(1.0, foo._off_sum/foo._on_sum, 1)

if __name__ == '__main__':
    unittest.main()
