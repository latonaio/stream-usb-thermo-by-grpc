# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

import os
import time

from aion.kanban import Kanban
from aion.logger import initialize_logger, lprint
from aion.microservice import Options, main_decorator
from .thermo_client import TemperatureClient

SERVICE_NAME = "stream-usb-thermo-by-grpc-client"
DEVICE_NAME = os.environ.get("DEVICE_NAME")
initialize_logger(SERVICE_NAME)
INTERVAL = 1.0

@main_decorator(SERVICE_NAME)
def main_without_kanban(opt: Options):
    lprint("start main_without_kanban()")
    # get cache kanban
    conn = opt.get_conn()
    num = opt.get_number()
    kanban: Kanban = conn.set_kanban(SERVICE_NAME, num)

    ######### main function #############
    client = TemperatureClient(host='stream-usb-thermo-by-grpc-server-001-srv', port=50051)
    while True:
        # temp = client.get_temperature()
        temp = client.get()

        # output after kanban
        if temp is not None:
            # image_list = temp.img.tolist()
            # temp_list = temp.temps.tolist()

            metadata = {
                "img": temp.image,
                "temp": temp.temperatures,
                "timestamp": temp.timestamp,
            }
            # NOTE: can not send decode image because size is too big
            #       reciever need to decode image 
            conn.output_kanban(
                result = True,
                connection_key="default",
                process_number=num,
                metadata=metadata,
            )

        time.sleep(INTERVAL)

@main_decorator(SERVICE_NAME)
def send_kanbans_at_highspeed(opt: Options):
    lprint("start send_kanbans_at_highspeed()")
    pass


@main_decorator(SERVICE_NAME)
def main_with_kanban_itr(opt: Options):
    lprint("start main_with_kanban_itr()")
    pass


@main_decorator(SERVICE_NAME)
def main_with_kanban(opt: Options):
    lprint("start main_with_kanban()")


if __name__ == '__main__':
    pass
