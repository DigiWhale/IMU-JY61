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
    # while True:
    #     data = []
    #     c = ser.read()
    #     if c == b'':
    #         break
    #     while c != b'U' and c != b'':
    #         data.append(c)
    #         c = ser.read()
    #     data = b''.join(data)
    #     for i in range(1, len(data), 1):
    #       sensor = binascii.hexlify(data[0:1]).decode('UTF-8')
    #       hex_value = b'0x' + binascii.hexlify(data[i:i+1])
    #       string = int(hex_value.decode('UTF-8'), 16)
    #       bit_string = "{:08b}".format(string)
    #       shifted = (string << 8)
    #       shifted_bit_string = "{:08b}".format(shifted)
    #       if sensor == "51":
    #         print('Accelerometer:', string, bit_string, shifted, shifted_bit_string)
    #       # elif sensor == "52":
    #       #   print('Gyroscope:', string)
    #       # elif sensor == "53":
    #       #   print('Magnetometer:', string)
    #     print('########################')
    while True:
        data = []
        c = ser.read()
        if c == b'':
            break
        while c != b'U' and c != b'':
            data.append(c)
            c = ser.read()
        data = b''.join(data)
        for i in range(2, len(data), 2):
          sensor = binascii.hexlify(data[0:1]).decode('UTF-8')
          low_byte = b'0x' + binascii.hexlify(data[i-1:i])
          high_byte = b'0x' + binascii.hexlify(data[i:i+1])
          low_string = int(low_byte.decode('UTF-8'), 16)
          high_string = int(high_byte.decode('UTF-8'), 16)
          low_bit_string = "{:08b}".format(low_string)
          high_bit_string = "{:08b}".format(high_string)
          high_shifted = (high_string << 8)
          high_shifted_bit_string = "{:08b}".format(high_shifted)
          low_shifted = low_bit_string.zfill(len(low_bit_string) + len(high_shifted_bit_string))
          low_shifted_bit_string = "{:08b}".format(low_shifted)
          if sensor == "51":
            print('Accelerometer:low', low_string, low_bit_string, low_shifted, low_shifted_bit_string)
            print('Accelerometer:high', high_string, high_bit_string, high_shifted, high_shifted_bit_string)
          # elif sensor == "52":
          #   print('Gyroscope:', string)
          # elif sensor == "53":
          #   print('Magnetometer:', string)
        print('########################')
    ser.close()
    print('done')
    
if __name__ == '__main__':
    open_serial_connection_and_print_output()