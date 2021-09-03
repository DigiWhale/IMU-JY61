
import serial
import binascii
import sys
from ast import literal_eval


def open_serial_connection_and_print_output():
    """
    Opens a serial connection to the IMU
    """
    # Open the serial connection
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=10)
    # Flush the buffers
    ser.flushInput()
    ser.flushOutput()

    while ser.available():
        # initialize data buffer to store bytes
        data = []
        # start reading bytes
        c = ser.read()
        # if no bytes are available, break out of loop
        if c == b'':
            break
        # while the incoming byte is not the delimiter, add it to the data buffer
        while c != b'U' and c != b'':
            data.append(c)
            c = ser.read()
        # join the data buffer into a string
        data_string = b''.join(data)
        # match data bytes to chipset format for Wit Motion WT61 IMU
        sensor = binascii.hexlify(data_string[0:1])
        reg_1 = data_string[1:3]
        reg_2 = data_string[3:5]
        reg_3 = data_string[5:7]
        reg_4 = data_string[7:9]
        checksum = data_string[9:10]
        # if accel data is available, print it
        if sensor == b'51':
          dec_reg_1 = round(int.from_bytes(reg_1, byteorder=sys.byteorder, signed=True)/32768*16, 2)
          dec_reg_2 = round(int.from_bytes(reg_2, byteorder=sys.byteorder, signed=True)/32768*16, 2)
          dec_reg_3 = round(int.from_bytes(reg_3, byteorder=sys.byteorder, signed=True)/32768*16, 2)
          dec_reg_4 = round(int.from_bytes(reg_4, byteorder=sys.byteorder, signed=True)/340+36.53, 2)
          dec_checksum = round(int.from_bytes(checksum, byteorder=sys.byteorder, signed=False), 2)
          accel = {'sensor': 'accel', 'x': dec_reg_1, 'y': dec_reg_2, 'z': dec_reg_3}
          for key, value in accel.items():
            print(key, ' : ', value)
        # if velocity data is available, print it
        elif sensor == b'52':
          dec_reg_1 = round(int.from_bytes(reg_1, byteorder=sys.byteorder, signed=True)/32768*2000, 2)
          dec_reg_2 = round(int.from_bytes(reg_2, byteorder=sys.byteorder, signed=True)/32768*2000, 2)
          dec_reg_3 = round(int.from_bytes(reg_3, byteorder=sys.byteorder, signed=True)/32768*2000, 2)
          dec_reg_4 = round(int.from_bytes(reg_4, byteorder=sys.byteorder, signed=True)/340+36.53, 2)
          dec_checksum = round(int.from_bytes(checksum, byteorder=sys.byteorder, signed=False), 2)
          velocity = {'sensor': 'velocity', 'x': dec_reg_1, 'y': dec_reg_2, 'z': dec_reg_3}
          for key, value in velocity.items():
            print(key, ' : ', value)
        # if angle data is available, print it
        elif sensor == b'53':
          dec_reg_1 = round(int.from_bytes(reg_1, byteorder=sys.byteorder, signed=True)/32768*180, 2)
          dec_reg_2 = round(int.from_bytes(reg_2, byteorder=sys.byteorder, signed=True)/32768*180, 2)
          dec_reg_3 = round(int.from_bytes(reg_3, byteorder=sys.byteorder, signed=True)/32768*180, 2)
          dec_reg_4 = round(int.from_bytes(reg_4, byteorder=sys.byteorder, signed=True)/340+36.53, 2)
          dec_checksum = round(int.from_bytes(checksum, byteorder=sys.byteorder, signed=False), 2)
          angle = {'sensor': 'angle', 'x': dec_reg_1, 'y': dec_reg_2, 'z': dec_reg_3}
          for key, value in angle.items():
            print(key, ' : ', value)
    ser.close()
    print('done')
    
if __name__ == '__main__':
    open_serial_connection_and_print_output()