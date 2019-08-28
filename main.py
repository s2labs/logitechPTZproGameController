import evdev
import scale
from subprocess import check_output, Popen
import configparser
import argparse
import shlex
from time import sleep

# When should the "analog" buttons react?
buttonSensitivityThreshold = 18000

def uvcSET(cam_name, command, value):
    check_output("uvcdynctrl -d {} -s \'{}\' -- {}".format(cam_name, command, value), shell=True)
    print("uvcdynctrl -d {} -s \'{}\' -- {}".format(cam_name, command, value))

def uvcGET(cam_name, command):
    print("uvcdynctrl -d {} -g \'{}\'".format(cam_name, command))
    res = check_output("uvcdynctrl -d {} -g \'{}\'".format(cam_name, command), shell=True).decode("utf-8")
    val = int(res.split(")")[0])
    return val

def executeInLoop(periodicity, command):

    while True:
        proc = Popen(shlex.split(command), bufsize=1, stdin=None, stdout=None, stderr=None, shell=True)
        sleep(periodicity)
        return proc

def stopExecuteInLoop(processID):

    processID.kill()

def gamepad_control(device, cam_name):

    # for storing where the camera is currently moving not to issue double
    movingDirection = [0, 0]

    for ev in device.read_loop():
        print(evdev.ecodes.EV_KEY)
        if ev.type == evdev.ecodes.EV_KEY:
        # TODO: also check if it is the keyDOWN event otherwise it fires on down and up!
            k = evdev.events.KeyEvent(ev)
            print(k.keystate)
            print(k.scancode)
            print(k.key_down)
            print(k.keycode)
            print(k.event)
            ### Movement (Pan/ Tilt)
            # 2=right
            if k.scancode == "305" and k.keystate == k.key_down:
                uvcSET("Pan (relative)", "-80")
            # 7=left
            if k.scancode == "307" and k.keystate == k.key_down:
                uvcSET("Pan (relative)", "80")
            # 1=UP
            elif k.scancode == "308" and k.keystate == k.key_down:
                uvcSET("Tilt (relative)", "80") 
            # 3=down
            elif k.scancode == "304" and k.keystate == k.key_down:
                uvcSET("Tilt (relative)", "-80")
            # Right Cross pressed:
            elif k.scancode == "318" and k.keystate == k.key_down:
                uvcSET("Tilt Reset", "1")
                uvcSET("Pan Reset", "1")
            ### Other functions
            # select: toggle other commands (zoom, exposure, ...) for usage withthe back buttons
            # start: select between auto and manual
            #
            # back right button = +1 for the selected property
            # back left button = -1 for the selected property
            #
            # left cross: up/ down = Zoom one step;
            # 17=up (-1)
            # elif k.scancode == "17" and k.event.value == "-1":
            #     uvcSET(cam_name, "Zoom, Absolute", uvcGET(cam_name, "Zoom, Absolute")+10)
            # # 17=down (1)
            # elif k.scancode == "17" and k.event.value.value == "1":
            #     uvcSET(cam_name, "Zoom, Absolute", uvcGET(cam_name, "Zoom, Absolute")-10)
            # # left cross: left/right = exposure one step
            else:
                ops = True
                continue
        else:
        # "analog" buttons
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
                # farg = 4 : right controller and up/down movement
                if farg in  [3, 4]:
                    should_move = abs(sarg) > buttonSensitivityThreshold 
                    is_increasing = (sarg>=0)
                    command2move = ["Pan (Speed)", "Tilt (Speed)"]

                    selectedOperation = 0
                    if should_move:
                        selectedOperation = 1 if is_increasing else -1
                    # invert for TILT
                    if (farg-3 ==1):
                        selectedOperation = -1*selectedOperation

                    if (movingDirection[farg-3] != abs(selectedOperation)):
                        movingDirection[farg-3] = abs(selectedOperation)
                        uvcSET(cam_name, command2move[farg-3], selectedOperation)
                # farg = 0: left controller and side movement
                # farg = 1: left controller and up/down movement
                elif farg == 1:
                    should_zoom = abs(sarg) > buttonSensitivityThreshold
                    if should_zoom:
                        zoom_level = scale.zoom_scale(sarg, uvcGET(cam_name, "Zoom, Absolute"))
                        uvcSET(cam_name, "Zoom, Absolute", zoom_level)
                        should_zoom = False
                elif farg == 17:
                    zoom_level = uvcGET(cam_name, "Zoom, Absolute")
                    if sarg == 1:
                        zoom_level = zoom_level - 30
                    if sarg == -1:
                        zoom_level = zoom_level + 30
                    if zoom_level > 1000:
                        zoom_level = 1000
                    if zoom_level < 100:
                        zoom_level = 100
                    uvcSET(cam_name, "Zoom, Absolute", zoom_level)
                else:
                    ops = True
                    continue


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--video")
    parser.add_argument("--gamepad")
    args = parser.parse_args()
    #print(args.video)
    #print(args.gamepad)
    config = configparser.ConfigParser()
    config.read('config.ini')
    if args.gamepad == None:
        device_name = config['DEVICE']['Name']
    else:
        device_name = str(args.gamepad)
    device = evdev.InputDevice(device_name)
    if args.video == None:
        cam_name = config['VIDEO']['Name']
    else:
        cam_name = str(args.video)
    print(cam_name)
    print(device_name)
    gamepad_control(device, cam_name)


