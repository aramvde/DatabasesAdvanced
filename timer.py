import time

class Timer:
    def __init__(self):
        pass
    
    def starttime(self):
        starttime = time.time()
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))