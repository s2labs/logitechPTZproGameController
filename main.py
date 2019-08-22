import evdev
from camcontrol import execute


device = evdev.InputDevice('/dev/input/event3')

while True:
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            res = evdev.categorize(event)
            res = str(res)
            res = res.split(",")[1].split("(")[0].strip()
            if res == "305":
                ops = execute("right")
            elif res == "307":
                ops = execute("left")
            elif res == "308":
                ops = execute("up")
            elif res == "304":
                ops = execute("down")
            else:
                ops = True
                continue



