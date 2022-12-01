
import serial
import serial.tools.list_ports

def print_ports():
    ports = serial.tools.list_ports.comports()
    ports = sorted(ports)
    for port, desc, hwid in ports:
            print("{}: {} [{}]".format(port, desc, hwid))
    return ports

if __name__ == "__main__":
    ports = print_ports()
    path, desc, hwid  = ports[-1]
    ser = serial.Serial(path, 9600, timeout = 1)
    while True:
        try:
            ser_bytes = ser.readline()
            decoded_bytes = str(ser_bytes.decode("utf-8")) 
            print(decoded_bytes)
        except:
            print("Keyboard Interrupt")
            break