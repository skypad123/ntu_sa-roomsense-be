import pyaudio

import wave
from scipy.io.wavfile import read
import numpy as np

import mongoTypes as mt
import datetime
from getmac import get_mac_address as gma

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5

class AudioManager:

    def __init__(self, MongoDBInterfece: mt.MongoDBInterface, filepath):
        self.filepath = filepath
        self.MongoInterface = mt.MongoDBInterface 

    def record_audio(self):
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("* recording")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(self.filepath, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()


    def analyse_audio(self) -> dict:
        #reading program root file for output
        samprate, wavdata = read(self.filepath)

        # basically taking a reading every half a second - the size of the data 
        # divided by the sample rate gives us 1 second chunks 
        # sample rate in half for half second chunks
        chunks = np.array_split(wavdata, wavdata.size/(samprate/2))
        dbs = [20*np.log10(np.mean(chunk**2)) for chunk in chunks]
        data = dict()
        data["averageDecibel"] = np.mean(dbs)
        return data


    def _upload_file_mongodb(self)-> any:
        filepath = self.filepath
        return self.MongoInterface.insertAudioFile(filepath)

    def _upload_metadata_mongodb(self,AudioData: mt.AudioLog )->any:
        return self.MongoInterface.insertAudioLog("Audio", AudioData)
    
    def audio_process(self):
        self.record_audio()
        mongoTag = self._upload_file_mongodb()
        generatedData = self.analyse_audio()
        print(mongoTag)
        audioMeta = mt.AudioLog(datetime.datetime.now(),generatedData["averageDecibel"],mongoTag,str(gma()))
        self._upload_metadata_mongodb(audioMeta)


if __name__ == "__main__":
    mongoInterface = mt.MongoDBInterface("mongodb+srv://RoomSense-be:RoomSense-be@roomsenseserverless.p2y6b.mongodb.net/?retryWrites=true&w=majority", "RoomSense")
    audioManager = AudioManager(mongoInterface, "output.wav")
    currenttime = datetime.datetime.now()
    while(True):
        if datetime.datetime.now() - datetime.timedelta(minutes=1) > currenttime:
            audioManager.audio_process()
            currenttime = datetime.datetime.now() 
