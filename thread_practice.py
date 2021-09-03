from threading import Thread, Event
from time import sleep
from Uart61 import open_serial_connection_and_print_output
from compass import get_compass_value
event = Event()

def modify_variable(var):
    while True:
        for i in range(len(var)):
            var[i] += 1
        if event.is_set():
            break
        sleep(.001)
    print('Stop printing')
    
def modify_variable_2(var):
    while True:
        for i in range(len(var)):
            var[i] += 2
        if event.is_set():
            break
        sleep(1)
    print('Stop printing')

your_var = [0, 1, 2]
my_var = [1, 2, 3]
velocity = []
accel = []
angle = []
compass = []
t = Thread(target=open_serial_connection_and_print_output, args=(velocity, angle, accel, ))
b = Thread(target=get_compass_value, args=(compass, ))
t.start()
b.start()
while True:
    try:
        print(compass, velocity, angle, accel)
    except KeyboardInterrupt:
        event.set()
        break
t.join()
b.join()
print('done')