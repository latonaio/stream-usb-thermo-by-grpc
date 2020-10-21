# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.


from concurrent import futures
import time
import cv2
import grpc
import base64
import numpy as np
import sys
from pathlib import Path
from aion.logger import lprint
from . import thermo_pb2
from . import thermo_pb2_grpc


WIDTH = 382
HEIGHT = 288

class TemperatureDecoder():

    def __init__(self, timg, temperatures, timestamp=None):
        self.img = timg
        self.temps = temperatures.reshape(HEIGHT, WIDTH, 1)[:,:,::-1]
        self.temps = self.temps / 10. - 100
        self.timestamp = timestamp

    def write_image(self):
        cv2.imwrite("/var/lib/aion/Data/themograpy_image.jpg", self.img)


class TemperatureClient():
    
    def __init__(self, host='127.0.0.1', port=50051):
        self.host = host
        self.port = port

    def get(self):
        address = f'{self.host}:{self.port}'
        print(f'access to server:{address}')
        with grpc.insecure_channel(address) as channel:
            stub = thermo_pb2_grpc.TemperatureServerStub(channel)
            try:
                res = stub.getTemperature(thermo_pb2.TemperatureRequest())
                t1 = time.time()
                for r in res:
                    t2 = time.time()
                    lprint(f'recieve time: {t2 - t1}')
                    t1 = t2
            except grpc.RpcError as e:
                lprint(e.details())
                return None
        return r

    def get_temperature(self):
        address = f'{self.host}:{self.port}'
        print(f'access to server:{address}')
        with grpc.insecure_channel(address) as channel:
            stub = thermo_pb2_grpc.TemperatureServerStub(channel)
            try:
                res = stub.getTemperature(thermo_pb2.TemperatureRequest())
                t1 = time.time()
                for r in res:
                    bimg_64d = base64.b64decode(r.image)
                    btemp_64d = base64.b64decode(r.temperatures)
                    timestamp = r.timestamp
                    
                    dimg_Buf = np.frombuffer(bimg_64d, dtype = np.uint8)
                    dst_img = cv2.imdecode(dimg_Buf, cv2.IMREAD_COLOR)
                    d_temperatures = np.frombuffer(btemp_64d, dtype = np.uint16)

                    t = TemperatureDecoder(dst_img, d_temperatures, timestamp)
                    print(t.img.shape, t.temps.shape, t.timestamp)
                    t2 = time.time()
                    print(f'recieve time: {t2 - t1}')
                    t1 = t2

            except grpc.RpcError as e:
                print(e.details())
                return None

        return  t

if __name__ == '__main__':

    with grpc.insecure_channel('127.0.0.1:50051') as channel:

        stub = thermo_pb2_grpc.TemperatureServerStub(channel)
            
        try:
            res = stub.getTemperature(thermo_pb2.TemperatureRequest())
            for r in res:
                bimg_64d = base64.b64decode(r.image)
                btemp_64d = base64.b64decode(r.temperatures)
                timestamp = r.timestamp
                
                dimg_Buf = np.frombuffer(bimg_64d, dtype = np.uint8)
                dst_img = cv2.imdecode(dimg_Buf, cv2.IMREAD_COLOR)
                d_temperatures = np.frombuffer(btemp_64d, dtype = np.uint16)

                print((dst_img.shape))
                print(d_temperatures.shape)
                print(timestamp)

        except grpc.RpcError as e:
            print(e.details())

        print("finish client")


