import audio
import visual
import arduino
import multiprocessing as mp
from multiprocessing import Process
if __name__ == "__main__":
    mp.set_start_method('spawn')
    audioP = Process(target=audio.run_process)
    visualP = Process(target=visual.run_process)
    arduinoP = Process(target=arduino.run_process)
    audioP.start()
    visualP.start()
    arduinoP.start()
    audioP.join()
    visualP.join()
    arduinoP.join()
    