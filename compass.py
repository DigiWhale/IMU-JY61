import random
import time

def get_compass_value(compass):
    """
    Return the compass value of the current heading.
    """
    while True:
      compass[:] = {'heading': random.randint(0, 360)}
      time.sleep(0.001)
      