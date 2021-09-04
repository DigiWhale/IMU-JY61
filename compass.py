import random
import time

def get_compass_value(compass):
    """
    Return the compass value of the current heading.
    """
    while True:
      compass[:] = {'heading': 0}.items()
      time.sleep(0.001)
      