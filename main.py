import audio
import visual
import arduino
import multiprocessing as mp
from multiprocessing import Process
from time import sleep
import urllib

#for internet checking
def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False

if __name__ == "__main__":
    mp.set_start_method('spawn')
    
    while (not connect()):
        print("not connected, waiting 1000 ms for connection.")
        sleep(1000)
    
    audioP = Process(target=audio.run_process)
    visualP = Process(target=visual.run_process)
    arduinoP = Process(target=arduino.run_process)
    audioP.start()
    visualP.start()
    arduinoP.start()
    audioP.join()
    visualP.join()
    arduinoP.join()
    