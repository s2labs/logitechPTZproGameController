from subprocess import check_output
from commands import Command

def shift_right(cam_name):

    check_output(Command.camera_commands.cmd["right_shift"].format(cam_name, cam_name), shell=True)

def shift_left(cam_name):

    check_output(Command.camera_commands.cmd["left_shift"].format(cam_name, cam_name), shell=True)

def shift_up(cam_name):

    check_output(Command.camera_commands.cmd["up"].format(cam_name, cam_name), shell=True)

def shift_down(cam_name):

    check_output(Command.camera_commands.cmd["down"].format(cam_name, cam_name), shell=True)

def zoom(val):

    check_output(Command.camera_commands.cmd["zoom"].format(val), shell=True)

def execute(param, zoom_val, cam_name):

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
    elif param == 'zoom':
        zoom(zoom_val)
        return True
    else:
        return False




