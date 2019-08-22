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

def zoom_in():

    check_output(Command.camera_commands.cmd["zoom_in"], shell=True)

def zoom_out():

    check_output(Command.camera_commands.cmd["zoom_out"], shell=True)

def execute(param):

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
    elif param == 'zoomin':
        zoom_in()
        return True
    elif param == 'zoomout':
        zoom_out()
        return True
    else:
        return False




