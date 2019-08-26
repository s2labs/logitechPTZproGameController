import evdev
from time import sleep
from commands import run_and_get_output
import asyncio

dev = evdev.InputDevice('/dev/input/event3')


for ev in dev.async_read_loop():
    res = repr(ev)
    res = str(res)
    print(res)
