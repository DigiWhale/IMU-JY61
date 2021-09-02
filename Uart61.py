
import serial
import binascii
import time

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
        data = b''.join(data)
        for i in range(2, len(data), 2):
          # read 1st bit to identify sensor message
          sensor = binascii.hexlify(data[0:1]).decode('UTF-8')
          # convert low byte and high byte to hex
          low_byte = b'0x' + binascii.hexlify(data[i-1:i])
          high_byte = b'0x' + binascii.hexlify(data[i:i+1])
          # convert low byte and high byte from hex to b''
          low_string = int(low_byte.decode('UTF-8'), 16)
          high_string = int(high_byte.decode('UTF-8'), 16)
          # convert string to b'' 
          low_bit_string = "{:08b}".format(low_string)
          # shift high byte to left 8 spaces ex. 11010011 -> 1101001100000000
          high_shifted = (high_string << 8)
          #convert new 16 bit high byte to b''
          high_shifted_bit_string = "{:016b}".format(high_shifted)
          # add zeros to the front of the low byte b'' to match len of high byte b'' ex. 11010011 -> 0000000011010011
          low_shifted = low_bit_string.zfill(len(high_shifted_bit_string))
          # bitwise OR operation between high and low b'' ex 1101001100000000 | 0000000011010011 = 1101001111010011
          combined = (int(high_shifted_bit_string, 2)) | (int(low_shifted, 2))
          #collect the sign from the first bit
          sign = "{:016b}".format(combined)[:1]
          #collect the value from the last 15 bits -32768 to +32767
          signed = int("{:016b}".format(combined)[:], 2)
          if sensor == "51":
            print('accel')
            if sign == '1':
              # accel.append(-signed/32768*2*16)
              print(-signed/32768)
              print(low_byte, high_byte, low_string, high_string, high_shifted_bit_string, low_shifted, combined, signed)
            else:
              print(signed/32768*16)
              print(low_byte, high_byte, low_string, high_string, high_shifted_bit_string, low_shifted, combined, signed)
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