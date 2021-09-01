import serial
import codecs

def open_serial_connection_and_print_output():
    """
    Opens a serial connection to the Arduino and prints the output.
    :return: None
    """
    decode_hex = codecs.getdecoder("hex_codec")
    # Open the serial connection
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=19200, bytesize=8, parity='N', stopbits=1, timeout=10)
    # Flush the input buffer
    ser.flushInput()
    # Read the output buffer
    ser.flushInput()
    ser.flushOutput()
    reading = ser.read(10)
    # Print the output buffer
  
    bytes_object = bytes.fromhex(reading.decode("uint16"))


    ascii_string = bytes_object.decode("ASCII")
    print(ascii_string)
    # Close the connection
    ser.close()
    print('done')
    
if __name__ == '__main__':
    open_serial_connection_and_print_output()