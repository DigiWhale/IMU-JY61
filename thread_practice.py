from threading import Thread, Event
from time import sleep
from Uart61 import open_serial_connection_and_print_output

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
        sleep(.01)
    print('Stop printing')

your_var = [0, 1, 2]
my_var = [1, 2, 3]
t = Thread(target=open_serial_connection_and_print_output)
t.start()
b = Thread(target=modify_variable_2, args=(your_var, ))
b.start()
while True:
    try:
        # print(my_var, your_var)
        sleep(.01)
    except KeyboardInterrupt:
        event.set()
        break
t.join()
b.join()
print('done')