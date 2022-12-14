
import serial
import serial.tools.list_ports
import ujson
import re
import mongoTypes as mt
import datetime
from getmac import get_mac_address as gma

def print_ports():
    ports = serial.tools.list_ports.comports()
    ports = sorted(ports)
    for port, desc, hwid in ports:
            print("{}: {} [{}]".format(port, desc, hwid))
    return ports


if __name__ == "__main__":
    ports = print_ports()
    path, desc, hwid  = ports[-1]
    ser = serial.Serial(path, 115200, timeout=1)

    MongoInterface = mt.MongoDBInterface("mongodb+srv://RoomSense-be:RoomSense-be@roomsenseserverless.p2y6b.mongodb.net/?retryWrites=true&w=majority", "RoomSense")
    time = datetime.datetime.now()
    while True:
        # try:
    
        ser_bytes = ser.readline()
        decoded = str(ser_bytes.decode("utf-8"))
        if (len(list(re.finditer("{",decoded))) == 1 and time  < datetime.datetime.now()  - datetime.timedelta(minutes=1)):
            try:
                unjson = ujson.loads(decoded)
                
                SDC30_data = mt.SDC30Log(datetime.datetime.now(), unjson["C02"], unjson["Humidity"], unjson["Temperature"], str(gma()))
                print(SDC30_data.toDict())
                TSL2591_data = mt.TSL2591Log(datetime.datetime.now(), unjson["Light"], str(gma()))
                print(TSL2591_data.toDict())
                MongoInterface.insertSDC30Log("SDC30",SDC30_data)
                MongoInterface.insertTSL2591Log("TSL2591",TSL2591_data)
                
                time = datetime.datetime.now() 
            except:
                pass    

        # except:
        #     print("Keyboard Interrupt")
        #     break