import random

def get_compass_value(compass):
    """
    Return the compass value of the current heading.
    """
    while True:
      compass[:] = random.randint(0, 360)