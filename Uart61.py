
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

    while True:
        
        data = []
        c = ser.read()
        if c == b'':
            break
        while c != b'U' and c != b'':
            data.append(c)
            c = ser.read()
        data = b''.join(data)
        # header = binascii.hexlify(b'U')
        sensor = binascii.hexlify(data[0:1])
        reg_1 = data[1:3]
        reg_2 = data[3:5]
        reg_3 = data[5:7]
        reg_4 = data[7:9]
        checksum = data[9:10]

        if sensor == b'51':
          dec_reg_1 = int.from_bytes(reg_1, byteorder=sys.byteorder, signed=True)/32768*16
          dec_reg_2 = int.from_bytes(reg_2, byteorder=sys.byteorder, signed=True)/32768*16
          dec_reg_3 = int.from_bytes(reg_3, byteorder=sys.byteorder, signed=True)/32768*16
          dec_reg_4 = int.from_bytes(reg_4, byteorder=sys.byteorder, signed=True)/340+36.53
          dec_checksum = int.from_bytes(checksum, byteorder=sys.byteorder, signed=False)
          accel = {'sensor': 'accel', 'x': dec_reg_1, 'y': dec_reg_2, 'z': dec_reg_3}
          print(accel)
          # print('Acceleration', format(dec_reg_1, '.2f'), format(dec_reg_2, '.2f'), format(dec_reg_3, '.2f'), format(dec_reg_4, '.2f'))
        elif sensor == b'52':
          dec_reg_1 = int.from_bytes(reg_1, byteorder=sys.byteorder, signed=True)/32768*2000
          dec_reg_2 = int.from_bytes(reg_2, byteorder=sys.byteorder, signed=True)/32768*2000
          dec_reg_3 = int.from_bytes(reg_3, byteorder=sys.byteorder, signed=True)/32768*2000
          dec_reg_4 = int.from_bytes(reg_4, byteorder=sys.byteorder, signed=True)/340+36.53
          dec_checksum = int.from_bytes(checksum, byteorder=sys.byteorder, signed=False)
          velocity = {'sensor': 'velocity', 'x': dec_reg_1, 'y': dec_reg_2, 'z': dec_reg_3}
          print(velocity)
          # print('Velocity', format(dec_reg_1, '.2f'), format(dec_reg_2, '.2f'), format(dec_reg_3, '.2f'), format(dec_reg_4, '.2f'))
        elif sensor == b'53':
          dec_reg_1 = int.from_bytes(reg_1, byteorder=sys.byteorder, signed=True)/32768*180
          dec_reg_2 = int.from_bytes(reg_2, byteorder=sys.byteorder, signed=True)/32768*180
          dec_reg_3 = int.from_bytes(reg_3, byteorder=sys.byteorder, signed=True)/32768*180
          dec_reg_4 = int.from_bytes(reg_4, byteorder=sys.byteorder, signed=True)/340+36.53
          dec_checksum = int.from_bytes(checksum, byteorder=sys.byteorder, signed=False)
          angle = {'sensor': 'angle', 'x': dec_reg_1, 'y': dec_reg_2, 'z': dec_reg_3}
          print(angle)
          # print('Angle', format(dec_reg_1, '.2f'), format(dec_reg_2, '.2f'), format(dec_reg_3, '.2f'), format(dec_reg_4, '.2f'))
    ser.close()
    print('done')
    
if __name__ == '__main__':
    open_serial_connection_and_print_output()