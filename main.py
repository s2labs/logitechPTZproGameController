import evdev
import scale
from subprocess import check_output
import configparser

# When should the "analog" buttons react?
buttonSensitivityThreshold = 18000

def uvcSET(command, value):
    check_output("uvcdynctrl -d {} -s \'{}\' {}".format(cam_name, command, value), shell=True)
    print("uvcdynctrl -d {} -s \'{}\' {}".format(cam_name, command, value))
def uvcGET(command, param):
    check_output("uvcdynctrl -d {} -g \'{}\'".format(cam_name, command), shell=True)
    print("uvcdynctrl -d {} -g \'{}\'".format(cam_name, command))

def gamepad_control(device, cam_name):

    # for storing where the camera is currently moving not to issue double
    movingDirection = [0, 0]

    for ev in device.read_loop():
        if ev.type == evdev.ecodes.EV_KEY:
            res = evdev.categorize(ev)
            res = str(res)
            res = res.split(",")[1].split("(")[0].strip()

            ### Movement (Pan/ Tilt)
            # C=right
            if res == "305":
                uvcSET("Pan (Absolute)", "1")
            # A=left
            elif res == "307":
                uvcSET("Pan (Absolute)", "-- -1")
            # B=UP
            elif res == "308":
                uvcSET("Tilt (Absolute)", "1") 
            # D=down
            elif res == "304":
                uvcSET("Tilt (Absolute)", "-- -1")

            ### Other functions
            # select: toggle other commands (zoom, exposure, ...) for usage withthe back buttons
            # start: select between auto and manual

            # back right button = +1 for the selected property
            # back left button = -1 for the selected property

            # left cross: up/ down = Zoom one step;
            # left cross: left/right = exposure one step
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
                    # sanetize -1 for uvcdynctrl:
                    value = "-- -1" if selectedOperation < 0 else str(selectedOperation)

                    if (movingDirection[farg-3] != abs(selectedOperation)):
                        movingDirection[farg-3] = abs(selectedOperation)
                        uvcSET(command2move[farg-3],value)

                # farg= 1 = ZOOM; 0 = exposure
                # farg = 3 = value selected above - 5= value selected above +
                # for these buttons set the value to the maximum in the direction the user wants to go.
                # if the release event / stop comes: GET the current value (if this gives the actual value and not the target) and SET this value +/- 11

if __name__ == "__main__":

# Change this to work with the command line without config file
# add a --help -h !
    config = configparser.ConfigParser()
    config.read('config.ini')
    device_name = config['DEVICE']['Name']
    device = evdev.InputDevice(device_name)
    cam_name = config['VIDEO']['Name']
    gamepad_control(device, cam_name)

