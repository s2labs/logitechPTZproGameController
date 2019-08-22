import evdev
from camcontrol import execute
import scale

device = evdev.InputDevice('/dev/input/event3')


def gamepad_control():

    zoom_val = 100
    while True:
        for ev in device.read_loop():
            if ev.type == evdev.ecodes.EV_KEY:
                res = evdev.categorize(ev)
                res = str(res)
                res = res.split(",")[1].split("(")[0].strip()
                if res == "305":
                    ops = execute("right", zoom_val)
                elif res == "307":
                    ops = execute("left", zoom_val)
                elif res == "308":
                    ops = execute("up", zoom_val)
                elif res == "304":
                    ops = execute("down", zoom_val)
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
                                ops = execute("right", zoom_val)
                        else:
                            scval = abs(scval)
                            print(scval)
                            for i in range(0,scval):
                                ops = execute("left", zoom_val)
                    elif farg == 1:
                        scval = scale.xscale(sarg)
                        if scval > 0:
                            print(scval)
                            for i in range(0, scval):
                                ops = execute("down", zoom_val)
                        else:
                            scval = abs(scval)
                            print(scval)
                            for i in range(0, scval):
                                ops = execute("up", zoom_val)
                    elif farg == 5:
                        if zoom_val <= 300:
                            zoom_val += 10
                        ops = execute("zoom", zoom_val)
                    elif farg == 2:
                        if zoom_val >= 100:
                            zoom_val -= 10
                        ops = execute("zoom", zoom_val)
                    elif farg == 16:
                        if sarg == 1:
                            if zoom_val <= 300:
                                zoom_val += 10
                            ops = execute("zoom", zoom_val)
                        elif sarg == -1:
                            if zoom_val >= 100:
                                zoom_val -= 10
                            ops = execute("zoom", zoom_val)
                        else:
                            pass
                    else:
                        ops = True
                        continue



if __name__ == "__main__":

    gamepad_control()

