
import serial
import binascii
import time
from ast import literal_eval


def binaryToDecimal(binary):
    binary1 = binary
    decimal, i, n = 0, 0, 0
    while(binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1
    return decimal   

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
        accel = []
        data = []
        c = ser.read()
        if c == b'':
            break
        while c != b'U' and c != b'':
            data.append(c)
            c = ser.read()
        data = b'U' + b''.join(data)
        # print(data)
        header = literal_eval(binascii.hexlify(data[0:1]).decode('UTF-8'))
        sensor = literal_eval(binascii.hexlify(data[1:2]).decode('UTF-8'))
        reg_1 = literal_eval(binascii.hexlify(data[2:4]).decode('UTF-8'))
        reg_2 = literal_eval(binascii.hexlify(data[4:6]).decode('UTF-8'))
        reg_3 = literal_eval(binascii.hexlify(data[6:8]).decode('UTF-8'))
        reg_4 = literal_eval(binascii.hexlify(data[8:10]).decode('UTF-8'))
        checksum = literal_eval(binascii.hexlify(data[10:11]).decode('UTF-8'))
        dec_reg_1 = binaryToDecimal(int(reg_1, 16))
        dec_reg_2 = binaryToDecimal(int(reg_2, 16))
        dec_reg_3 = binaryToDecimal(int(reg_3, 16))
        dec_reg_4 = binaryToDecimal(int(reg_4, 16))
        print(header, sensor, reg_1, reg_2, reg_3, reg_4, checksum)
        print(header, sensor, dec_reg_1, dec_reg_2, dec_reg_3, dec_reg_4, checksum)
        for i in range(2, len(data), 2):
          pass
          # print(data[i:i+2])
          # x=binascii.hexlify(data[i:i+2])
          # y = binaryToDecimal(int(x.decode('UTF-8'), 16))/32768*16
          # print(x.decode('UTF-8'), y)
          # print(binascii.hexlify(data[i:i+2]))
          # # read 1st bit to identify sensor message
          # sensor = binascii.hexlify(data[0:1]).decode('UTF-8')
          # # convert low byte and high byte to hex
          # low_byte = b'0x' + binascii.hexlify(data[i-1:i])
          # high_byte = b'0x' + binascii.hexlify(data[i:i+1])
          # # convert low byte and high byte from hex to b''
          # low_string = int(low_byte.decode('UTF-8'), 16)
          # high_string = int(high_byte.decode('UTF-8'), 16)
          # # convert string to b'' 
          # low_bit_string = "{:08b}".format(low_string)
          # # shift high byte to left 8 spaces ex. 11010011 -> 1101001100000000
          # high_shifted = (high_string << 8)
          # #convert new 16 bit high byte to b''
          # high_shifted_bit_string = "{:016b}".format(high_shifted)
          # # add zeros to the front of the low byte b'' to match len of high byte b'' ex. 11010011 -> 0000000011010011
          # low_shifted = low_bit_string.zfill(len(high_shifted_bit_string))
          # # bitwise OR operation between high and low b'' ex 1101001100000000 | 0000000011010011 = 1101001111010011
          # combined = (int(high_shifted_bit_string, 2)) | (int(low_shifted, 2))
          # #collect the sign from the first bit
          # sign = "{:016b}".format(combined)[:1]
          # #collect the value from the last 15 bits -32768 to +32767
          # signed = int("{:016b}".format(combined)[:], 2)
          # if sensor == "51":
          #   print('accel')
          #   if sign == '1':
          #     # accel.append(-signed/32768*2*16)
          #     print(-((signed/(32768*2))*16))
          #     print(low_byte, high_byte, low_string, high_string, high_shifted_bit_string, low_shifted, combined, signed)
          #   else:
          #     print(signed/32768*16)
          #     print(low_byte, high_byte, low_string, high_string, high_shifted_bit_string, low_shifted, combined, signed)
          # elif sensor == "52":
          #   print('velocity')
          #   if sign == '1':
          #     print(-signed/32768*2000)
          #   else:
          #     print(signed/32768*2000)
          # elif sensor == "53":
          #   print('angle')
          #   if sign == '1':
          #     print(-signed/32768*180)
          #   else:
          #     print(signed/32768*180)
        print('########################')
        # time.sleep(0.1)
    ser.close()
    print('done')
    
if __name__ == '__main__':
    open_serial_connection_and_print_output()