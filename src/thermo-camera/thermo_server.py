import base64
import sys
import time
from concurrent import futures
from pathlib import Path

import cv2
import grpc
import numpy as np

from aion.logger import lprint
from .thermo_pb2 import TemperatureReply, TemperatureRequest
from .thermo_pb2_grpc import (TemperatureServerServicer,
                              add_TemperatureServerServicer_to_server)

try:
    __import__('aion.logger')
    from aion.logger import lprint, lprint_exception
except ModuleNotFoundError:
    lprint = print


class TemperatureServer(TemperatureServerServicer):

    def __init__(self):
        self.timestamp = None
        self.image = None
        self.temperatures = []

    def getTemperature(self, request, context):
        if self.image is None or self.temperatures is None:
            lprint("set no image")
            return

        old_timestamp = None
        while True:
            if old_timestamp != self.timestamp:
                yield TemperatureReply(
                    image=self.image,
                    temperatures=self.temperatures,
                    timestamp=self.timestamp)
                old_timestamp = self.timestamp
                lprint(f"send temperature data: {self.timestamp}")
                break
            time.sleep(0.01)
        return

    def update_temperature(self, temperatures, image, timestamp):
        try:
            ret, enimg = cv2.imencode('.jpg', image)
            self.image = base64.b64encode(enimg)
            self.temperatures = base64.b64encode(temperatures)
            self.timestamp = str(timestamp)
        except Exception as e:
            lprint("fail to encode data")


    def start(self, camera, ip=None, port=50051):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
        add_TemperatureServerServicer_to_server(self, server)

        if ip:
            server.add_insecure_port(f'{ip}:{port}')
            lprint(f"========== server start: {ip}:{port} ==============")
        else:
            server.add_insecure_port('[::]:50051')
            lprint(f"========== server start: localhost:{port} ==============")

        server.start()
        camera.start_shooting(self)
        server.wait_for_termination()
        server.stop()


if __name__ == "__main__":

    import infrared_camera

    camera = infrared_camera.InfraredCamera('../../config/generic.xml')
    server = TemperatureServer()
    server.start(camera)

