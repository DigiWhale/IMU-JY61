# import serial, struct
# from serial.tools.list_ports import comports


# SENSOR_PARAMS = {
#     'baudrate': 1000_000,
#     'stopbits': serial.STOPBITS_ONE,
#     'parity': serial.PARITY_NONE,
#     'bytesize': serial.EIGHTBITS,
# }

# def do_stuff_with_sensor_data(count, status, fx, fy, fz, checksum):
#     print(count, status, fx, fy, fz, checksum)

# with serial.Serial('/dev/ttyUSB0', **SENSOR_PARAMS) as opt_ser:
#     # write sensor setup code
#     # header = (170, 0, 50, 3)
#     # speed = 10  # 1 = 1000 Hz, 10 = 100 Hz, ...
#     # filt = 0   # don't pre-filter data
#     # zero = 255
#     # checksum = sum(header) + speed + filt + zero
#     # payload = (*header, speed, filt, zero, *checksum.to_bytes(2, 'big', signed=False))
#     # opt_ser.write(bytes(payload))

#     while True:
#         expected_header = bytes(0x55)
#         opt_ser.read_until(expected_header)
#         print('found header')
#         count, status, fx, fy, fz, checksum = (
#             struct.unpack('>hhhhhH', opt_ser.read(10))
#         )

#         do_stuff_with_sensor_data(count, status, fx, fy, fz, checksum)
import serial
import binascii

def open_serial_connection_and_print_output():
    """
    Opens a serial connection to the Arduino and prints the output.
    :return: None
    """
    # Open the serial connection
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=10)
    # Flush the input buffer
    ser.flushInput()
    ser.flushOutput()
    # Read the output buffer
    while True:
        data = []
        c = ser.read()
        if c == b'':
            break
        while c != b'U' and c != b'':
            data.append(c)
            c = ser.read()
        data = b''.join(data)
        for i in range(1, len(data), 1):
          hex_value = binascii.hexlify(data[i:i+1])
          print('hex_value', b'0x' + hex_value)
          # string = int(hex_value, '16')
          # print(string)
        print('########################')
        # print('data', data.hex())
    # while True:
    #   # ser.read_until(binascii.hexlify(b'0x55'))
    #   reading = ser.read(1)
    #   # converted = reading.hex()
    # # Print the output buffer
    #   print(int(reading, 16))
    #   # print(int(converted, 16))
    # # Close the connection
    ser.close()
    print('done')
    
if __name__ == '__main__':
    open_serial_connection_and_print_output()