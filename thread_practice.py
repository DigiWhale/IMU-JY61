from threading import Thread, Event
from time import sleep
from Uart61 import open_serial_connection_and_print_output
from compass import get_compass_value
from berryIMU import main
import sys
event = Event()

velocity = []
accel = []
angle = []
compass = []
t = Thread(target=open_serial_connection_and_print_output, args=(angle, velocity, accel, ))
b = Thread(target=main, args=(compass, ))
t.start()
b.start()
init_compass = False
print('Setting IMU heading offset...')
sleep(5)
while True:
    try:
        # print(compass, velocity, angle, accel)
        try:
          if init_compass == False:
            offset = round((angle[2][1]+180) - compass[0][1]) - compass[0][1]
            init_compass = True
          heading = compass[0][1] - ((angle[2][1]+180) - compass[0][1])
          imu_heading = angle[2][1] - offset
          print('heading', heading)
          print('compass', compass[0][1])
          print('imu_heading', imu_heading)
          # print(round(heading), round(compass[0][1]), round(angle[2][1] - compass[0][1]), round((angle[2][1]+180) - compass[0][1]), round(angle[2][1] - compass[0][1]), round((angle[2][1]+180) - compass[0][1]-offset))
          print('difference', round((angle[2][1]+180) - compass[0][1]-offset) - round(compass[0][1]))
          print('#################################')
          sleep(0.01)
          if event.is_set():
            break
        except:
          print(sys.exc_info())
    except KeyboardInterrupt:
        event.set()
        break
t.join()
b.join()
print('done')