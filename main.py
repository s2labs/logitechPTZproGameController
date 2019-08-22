import evdev
from camcontrol import execute
import scale

device = evdev.InputDevice('/dev/input/event3')


def gamepad_control():

    while True:
        for ev in device.read_loop():
            if ev.type == evdev.ecodes.EV_KEY:
                res = evdev.categorize(ev)
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
            else:
                res = repr(ev)
                res = str(res)
                res = res.split("InputEvents")
                for r in res:
                    r = r.split("(")[1].split(")")[0]
                    r = r.split(",")
                    farg = int(r[3])
                    sarg = int(r[4])
                    print("{}-{}".format(farg, sarg))
                    # farg = 3 : right controller and side movement
                    if farg == 3:
                        scval = scale.xscale(sarg)
                        if scval > 0:
                            print(scval)
                            for i in range(0,scval):
                                ops = execute("right")
                        else:
                            scval = abs(scval)
                            print(scval)
                            for i in range(0,scval):
                                ops = execute("left")
                    if farg == 1:
                        scval = scale.xscale(sarg)
                        if scval > 0:
                            print(scval)
                            for i in range(0, scval):
                                ops = execute("down")
                        else:
                            scval = abs(scval)
                            print(scval)
                            for i in range(0, scval):
                                ops = execute("up")


if __name__ == "__main__":

    gamepad_control()

