import evdev
from time import sleep
import asyncio

dev = evdev.InputDevice('/dev/input/event3')

for ev in dev.async_read_loop():
    print(repr(ev))
