# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

import os

from . import main_without_kanban, main_without_camera

KANBAN_MODE = os.environ.get("KANBAN_MODE", "main_without_kanban")
if __name__ == "__main__":
    if KANBAN_MODE == "main_without_camera":
        print(f"mode is {KANBAN_MODE}")
        main_without_camera()
    else:
        print(KANBAN_MODE)
        main_without_kanban()

