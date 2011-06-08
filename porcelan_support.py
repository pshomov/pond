import random
import string
import subprocess

def launch(cmd):
    return subprocess.Popen(cmd, shell=True)


def launch_and_wait(cmd):
    r = subprocess.call(cmd, shell=True)
    if r: exit(r)


def generate_temp_server_name():
    return 'temp'.join(random.choice(string.ascii_uppercase + string.digits) for x in range(5))