import serial

def open_serial_connection_and_print_output():
    """
    Opens a serial connection to the Arduino and prints the output.
    :return: None
    """
    # Open the serial connection
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=1)
    # Flush the input buffer
    ser.flushInput()
    # Read the output buffer
    reading = ser.read(1000)
    # Print the output buffer
    print(reading)
    # Close the connection
    ser.close()
    print('done')
    
if __name__ == '__main__':
    open_serial_connection_and_print_output()