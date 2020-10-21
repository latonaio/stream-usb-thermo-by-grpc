import ctypes as ct
import datetime
import os
import sys
import time
from ctypes.util import find_library

import cv2
import numpy as np

try:
    __import__('aion.logger')
    from aion.logger import lprint
except ModuleNotFoundError:
    lprint = print

DISP_SW = os.environ.get('DISP_SW', '')
RETRY_MAX = 100
INTERVAL = 0.1

def draw_temp_image(img, themal):
    TEMP_THD = 32
    height = themal.shape[0]
    width = themal.shape[1]
    for h in range(0, height, int(height / 5)):
        for w in range(0, width, int(width / 6)):
            color =  (255, 255, 255) if themal[h][w] < TEMP_THD else (0, 0, 0)
            print(f'({h}, {w}: {themal[h][w]})')
            img = cv2.putText(img, str(themal[h][w]), (w, h), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, thickness=1)
    return img

# Define EvoIRFrameMetadata structure for additional frame infos
class EvoIRFrameMetadata(ct.Structure):
    _fields_ = [("counter", ct.c_uint),
                ("counterHW", ct.c_uint),
                ("timestamp", ct.c_longlong),
                ("timestampMedia", ct.c_longlong),
                ("flagState", ct.c_int),
                ("tempChip", ct.c_float),
                ("tempFlag", ct.c_float),
                ("tempBox", ct.c_float),
                ]


# load library
libir = ct.cdll.LoadLibrary(ct.util.find_library("irdirectsdk"))


class InfraredCamera():

    def __init__(self, config_path, logfilename='./log/logfilename'):

        pathConfig = ct.c_char_p(config_path.encode())
        # init vars
        pathFormat = ct.c_char_p()
        pathLog = ct.c_char_p(logfilename.encode())

        self.palette_width = ct.c_int()
        self.palette_height = ct.c_int()

        self.thermal_width = ct.c_int()
        self.thermal_height = ct.c_int()

        self.serial = ct.c_ulong()
        # init EvoIRFrameMetadata structure
        self.metadata = EvoIRFrameMetadata()

        # NOTE: wait untile last camera buffer is cleared
        lprint("now setting up the camera...")
        # time.sleep(SETUP_TIME)

        # init lib
        ret = libir.evo_irimager_usb_init(pathConfig, pathFormat, pathLog)
        if ret != 0:
            lprint("error at init")
            sys.exit(ret)

        ret = libir.evo_irimager_get_serial(ct.byref(self.serial))

        libir.evo_irimager_get_thermal_image_size(
            ct.byref(self.thermal_width), ct.byref(self.thermal_height))

        lprint(f'serial: {self.serial}')
        lprint(f'thermal width: {str(self.thermal_width.value)}')
        lprint(f'thermal height: {str(self.thermal_height.value)}')

        # init thermal data container
        self.np_thermal = np.zeros(
            [self.thermal_width.value * self.thermal_height.value], dtype=np.uint16)
        self.npThermalPointer = self.np_thermal.ctypes.data_as(
            ct.POINTER(ct.c_ushort))

        # get palette image size, width is different to thermal image width duo to stride alignment!!!
        libir.evo_irimager_get_palette_image_size(
            ct.byref(self.palette_width), ct.byref(self.palette_height))

        lprint('palette width: ' + str(self.palette_width.value))
        lprint('palette height: ' + str(self.palette_height.value))

        # init image container
        self.np_img = np.zeros(
            [self.palette_width.value * self.palette_height.value * 3], dtype=np.uint8)
        self.npImagePointer = self.np_img.ctypes.data_as(
            ct.POINTER(ct.c_ubyte))

        lprint('finish initialize')

    def start_shooting(self, server=None):
        lprint("start_shooting")
        retry = 0
        while True:
            ret = libir.evo_irimager_get_thermal_palette_image_metadata(
                self.thermal_width, self.thermal_height, self.npThermalPointer,
                self.palette_width, self.palette_height, self.npImagePointer, ct.byref(self.metadata))

            if ret != 0:
                retry += 1
                lprint(
                    f'error on evo_irimager_get_thermal_palette_image {ret}')
                if retry > RETRY_MAX:
                    lprint('retry exceed max')
                    break
                continue

            img = self.np_img.reshape(self.palette_height.value, self.palette_width.value, 3)[:,:,::-1]
            
            if server:
                server.update_temperature(
                    self.np_thermal, img, self.metadata.timestamp)

            # NOTE : TEMP is calculated BELOW
            temperature = self.np_thermal / 10. - 100
            
            if DISP_SW:
                image_temp = temperature.reshape(self.thermal_height.value, 
                                    self.thermal_width.value, 1)[:,:,::-1]
                img = draw_temp_image(img, image_temp)

                cv2.imshow('thermography', img)
                key = chr(cv2.waitKey(1) & 255)

            # NOTE: np_thermal type is uint16 
            # lprint(self.np_thermal.dtype)
            
            # NOTE: np_img type is uint8
            # lprint(self.np_img.dtype)
            
            time.sleep(INTERVAL)

        libir.evo_irimager_terminate()


if __name__ == '__main__':
    camera = InfraredCamera('../../config/generic.xml')

    camera.start_shooting()
