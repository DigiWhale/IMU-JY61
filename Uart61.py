import serial

def open_serial_connection_and_print_output():
    """
    Opens a serial connection to the Arduino and prints the output.
    :return: None
    """
    # Open the serial connection
    ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)
    # Flush the input buffer
    ser.flushInput()
    # Read the output buffer
    ser.readline()
    # Print the output buffer
    print(ser.readline())
    # Close the connection
    ser.close()