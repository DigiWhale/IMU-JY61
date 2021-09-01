import serial

def open_serial_connection_and_print_output():
    """
    Opens a serial connection to the Arduino and prints the output.
    :return: None
    """
    # Open the serial connection
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=19200, bytesize=8, parity='N', stopbits=1, timeout=1)
    # Flush the input buffer
    ser.flushInput()
    # Read the output buffer
    reading = ser.readline()
    # Print the output buffer
    print(reading.decode())
    # Close the connection
    ser.close()
    print('done')
    
if __name__ == '__main__':
    open_serial_connection_and_print_output()