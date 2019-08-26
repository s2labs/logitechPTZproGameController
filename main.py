import evdev
from camcontrol import execute
import scale
from subprocess import check_output
import configparser

def uvcSET(command, value):
    check_output("uvcdynctrl -d {} -s \'{}\' {}".format(cam_name, command, value), shell=True)
def uvcGET(command, param):
    check_output("uvcdynctrl -d {} -g \'{}\'".format(cam_name, command), shell=True)

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
                    should_move = abs(sarg) > 18000
                    is_increasing = (sarg>=0)
                    command2move = ["Pan (Speed)", "Tilt (Speed)"]
                    if is_increasing:
                        selectedOperation = 1
                    else:
                        selectedOperation = -1
                    if (farg-3 ==1):
                        selectedOperation = -1*selectedOperation
                    if not should_move:
                        selectedOperation = 0
                    value = str(selectedOperation)
                    if selectedOperation == -1:
                        value = "-- -1"
                    if (movingDirection[farg-3] != abs(selectedOperation)):
                        movingDirection[farg-3] = abs(selectedOperation)
                        print(movingDirection)
                        uvcSET(command2move[farg-3],value)
                        print("uvcdynctrl -d {} -s \'{}\' {}".format(cam_name,command2move[farg-3],value))

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

