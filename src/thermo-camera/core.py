# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

import os
import time

from aion.kanban import Kanban
from aion.logger import initialize_logger, lprint
from aion.microservice import Options, main_decorator

from .infrared_camera import InfraredCamera
from .dummy_camera import DummyCamera
from .thermo_server import TemperatureServer

SERVICE_NAME = "stream-usb-thermo-by-grpc-server"
DEVICE_NAME = os.environ.get("DEVICE_NAME")
initialize_logger(SERVICE_NAME)

config_path = f'/var/lib/aion/Data/{SERVICE_NAME}_1/generic.xml'
log_path = f'/var/lib/aion/Data/{SERVICE_NAME}_1/log'


# @main_decorator(SERVICE_NAME)
#def main_without_kanban(opt: Options):
def main_without_kanban():
    lprint("start main_without_kanban()")
    # get cache kanban
    # conn = opt.get_conn()
    # num = opt.get_number()
    # kanban: Kanban = conn.set_kanban(SERVICE_NAME, num)

    ######### main function #############
    camera = InfraredCamera(config_path, log_path)
    server = TemperatureServer()
    server.start(camera)

@main_decorator(SERVICE_NAME)
def main_without_camera(opt:Options):
    lprint("start main_without_camera")

    camera = DummyCamera()
    server = TemperatureServer()
    server.start(camera)


if __name__ == '__main__':
    camera = InfraredCamera(config_path, log_path)

    server = TemperatureServer()

    server.start(camera)
