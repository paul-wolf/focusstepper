# -*- coding: utf-8 -*-
import os
import sys
import termios
import tty
import logging
import uuid
import time

from dotenv import load_dotenv

from adafruit_motor import stepper

from photo import capture_and_download
from stepper import move
from s3 import store_stream_s3
from files import upload_stack, stack_files, upload_image

load_dotenv()

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
PATH_DATA = os.environ.get("PATH_DATA", "./data")
DEFAULT_STACK_COUNT = os.environ.get("DEFAULT_STACK_COUNT", 30)
DEFAULT_STEP_SIZE = os.environ.get("DEFAULT_STEP_SIZE", 30)

stack = str(uuid.uuid4())
stack_pos = 0
stack_count = int(DEFAULT_STACK_COUNT)
step_size = int(DEFAULT_STEP_SIZE)
incremental_upload = False

def help():
    s = """
    use keys:

    i, j: forward by step size ({step_size})
    k, l: backward by size ({step_size})
    p: set parameters (step size) 
    e: edit stack id
    n: new session
    s: session info
    c: capture, move files to s3
    a: capture entire stack
    h, ?: help (this message)
    q: quit
    """.format(
        step_size=step_size
    )
    print(s)


def session_info():
    print("Base directory         : {}".format(BASE_DIR))
    print("Data path              : {}".format(PATH_DATA))
    print("Incremental upload     : {}".format(incremental_upload))
    print("Current stack id       : {}".format(stack))
    print("Current stack position : {}".format(stack_pos))
    print("Step size              : {}".format(step_size))
    print("Stack count            : {}".format(stack_count))
    print("Files: ")
    files = stack_files(stack)
    for f in files:
        print(f)
    else:
        print("<no files>")


def get_parameters():
    global step_size, stack_count

    v = input("Enter new step size value ({}): ".format(step_size))
    if v:
        step_size = int(v)
        print("New step size: {}".format(step_size))
    else:
        print("step size not changed")

    v = input("Enter new stack count value ({}): ".format(stack_count))
    if v:
        stack_count = int(v)
        print("New stack count: {}".format(stack_count))
    else:
        print("stack count not changed")


def set_stack():
    global stack
    v = input("Enter stack id ({}): ".format(stack))
    if v:
        stack = v
        print("New stack: {}".format(stack))
    else:
        print("stack id not changed")


def new_session():
    global stack, stack_pos, stack_count
    stack_pos = 0
    stack_count = 10
    stack = str(uuid.uuid4())
    print("New stack session: {}".format(stack))
    session_info()


def capture_image():
    global stack, stack_pos, stack_count, incremental_upload
    path = os.path.join(PATH_DATA, stack)
    if not os.path.exists(path):
        os.makedirs(path)
    p = capture_and_download(path, stack, stack_pos)
    if incremental_upload:
        upload_image(stack, p)
    print("Ready, stack_pos={}".format(stack_pos))


def capture_stack():
    global stack, stack_pos, stack_count, step_size
    while stack_pos < stack_count:
        capture_image()
        # if we do not wait, it causes the stepper to take short steps
        time.sleep(0.5) 
        move(
            step_size=step_size,
            direction=stepper.FORWARD,
            style=stepper.SINGLE)
        
        stack_pos += 1        
        print("Ready, stack_pos={}".format(stack_pos))
    print("Stack complete: {}, stack_pos={}".format(stack, stack_pos))

    
def toggle_incremental_upload():
    global incremental_upload
    incremental_upload = not incremental_upload
    print("Incremental upload: {}".format(incremental_upload))

    
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


help()

while True:
    char = getch()
    if char == "q":
        print("Done!")
        exit(0)

    if char == "j":
        move(
            step_size=step_size,
            direction=stepper.FORWARD,
            style=stepper.DOUBLE,
        )
        stack_pos -= 1
    elif char == "l":
        move(
            step_size=step_size,
            direction=stepper.BACKWARD,
            style=stepper.DOUBLE,
        )
        stack_pos += 1
    elif char == "i":
        move(
            step_size=step_size,
            direction=stepper.FORWARD,
            style=stepper.SINGLE,
        )
        stack_pos += 1
        
    elif char == "k":
        move(
            step_size=step_size,
            direction=stepper.BACKWARD,
            style=stepper.SINGLE,
        )
        stack_pos -= 1
        
    elif char in "?h":
        help()

    elif char == "p":
        get_parameters()

    elif char == "e":
        set_stack()

    elif char == "s":
        session_info()

    elif char == "n":
        new_session()

    elif char == "c":
        capture_image()

    elif char == "a":
        capture_stack()

    elif char == "u":
        toggle_incremental_upload()

    elif char == "0":
        stack_pos = 0
        print("Stack position: {}".format(0))

    elif char == "[":
        # move to start
        while stack_pos > 0:
            move(
                step_size=step_size,
                direction=stepper.BACKWARD,
                style=stepper.SINGLE,
            )
            stack_pos -= 1            
        print("Stack position: {}".format(stack_pos))
        
    elif char == "]":
        # move to end
        while stack_pos < stack_count:
            move(
                step_size=step_size,
                direction=stepper.FORWARD,
                style=stepper.SINGLE,
            )
            stack_pos += 1
        print("Stack position: {}".format(stack_pos))

    elif char == "0":
        stack_pos = 0
        print("Stack position: {}".format(stack_pos))

    else:
        #  print(hex(ord(char)))
        pass

print("Done!")
