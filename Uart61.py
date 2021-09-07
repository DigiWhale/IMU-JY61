
import serial
import binascii
import time

def open_serial_connection_and_print_output(angle_list, velocity_list, accel_list, print_data=False):
    """
    Opens a serial connection to the IMU
    """
    # Open the serial connection
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1)
    print('connected to IMU on /dev/ttyUSB0')
    time.sleep(1)
    ser.write(b'\r\n')
    # ser.reset_input_buffer()
    # ser.reset_output_buffer()
    # Flush the buffers
    # ser.flushInput()
    # ser.flushOutput()
    time.sleep(1)
    try:
      accel_ready = False
      velocity_ready = False
      angle_ready = False
      while True:
          time.sleep(0.001)
          # ser.reset_input_buffer()
          # ser.flushOutput()
          # initialize data buffer to store bytes
          data = []
          # start reading bytes
          # ser.flushOutput()
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
          # reg_4 = data_string[7:9]
          # checksum = data_string[9:10]
                    
          # if accel data is available, print it
          if sensor == b'51' and accel_ready == False:
            try:
              dec_reg_1 = round(int.from_bytes(reg_1, byteorder='little', signed=True)/32768*16, 2)
              dec_reg_2 = round(int.from_bytes(reg_2, byteorder='little', signed=True)/32768*16, 2)
              dec_reg_3 = round(int.from_bytes(reg_3, byteorder='little', signed=True)/32768*16, 2)
              # dec_reg_4 = round(int.from_bytes(reg_4, byteorder='little', signed=True)/340+36.53, 2)
              # dec_checksum = round(int.from_bytes(checksum, byteorder='little', signed=False), 2)
              accel = {'ax': dec_reg_1, 'ay': dec_reg_2, 'az': dec_reg_3}
              accel_ready = True
            except:
              pass

          elif sensor == b'52' and velocity_ready == False:
            try:
              dec_reg_1 = round(int.from_bytes(reg_1, byteorder='little', signed=True)/32768*2000, 2)
              dec_reg_2 = round(int.from_bytes(reg_2, byteorder='little', signed=True)/32768*2000, 2)
              dec_reg_3 = round(int.from_bytes(reg_3, byteorder='little', signed=True)/32768*2000, 2)
              # dec_reg_4 = round(int.from_bytes(reg_4, byteorder='little', signed=True)/340+36.53, 2)
              # dec_checksum = round(int.from_bytes(checksum, byteorder='little', signed=False), 2)
              velocity = {'vx': dec_reg_1, 'vy': dec_reg_2, 'vz': dec_reg_3}
              velocity_ready = True
            except:
              pass

          elif sensor == b'53' and angle_ready == False:
            try:
              dec_reg_1 = round(int.from_bytes(reg_1, byteorder='little', signed=True)/32768*180, 2)
              dec_reg_2 = round(int.from_bytes(reg_2, byteorder='little', signed=True)/32768*180, 2)
              dec_reg_3 = round(int.from_bytes(reg_3, byteorder='little', signed=True)/32768*180, 2)
              # dec_reg_4 = round(int.from_bytes(reg_4, byteorder='little', signed=True)/340+36.53, 2)
              # dec_checksum = round(int.from_bytes(checksum, byteorder='little', signed=False), 2)
              angle = {'wx': dec_reg_1, 'wy': dec_reg_2, 'wz': dec_reg_3}
              angle_ready = True
            except:
              pass
          
          if angle_ready and velocity_ready and accel_ready:
            angle_list[:] = angle.items()
            velocity_list[:] = velocity.items()
            accel_list[:] = accel.items()
            if print_data == True:
              print(angle['wz'])
              # for key, value in angle.items():
              #   print(key, ' : ', value)
              # for key, value in velocity.items():
              #   print(key, ' : ', value)
              # for key, value in accel.items():
              #   print(key, ' : ', value)
            angle_ready, velocity_ready, accel_ready = False, False, False
            

    finally:
      ser.close()
      print('Serial connection closed')
    
if __name__ == '__main__':
    angle_list = []
    velocity_list = []
    accel_list = []
    open_serial_connection_and_print_output(angle_list, velocity_list, accel_list, print_data=True)