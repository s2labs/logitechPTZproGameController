import evdev
from camcontrol import execute
import scale
import configparser


def gamepad_control(device, cam_name):

    # isPaningRight = False
    # isPaningLeft = False
    # isTiltingUp = False
    # isTiltingDown = False
    movingDirection = [0, 0]

    for ev in device.read_loop():
        if ev.type == evdev.ecodes.EV_KEY:
            res = evdev.categorize(ev)
            res = str(res)
            res = res.split(",")[1].split("(")[0].strip()
            if res == "305":
                ops = execute("right", cam_name)
            elif res == "307":
                ops = execute("left", cam_name)
            elif res == "308":
                ops = execute("up", cam_name)
            elif res == "304":
                ops = execute("down", cam_name)
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
                #print("{}-{}".format(farg, sarg))
                # farg = 3 : right controller and side movement

                if farg in  [3, 4]:
                    should_move = (sarg < -10000) or (sarg > 10000)
                    is_increasing = (sarg>=0)
                    command2move = [["right", "left"], ["up", "down"]]
                    command2stop = ["pan_stop", "tilt_stop"]
                    print(movingDirection)
                    if is_increasing:
                        selectedOperation = 0
                    else:
                        selectedOperation = 1

                    if should_move:
                        if (movingDirection[farg-3] == 0):
                            ops = execute(command2move[farg-3][selectedOperation], cam_name)
                            movingDirection[farg-3] = 1
                    else:
                        if (movingDirection[farg - 3] == 1):
                            ops = execute(command2stop[farg - 3], cam_name)
                            movingDirection[farg - 3] = 0


                # if should_move:
                #     if is_increasing:
                #
                #
                # if float(sarg/32800) > 0.3:
                #     if farg == 3:
                #         if not isPaningRight:
                #             ops = execute("right", cam_name)
                #             isPaningRight = True
                #     elif farg == 4:
                #         if not isTiltingUp:
                #             ops = execute("up", cam_name)
                #             isTiltingUp = True
                # elif float(sarg/32800) < -0.3:
                #     if farg == 3:
                #         if not isPaningLeft:
                #             ops = execute("left", cam_name)
                #             isPaningLeft = True
                #     elif farg == 4:
                #         if not isTiltingDown:
                #             ops = execute("down", cam_name)
                #             isTiltingDown = True
                # else:
                #     if isPaningRight or isPaningLeft:
                #         ops = execute("pan_stop", cam_name)
                #         isPaningRight = False
                #         isPaningLeft = False
                #     if isTiltingUp or isTiltingDown:
                #         ops = execute("tilt_stop", cam_name)
                #         isTiltingDown = False
                #         isTiltingUp = False


if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read('config.ini')
    device_name = config['DEVICE']['Name']
    device = evdev.InputDevice(device_name)
    cam_name = config['VIDEO']['Name']
    gamepad_control(device, cam_name)

