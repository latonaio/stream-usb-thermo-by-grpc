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

import thermo_pb2
import thermo_pb2_grpc


if __name__ == '__main__':

    with grpc.insecure_channel('127.0.0.1:50051') as channel:

        stub = thermo_pb2_grpc.TemperatureServerStub(channel)

        while True:
            
            try:
                res = stub.getTemperature(thermo_pb2.TemperatureRequest())
                for r in res:
                    bimg_64d = base64.b64decode(r.image)
                    btemp_64d = base64.b64decode(r.temperatures)
                    timestamp = r.timestamp
                    
                    dimg_Buf = np.frombuffer(bimg_64d, dtype = np.uint8)
                    dst_img = cv2.imdecode(dimg_Buf, cv2.IMREAD_COLOR)
                    d_temperatures = np.frombuffer(btemp_64d, dtype = np.uint16)

                    print((dst_img))
                    print(d_temperatures.dtype)

            except grpc.RpcError as e:
                print(e.details())
                break

        print("finish client")


