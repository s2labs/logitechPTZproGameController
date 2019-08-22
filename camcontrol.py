from subprocess import check_output
from commands import Command

def shift_right():

    check_output(Command.camera_commands.cmd["right_shift"], shell=True)

def shift_left():

    check_output(Command.camera_commands.cmd["left_shift"], shell=True)

def shift_up():

    check_output(Command.camera_commands.cmd["up"], shell=True)

def shift_down():

    check_output(Command.camera_commands.cmd["down"], shell=True)

def zoom(val):

    check_output(Command.camera_commands.cmd["zoom"].format(val), shell=True)

def execute(param, zoom_val):

    if param == 'left':
        shift_left()
        return True
    elif param == 'right':
        shift_right()
        return True
    elif param == 'up':
        shift_up()
        return True
    elif param == 'down':
        shift_down()
        return True
    elif param == 'zoom':
        zoom(zoom_val)
        return True
    else:
        return False




