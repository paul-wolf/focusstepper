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
DEFAULT_STEP_INCREMENT = os.environ.get("DEFAULT_STEP_INCREMENT", 30)

stack = str(uuid.uuid4())
stack_pos = 0
stack_count = DEFAULT_STACK_COUNT
step_increment = DEFAULT_STEP_INCREMENT


def help():
    s = """
    use keys:

    i, j: forward by step increment ({step_increment})
    k, l: backward by increment ({step_increment})
    p: set parameters (step increment) 
    e: edit stack id
    n: new session
    s: session info
    c: capture, move files to s3
    a: capture entire stack
    h, ?: help (this message)
    q: quit
    """.format(
        step_increment=step_increment
    )
    print(s)


def session_info():
    print("Base directory         : {}".format(BASE_DIR))
    print("Data path              : {}".format(PATH_DATA))
    print("Current stack id       : {}".format(stack))
    print("Current stack position : {}".format(stack_pos))
    print("Step increment         : {}".format(step_increment))
    print("Stack count            : {}".format(stack_count))
    print("Files: ")
    files = stack_files(stack)
    for f in files:
        print(f)
    else:
        print("<no files>")
        
def get_increment():
    global step_increment, stack_count
    
    v = input("Enter new increment value ({}): ".format(step_increment))
    if v:
        step_increment = int(v)
        print("New increment: {}".format(step_increment))        
    else:
        print("step increment not changed")


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
    global stack, stack_pos, stack_count
    path = os.path.join(PATH_DATA, stack)
    if not os.path.exists(path):
        os.makedirs(path)
    p = capture_and_download(path, stack, stack_pos)
    stack_pos += 1
    upload_image(stack, p)
    print("Ready")


def capture_stack():
    global stack, stack_pos, stack_count
    while stack_pos < stack_count:
        capture_image()
        move(step_increment=step_increment)
        time.sleep(0.5)
    print("Stack complete: {}".format(stack))


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
            step_increment=step_increment,
            direction=stepper.FORWARD,
            style=stepper.DOUBLE,
        )

    elif char == "l":
        move(
            step_increment=step_increment,
            direction=stepper.BACKWARD,
            style=stepper.DOUBLE,
        )

    elif char == "i":
        move(
            step_increment=step_increment,
            direction=stepper.FORWARD,
            style=stepper.SINGLE,
        )

    elif char == "k":
        move(
            step_increment=step_increment,
            direction=stepper.BACKWARD,
            style=stepper.SINGLE,
        )

    elif char in "?h":
        help()

    elif char == "p":
        get_increment()

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

    else:
        #  print(hex(ord(char)))
        pass

print("Done!")
