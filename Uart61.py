import serial

def open_serial_connection_and_print_output():
    """
    Opens a serial connection to the Arduino and prints the output.
    :return: None
    """
    # Open the serial connection
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=19200, bytesize=8, parity='N', stopbits=1, timeout=10)
    # Flush the input buffer
    ser.flushInput()
    # Read the output buffer
    while True:
      ser.read_until(bytes(b'\n'), timeout=10)
      reading = ser.read(1)
    # Print the output buffer

      print(reading)
    # Close the connection
    ser.close()
    print('done')
    
if __name__ == '__main__':
    open_serial_connection_and_print_output()