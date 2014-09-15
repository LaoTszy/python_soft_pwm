python_soft_pwm
===============

Software Pulse Width Modulation in Python

Yet another implementation of PWM in Python. I needed it for playing with Raspberry Pi, where you only have one hardware PWM pin. I have actually noticing that both hardware and software PWM by standard libraries available for Pi are quite imprecise (have to notice though that they do not use much processor time). 

This implementation is quite pricese, because it does not rely on the exactness of timers, it just adopts to whatever it gets. At a price of processor power of cause: on Pi it uses all the free processor time. 

The algorithm is quite simple: it tries to wake up every 4 msec (the default slice, you can change it by setting  `PulseWidthModulator.Slice` to some other value in seconds), keeping the records of how long the managed component was on and for how long it was off and depeneding on the current ration of these times it desides to switch it on or off for the next slice. Then it goes to sleep until the next timer event.

Here is the example usage with RPi.GPIO:

```
import RPi.GPIO as GPIO
from pwm import PulseWidthModulator
import time
...
GPIO.setup(8, GPIO.OUT)
pwm=PulseWidthModulator(lambda: GPIO.output(8, GPIO.HIGH), lambda: GPIO.output(8, GPIO.LOW))
pwm.set_power(25)
time.sleep(3)
pwm.power(75)
time.sleep(3)
pwm.set_power(0)
```
