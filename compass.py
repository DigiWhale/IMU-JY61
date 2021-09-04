import random
import time

def get_compass_value(compass):
    """
    Return the compass value of the current heading.
    """
    while True:
      compass[:] = {'heading': 90}.items()
      time.sleep(0.01)
      