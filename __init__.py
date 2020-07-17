import time
import asyncio
import sys
from binaryninja import BackgroundTaskThread
from binaryninjaui import DockHandler

try:
    from pypresence import Presence
except ModuleNotFoundError as _error:
    if sys.platform in ["win32", "win64", "darwin"]:
        from pip._internal import main

        main(['install', '--quiet', 'pypresence==4.0.0'])


class DiscordRichPresence(BackgroundTaskThread):
    client_id = "733382890725048364"

    def __init__(self):
        BackgroundTaskThread.__init__(self, "Running Discord Rich Presence", True)
        self.rpc = Presence(client_id=DiscordRichPresence.client_id)
        self.active = True

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.rpc.connect()

        dock_handler = DockHandler.getActiveDockHandler()

        start = None
        while self.active:
            view_frame = dock_handler.getViewFrame()

            if view_frame:
                name = view_frame.getShortFileName()

                if not start:
                    start = int(time.time())

                self.rpc.update(large_image="bn-logo-round", large_text="Binary Ninja",
                                small_image="bn-logo-round", small_text="Binary Ninja",
                                start=start, details=f"{name}")

            else:
                start = None
                self.rpc.clear()

            time.sleep(5)

        self.rpc.close()

    def cancel(self):
        self.finish()

    def finish(self):
        self.active = False


task = DiscordRichPresence()
task.start()
