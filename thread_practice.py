from threading import Thread, Event
from time import sleep
from Uart61 import open_serial_connection_and_print_output
from compass import get_compass_value
from berryIMU import main
import sys
import redis
import json

def open_file_and_log_data(filename, log_data_event):
    with open(filename, 'w') as f:
        f.write(str(log_data_event) + '\n')

r = redis.Redis(host="localhost", port=6379, db=0)
r.pubsub(ignore_subscribe_messages=True)
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
# sleep(2)
while True:
    try:
        # print(compass, velocity, angle, accel)
        try:
          # if init_compass == False:
          #   offset = round((angle[2][1]+180) - compass[0][1]) - compass[0][1]
          #   init_compass = True
          # heading = compass[0][1] - ((angle[2][1]+180) - compass[0][1])
          # imu_heading = angle[2][1] - offset
          # negative = round(angle[2][1] + 360)
          # positive = round(angle[2][1])
          # print('heading', round(heading), 'compass', round(compass[0][1]), 'imu_heading', round(imu_heading), 'imu_compensated',  (negative if angle[2][1] < 0 else positive))
          # print(round(heading), round(compass[0][1]), round(angle[2][1] - compass[0][1]), round((angle[2][1]+180) - compass[0][1]), round(angle[2][1] - compass[0][1]), round((angle[2][1]+180) - compass[0][1]-offset))
          # print('difference', round((angle[2][1]+360 if angle[2][1] < 0 else angle[2][1]) - compass[0][1]-offset) - round(compass[0][1]))
          # print('#################################')
          print(angle, compass)
          # open_file_and_log_data('/home/pi/Desktop/data.txt', (compass, velocity, angle, accel))
          r.publish('my-channel', json.dumps({"heading": compass[0][1], "velocity": velocity[0][1], "accel": accel[0][1]}))
          sleep(0.001)
          if event.is_set():
            break
        except:
          print(sys.exc_info())
    except KeyboardInterrupt:
        event.set()
        t.join()
        b.join()
        break
t.join()
b.join()
print('done')