__author__ = 'Lao'

import threading
import time


class PulseWidthModulator(object):

    Slice=0.004
    Max=100

    def __init__(self, turn_on_func, turn_off_func):
        self._turn_on=turn_on_func
        self._turn_off=turn_off_func
        self.power=0
        self._off_to_on_ratio=0.0
        self._last_state=False
        self._timer=None
        self._lock=threading.Lock()
        self._off_sum=0.0
        self._t_prev=time.time()

    def set_power(self, power):
        #check boundaries
        if power<0: power=0
        if power>self.Max: power=self.Max

        #nothing to do?
        if self.power==power:
            return

        #start/stop
        if self.power==0:
            self._start(power)
        elif power==0:
            self._stop()
        #change power
        else:
            self._set_new(power)

    def _set_new(self, power, starting=False):
        with self._lock:
            self.power=power
            #assuming self.power>0
            self._off_to_on_ratio=float(self.Max-self.power)/self.power
            #initialize so that off/on==ratio, on assumed to be always 1.0
            self._off_sum=self._off_to_on_ratio
            if starting:
                self._last_state=False
                self._t_prev=time.time()
                self._timer=1 #just something not None

    def _start(self, power):
        self._set_new(power, starting=True)
        self._go_on()

    def _stop(self):
        with self._lock:
            self._timer.cancel()
            self._timer=None
            self.power=0
            self._turn_off()

    def _go_on(self):
        with self._lock:
            #has been just killed?
            if not self._timer:
                return

            t=time.time()
            dt=t-self._t_prev
            self._t_prev=t
            #compute sums for ratio
            on_sum=1.0
            if self._last_state:
                on_sum+=dt
            else:
                self._off_sum+=dt
            #continue as on if off/on >= needed ratio
            if self._off_sum/on_sum>=self._off_to_on_ratio:
                self._last_state=True
                self._turn_on()
            #not just started and the off/on < needed ration
            else:
                self._last_state=False
                self._turn_off()
            #always normalize, so that on_sum=1.0
            self._off_sum/=on_sum
            #do not need to keep on_sum, since it is always 1.0 after the normalization above

            #restart timer
            self._timer=threading.Timer(self.Slice, self._go_on)
            self._timer.start()
