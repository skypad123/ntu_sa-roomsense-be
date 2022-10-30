import datetime

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pymongo
import gridfs


class DHT11Log:

    #relies on DHT11 Sensor (Humidity Sensor)
    # data: {
    # datetime: <python datetime>
    # humidity: <float> (0-100)
    # temperature: <float> (in celsius)
    # device: <string> (mac address of rpi)
    # sensor: "DHT11"
    # }

    def __init__(self, datetime: datetime.datetime, humidity: float, temperature: float, device: str):
        self.datetime = datetime
        self.humidity = humidity
        self.temperature = temperature
        self.device = device
        self.sensor = "DHT11"
    
    def toDict(self):
        return {
            "datetime": self.datetime,
            "humidity": self.humidity,
            "temperature": self.temperature,
            "device": self.device,
            "sensor": self.sensor
        }

class TSL2591Log:

    #relies on TSL2591 Sensor (Light Sensor)
    # data: {
    # datetime: <python datetime>
    # lux: <float> (in lux)
    # device: <string> (mac address of rpi)
    # sensor: "TSL2591"
    # }

    def __init__(self, datetime: datetime.datetime, lux: float, device: str):
        self.datetime = datetime
        self.lux = lux
        self.device = device
        self.sensor = "TSL2591"
    
    def toDict(self):
        return {
            "datetime": self.datetime,
            "lux": self.lux,
            "device": self.device,
            "sensor": self.sensor
        }

class S8Log:
    #relies on S8 Sensor (Humidity Sensor)
    # data: {
    # datetime: <python datetime>
    # ppm: <float> (in ppm)
    # device: <string> (mac address of rpi)
    # sensor: "S8"
    # }

    def __init__(self, datetime: datetime.datetime, ppm: float, device: str):
        self.datetime = datetime
        self.ppm = ppm
        self.device = device
        self.sensor = "S8"
    
    def toDict(self):
        return {
            "datetime": self.datetime,
            "ppm": self.temperature,
            "device": self.device,
            "sensor": self.sensor
        }

class CameraLog:
    #relies on Camera Data
    # data: {
    # datetime: <python datetime>
    # personCount: <int> (estimate count of person by camera AI)
    # device: <string> (mac address of rpi)
    # sensor: "image"
    # objectId: <mongo ObjectId>
    # }
    def __init__(self, datetime: datetime.datetime, personCount: int, objectId: str, device: str):
        self.datetime = datetime
        self.personCount = personCount
        self.device = device
        self.objectId = objectId
        self.sensor = "camera"
    
    def toDict(self):
        return {
            "datetime": self.datetime,
            "personCount": self.personCount,
            "device": self.device,
            "objectId": self.objectId,
            "sensor": self.sensor
        }

class AudioLog:
    # relies on Mircophone Data
    # data: {
    # datetime: <python datetime>
    # averageDecibel: <float> (in decibel)
    # device: <string> (mac address of rpi)
    # sensor: "audio"
    # objectId: <mongo ObjectId>
    # }
    def __init__(self, datetime: datetime.datetime, averageDecibel: float, objectId: str, device: str):
        self.datetime = datetime
        self.averageDecibel = averageDecibel
        self.device = device
        self.objectId = objectId
        self.sensor = "audio"
    
    def toDict(self):
        return {
            "datetime": self.datetime,
            "averageDecible": self.averageDecibel,
            "device": self.device,
            "objectId": self.objectId,
            "sensor": self.sensor
        }




class MongoDBInterface:

    def __init__(self, connectionString:str, databaseName:str):
        self.client = pymongo.MongoClient(connectionString, server_api=ServerApi('1'))
        self.database = self.client[databaseName] 
        

    def insertDHT11Log(self,collectionName:str,data:DHT11Log):
        #relies on DHT11 Sensor (Humidity Sensor)
        # data: {
        # datetime: <python datetime>
        # humidity: <float> (0-100)
        # temperature: <float> (in celsius)
        # device: <string> (mac address of rpi)
        # sensor: "DHT11"
        # }
        collection = self.database[collectionName]
        # if (type(data) is list): 
        #     ret = collection.insert_many([x.toDict() for x in data])
        #     return (ret.inserted_ids)
        ret = collection.insert_one(data.toDict())
        return (ret.inserted_id)

    def insertTSL2591Log(self,collectionName:str,data:TSL2591Log):    
        #relies on TSL2591 Sensor (Light Sensor)
            # data: {
            # datetime: <python datetime>
            # lux: <float> (in lux)
            # device: <string> (mac address of rpi)
            # sensor: "TSL2591"
            # }
        collection = self.database[collectionName]
        ret = collection.insert_one(data.toDict())
        return (ret.inserted_id)

    def insertS8Log(self,collectionName:str,data:S8Log):    
        #relies on S8 Sensor (Humidity Sensor)
            # data: {
            # datetime: <python datetime>
            # ppm: <float> (in ppm)
            # device: <string> (mac address of rpi)
            # sensor: "S8"
            # }
        collection = self.database[collectionName]
        ret = collection.insert_one(data.toDict())
        return (ret.inserted_id)

    def insertCameraLog(self,collectionName:str,data:CameraLog):
            #relies on Camera Data
            # data: {
            # datetime: <python datetime>
            # personCount: <int> (estimate count of person by camera AI)
            # device: <string> (mac address of rpi)
            # sensor: "image"
            # objectId: <mongo ObjectId>
            # }
        collection = self.database[collectionName]
        ret = collection.insert_one(data.toDict())
        return (ret.inserted_id)

    def insertAudioLog(self,collectionName:str,data:AudioLog):
            #relies on Mircophone Data
            # data: {
            # datetime: <python datetime>
            # averageDecibel: <float> (in decibel)
            # device: <string> (mac address of rpi)
            # sensor: "audio"
            # objectId: <mongo ObjectId>
            # }
        collection = self.database[collectionName]
        ret = collection.insert_one(data.toDict())
        return (ret.inserted_id)

    def insertAudioFile(self,filepath:str):
        stringSplit = filepath.split("/")
        clientGridfs = self.client.grid_file
        fileItem = open(filepath,"rb")
        data = fileItem.read()
        fs = gridfs.GridFS(clientGridfs)
        ret = fs.put(data, filename = stringSplit[-1])
        return ret

    def insertCameraFile(self,filepath:str):
        stringSplit = filepath.split("/")
        clientGridfs = self.client.grid_file
        fileItem = open(filepath,"rb")
        data = fileItem.read()
        fs = gridfs.GridFS(clientGridfs)
        ret = fs.put(data, filename = stringSplit[-1])
        return ret


if __name__ == "__main__":
    # connectionString = "mongodb+srv://RoomSense-be:xNT7ddS0RT3ksGvr@roomsenseserverless.p2y6b.mongodb.net/?retryWrites=true&w=majority"
    # client = pymongo.MongoClient(connectionString, server_api=ServerApi('1'))
    # roomsenseDB = client["RoomSense"]
    MongoInterface = MongoDBInterface("mongodb+srv://RoomSense-be:RoomSense-be@roomsenseserverless.p2y6b.mongodb.net/?retryWrites=true&w=majority", "RoomSense")
    ret = MongoInterface.insertAudioFile("./Audio1.wav")
    print(ret)