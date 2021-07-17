from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
import hub as hb
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
import math

# For running multiple routines in parallel
from utime import sleep as wait_for_seconds
from utime import ticks_diff, ticks_ms

# To create and render images that make Charlie blink  
H = 9
_ = 0
blink = [
    [_,H,_,H,H],
    [_,H,_,H,H],
    [_,_,_,_,_],
    [_,H,_,H,H],
    [_,H,_,H,H],
]

blank = [
    [_,H,_,_,_],
    [_,H,_,_,_],
    [_,_,_,_,_],
    [_,H,_,_,_],
    [_,H,_,_,_],
]
# Convert an n x m matrix to a hub Image with semicolons
def matrix_to_image(matrix):
    return hb.Image(":".join(["".join([str(n) for n in r]) for r in matrix]))

blink_img = matrix_to_image(blink)
blank_img = matrix_to_image(blank)

"""
Motor connections:

Motor 1: Right wheel is connected to port E
Motor 2: Left wheel is connected to port A
Motor 3: Right arm is connected to port F
Motor 4: Left arm is connected to port B

"""

hub = MSHub()
main_timer = Timer()
background_image_timer = Timer()

arms = MotorPair('B','F')
arm_left = Motor('B')
arm_right = Motor('F')

arms.set_default_speed(100)
arm_left.set_default_speed(100)
arm_right.set_default_speed(100)

# Timer class for running multiple routines in parallel
class Timer():
    """Replacement Timer class that allows decimal points so we can measure times of less than one second."""
    def __init__(self):
        self.start_ticks = 0

    def now(self):
        """Returns the time in seconds since the timer was last reset."""
        return ticks_diff(ticks_ms(), self.start_ticks) / 1000

    def reset(self):
        """Resets the timer."""
        self.start_ticks = ticks_ms()

def background_image_delay(seconds):
    """Delays for ``seconds``."""
    background_image_timer.reset()
    while background_image_timer.now() < seconds:
        yield

def animate_image():
    """Shows different images in the background."""
    while True:
        hb.display.show(blink_img)
        yield from background_image_delay(0.001)
        hb.display.show(blank_img)
        yield from background_image_delay(0.001)

def main_thread_yield(t):
    """
    Parameters
    ----------
    t:
        Time (in seconds) for which the main thread will execute this action
    """
    main_timer.reset()
    while main_timer.now() < t:
        yield


# This routine runs Charlie's dance 
def main_thread():

    yield from main_thread_yield(2) 

# Start: This part corresponds to Charlie's Calibrate module
    arms.move_tank(100,'degrees',-100,-100)
    arms.move_tank(100,'degrees',40,40)
    yield from main_thread_yield(0.001)
# End: This part corresponds to Charlie's Calibrate module

    wa_one = MotorPair('A','F')
    wa_two = MotorPair('B','E')

# We use the Humming sound file that Robot Inventor 51515 comes with 
    hb.sound.play("/extra_files/Humming")
    for r in range(0,2,1):
        arm_right.run_to_position(230,'counterclockwise',70)
        arm_right.run_to_position(300,'clockwise',70)
        arm_left.run_to_position(70,'clockwise',70)
        arm_left.run_to_position(0,'counterclockwise',70)

    yield from main_thread_yield(0.001)
    hb.sound.play("/extra_files/Humming")
    for r in range(0,2,1):
        wa_one.move_tank(80,'degrees',100,-100)
        wa_one.move_tank(80,'degrees',-100,100)     
        wa_two.move_tank(-90,'degrees',100,-100)
        wa_two.move_tank(-90,'degrees',-100,100)

    wheel_motors = MotorPair('A','E')
    wheel_motors.move_tank(40,'cm',80,-80)
    wheel_motors.move_tank(40,'cm',-80,80)
    yield from main_thread_yield(0.001)

    arm_right.run_to_position(260,'counterclockwise',43)
    arm_right.run_for_seconds(1,100)
    hb.sound.play("/extra_files/Tadaa")
    wait_for_seconds(1)
    arm_right.run_to_position(300,'counterclockwise',100)
    yield from main_thread_yield(0.001)


main_generator = main_thread()
animation_generator = animate_image()

# Start the two parallel routines to make Charlie dance 
#    and to make Charlie blink 
while True:
    next(main_generator)
    next(animation_generator)

