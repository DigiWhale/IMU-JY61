import random
import time

def get_compass_value(compass):
    """
    Return the compass value of the current heading.
    """
    num = 0
    while True:
      if num > 360:
        num == 0
      num += 1
      compass[:] = {'heading': 0}.items()
      time.sleep(1)
      