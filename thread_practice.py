from threading import Thread, Event
from time import sleep
from Uart61 import open_serial_connection_and_print_output
from compass import get_compass_value
from berryIMU import main
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
sleep(5)
while True:
    try:
        # print(compass, velocity, angle, accel)
        try:
          if init_compass == False:
            offset = round((angle[2][1]+180) - compass[0][1]) - compass[0][1]
            init_compass = True
          heading = compass[0][1] - ((angle[2][1]+180) - compass[0][1])
          print(round(heading), round(compass[0][1]), round(angle[2][1] - compass[0][1]), round((angle[2][1]+180) - compass[0][1]), round(angle[2][1] - compass[0][1]), round((-angle[2][1]+180) + compass[0][1]-offset))
          sleep(0.01)
        except:
          print('passed')
    except KeyboardInterrupt:
        event.set()
        break
t.join()
b.join()
print('done')