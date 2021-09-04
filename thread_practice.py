from threading import Thread, Event
from time import sleep
from Uart61 import open_serial_connection_and_print_output
from compass import get_compass_value
event = Event()

velocity = []
accel = []
angle = []
compass = []
t = Thread(target=open_serial_connection_and_print_output, args=(angle, velocity, accel, ))
b = Thread(target=get_compass_value, args=(compass, ))
t.start()
b.start()
while True:
    try:
        # print(compass, velocity, angle, accel)
        try:
          heading = angle[2]
          print(heading)
          sleep(0.01)
        except:
          print('passed')
    except KeyboardInterrupt:
        event.set()
        break
t.join()
b.join()
print('done')