import shlex
from subprocess import Popen, PIPE, check_output
from enum import Enum
import hashlib

class Command(Enum):
  camera_commands = ({
    "left_shift": "uvcdynctrl -d {} -s \'Pan (Speed)\' -- -1; sleep 0.1;  uvcdynctrl -d {} -s \'Pan (Speed)\' -- 0",
    "right_shift": " uvcdynctrl -d {} -s \'Pan (Speed)\' -- 1; sleep 0.1;  uvcdynctrl -d {} -s \'Pan (Speed)\' -- 0",
    "up": "uvcdynctrl -d {} -s \'Tilt (Speed)\' -- 1; sleep 0.1;  uvcdynctrl -d {} -s \'Tilt (Speed)\' -- 0",
    "down": "uvcdynctrl -d {} -s \'Tilt (Speed)\' -- -1; sleep 0.1;  uvcdynctrl -d {} -s \'Tilt (Speed)\' -- 0",
    "zoom": "uvcdynctrl -s \"Zoom, Absolute\" {}"
  })


  def __init__(self, cmd):
    self.cmd = cmd


class DaemonStatus(object):
  def __init__(self, daemon):
    if daemon is not None:
      self.status = daemon.poll()
    else:
      self.status = "never ran"
    self.running = (self.status == None)


def hash_of(string):
  return hashlib.sha224(string.encode("utf-8")).hexdigest()


def listen_to_process(command, process, process_logger):
  stdout, stderr = process.communicate()
  for line in stdout.split(b'\n'):
    process_logger.info(line.decode("utf-8"))
  for line in stderr.split(b'\n'):
    process_logger.info(line.decode("utf-8"))
  process.wait()
  process_logger.info("{} terminated".format(command))

def run_in_background(command, stdin=None, stdout=None, stderr=None):
  # BEWARE: Using a stdout/stderr pipe obliges you to read from it!
  #         Unread pipes block after 64k of data and stop the subprocess from running.
  # See e.g. https://thraxil.org/users/anders/posts/2008/03/13/Subprocess-Hanging-PIPE-is-your-enemy/
  return Popen(shlex.split(command), bufsize=1, stdin=stdin, stdout=stdout, stderr=stderr)

def run_and_get_output(command):
  return check_output(shlex.split(command)).decode("utf-8")

def run_command(command):
  process =  Popen(shlex.split(command), bufsize=1, stdin=PIPE, stdout=PIPE, stderr=PIPE)
  listen_to_process(command, process, process_logger)
  return process.returncode
