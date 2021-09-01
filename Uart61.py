import serial, struct
from serial.tools.list_ports import comports


SENSOR_PARAMS = {
    'baudrate': 1000_000,
    'stopbits': serial.STOPBITS_ONE,
    'parity': serial.PARITY_NONE,
    'bytesize': serial.EIGHTBITS,
}

def do_stuff_with_sensor_data(x, y, z):
    print(x, y, z)

with serial.Serial('/dev/ttyUSB0', **SENSOR_PARAMS) as opt_ser:
    # write sensor setup code
    header = (170, 0, 50, 3)
    speed = 1  # 1 = 1000 Hz, 10 = 100 Hz, ...
    filt = 0   # don't pre-filter data
    zero = 255
    checksum = sum(header) + speed + filt + zero
    payload = (*header, speed, filt, zero, *checksum.to_bytes(2, 'big', signed=False))
    opt_ser.write(bytes(payload))

    while True:
        expected_header = bytes(0x55)
        opt_ser.read_until(expected_header)
        print('found header')
        count, status, fx, fy, fz, checksum = (
            struct.unpack('>hhhhhH', opt_ser.read(12))
        )

        do_stuff_with_sensor_data(fx, fy, fz)
# import serial

# def open_serial_connection_and_print_output():
#     """
#     Opens a serial connection to the Arduino and prints the output.
#     :return: None
#     """
#     # Open the serial connection
#     ser = serial.Serial(port='/dev/ttyUSB0', baudrate=19200, bytesize=8, parity='N', stopbits=1, timeout=10)
#     # Flush the input buffer
#     ser.flushInput()
#     # Read the output buffer
#     while True:
#       ser.read_until(bytes(b'0x55'))
#       reading = ser.read(9)
#     # Print the output buffer

#       print(reading)
#     # Close the connection
#     ser.close()
#     print('done')
    
# if __name__ == '__main__':
#     open_serial_connection_and_print_output()