from subprocess import check_output
from commands import Command
import time
import subprocess


def shift_right(cam_name):

    check_output(Command.camera_commands.cmd["right_shift"].format(cam_name, cam_name), shell=True)

def shift_left(cam_name):

    check_output(Command.camera_commands.cmd["left_shift"].format(cam_name, cam_name), shell=True)

def shift_up(cam_name):

    check_output(Command.camera_commands.cmd["up"].format(cam_name, cam_name), shell=True)

def shift_down(cam_name):

    check_output(Command.camera_commands.cmd["down"].format(cam_name, cam_name), shell=True)

def pan_reset(cam_name):

    check_output(Command.camera_commands.cmd["pan_reset"].format(cam_name), shell=True)

def tilt_reset(cam_name):

    check_output(Command.camera_commands.cmd["tilt_reset"].format(cam_name), shell=True)

def pan_stop(cam_name):

    check_output(Command.camera_commands.cmd["pan_stop"].format(cam_name), shell=True)

def tilt_stop(cam_name):

    check_output(Command.camera_commands.cmd["tilt_stop"].format(cam_name), shell=True)

def pan_max_right(cam_name):

    check_output(Command.camera_commands.cmd["pan_max_right"].format(cam_name), shell=True)

def pan_max_left(cam_name):

    check_output(Command.camera_commands.cmd["pan_max_left"].format(cam_name), shell=True)

def tilt_max_up(cam_name):

    check_output(Command.camera_commands.cmd["tilt_max_up"].format(cam_name), shell=True)

def tilt_max_down(cam_name):

    check_output(Command.camera_commands.cmd["tilt_max_down"].format(cam_name), shell=True)

def zoom(val):

    check_output(Command.camera_commands.cmd["zoom"].format(val), shell=True)

def execute(param, cam_name):

    print("{}:{}\n".format(time.time(),param))

    if param == 'left':
        shift_left(cam_name)
        return True
    elif param == 'right':
        shift_right(cam_name)
        return True
    elif param == 'up':
        shift_up(cam_name)
        return True
    elif param == 'down':
        shift_down(cam_name)
        return True
    elif param == 'pan_reset':
        pan_reset(cam_name)
        return True
    elif param == 'tile_reset':
        tilt_reset(cam_name)
        return True
    elif param == 'pan_stop':
        pan_stop(cam_name)
        return True
    elif param == 'tile_stop':
        tilt_stop(cam_name)
        return True
    elif param == 'pan_max_right':
        pan_max_right(cam_name)
        return True
    elif param == 'pan_max_left':
        pan_max_left(cam_name)
        return True
    elif param == 'tilt_max_up':
        tilt_max_up(cam_name)
        return True
    elif param == 'tilt_max_down':
        tilt_max_down(cam_name)
        return True
    elif param == 'zoom':
        #zoom(zoom_val)
        return True
    else:
        return False




