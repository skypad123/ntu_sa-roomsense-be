import time
import numpy as np
import cv2
import imutils

from picamera import PiCamera

import mongoTypes as mt
import datetime
from getmac import get_mac_address as gma

class VisualManager:

    def __init__(self, MongoDBInterfece: mt.MongoDBInterface, filepath):
        self.filepath = filepath
        self.MongoInterface = mt.MongoDBInterface 

    def capture_visual(self):
        camera = PiCamera()
        #time.sleep(1)

        camera.capture(self.filepath)

        print("Done")


    def analyse_visual(self):
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        # Reading the image
        image = cv2.imread(self.filepath)
        image = imutils.resize(image, width=min(800, image.shape[1]))
        orig = image.copy()

        # detect people in the image
        (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)

        # draw the original bounding boxes
        for (x, y, w, h) in rects:
            cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
            
            b=len(rects)
            # cv2.putText(orig,"peoplecount:"+str(b),(20,50),0,2,(255,0,0),3)
            
        # apply non-maxima suppression to the bounding boxes using a fairly large overlap threshold to try to maintain overlapping
        # boxes that are still people
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)



        # draw the final bounding boxes
        for (xA, yA, xB, yB) in pick:
            cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
            
        b=len(pick)


        data = dict()
        data["personCount"]=b
        return data
        # cv2.putText(image,"peoplecount:"+str(b),(20,50),0,2,(255,0,0),3)
        # print(b)

        # show the output images
        # cv2.imshow("Before NMS", orig)
        # cv2.imshow("After NMS", image)
        # cv2.waitKey(0)


    def _upload_file_mongodb(self)-> any:
        return self.MongoInterface.insertCameraFile(self.filepath)

    def _upload_metadata_mongodb(self,VisualData: mt.CameraLog )->any:
        return self.MongoInterface.insertCameraLog("Image", VisualData)

    def visual_process(self):
        self.capture_visual()
        mongoTag = self._upload_file_mongodb()
        generatedData = self.analyse_visual()
        print(mongoTag)
        visualMeta = mt.CameraLog(datetime.datetime.now(),generatedData["personCount"],mongoTag,str(gma()))
        self._upload_metadata_mongodb(visualMeta)


if __name__ == "__main__":
    mongoInterface = mt.MongoDBInterface("mongodb+srv://RoomSense-be:RoomSense-be@roomsenseserverless.p2y6b.mongodb.net/?retryWrites=true&w=majority", "RoomSense")
    visualManager = VisualManager(mongoInterface, "output.jpg")
    currenttime = datetime.datetime.now()
    while(True):
        if datetime.datetime.now() - datetime.timedelta(minutes=1) > currenttime:
            visualManager.visual_process()
            currenttime = datetime.datetime.now() 
