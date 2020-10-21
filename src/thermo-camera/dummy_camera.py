from datetime import datetime
import time
import cv2
import numpy as np
import os
from aion.logger import lprint

class DummyCamera():

    def __init__(self):
        index = 4
        path = '/var/lib/aion/Data/stream-usb-thermo-by-grpc-server_1/dummy'
        img_path = os.path.join(path, f'thermal_{index}.jpg')
        img = cv2.imread(img_path, 1)
        self.img = img
        lprint(str(self.img.shape))
        lprint(str(self.img.dtype))

        temp_path = os.path.join(path, f'thermal_{index}.csv')
        temps = np.loadtxt(temp_path, delimiter=',', dtype='uint16')

        self.temps = temps
        lprint(str(self.temps.shape))
        lprint(str(self.temps.dtype))
        self.timestamp = datetime.now().isoformat()


    def start_shooting(self, server):

        while True:
            server.update_temperature(self.temps, self.img, self.timestamp)
            time.sleep(5)





