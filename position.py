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

stack = str(uuid.uuid4())
stack_pos = 0
stack_count = 10
button_delay = 0.2
step_increment = 100

def help():
    s = """
    use keys:

    i, j: forward by increment (100 by default)
    k, l: backward by increment (100 by default)
    p: set parameters (step increment) 
    e: edit stack id
    n: new stack id
    s: session info
    : info
    h, ?: help (this message)
    q: quit
    """
    print(s)

def session_info():
    print("Base directory         : {}".format(BASE_DIR))
    print("Data path              : {}".format(PATH_DATA))
    print("Current stack id       : {}".format(stack))
    print("Current stack position : {}".format(stack_pos))
    print("Files: ")
    files = stack_files(stack)
    for f in files:
        print(f)
    
def get_increment():
    global step_increment
    v = input("Enter new increment value ({}): ".format(step_increment))
    step_increment = int(v)

def set_stack():
    global stack
    v = input("Enter stack id ({}): ".format(stack))
    stack = int(v)
    
def new_session():
    global stack, stack_pos, stack_count
    stack_pos = 0
    stack_count = 10
    stack = str(uuid.uuid4())
    info()
    
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
    if (char == "q"):
        print("Done!")
        exit(0)
 
    if (char == "j"):
        move(step_increment=step_increment,
         direction=stepper.FORWARD,
             style=stepper.DOUBLE)

    elif (char == "l"):
        move(step_increment=step_increment,
         direction=stepper.BACKWARD,
             style=stepper.DOUBLE)

    elif (char == "i"):
        move(step_increment=step_increment,
         direction=stepper.FORWARD,
             style=stepper.SINGLE)
 
    elif (char == "k"):
        move(step_increment=step_increment,
         direction=stepper.BACKWARD,
             style=stepper.SINGLE)
 
    elif (char in "?h"):
        help()

    elif (char == "p"):
        get_increment()
        print("New increment: {}".format(step_increment))

    elif (char == "e"):
        set_stack()
        print("New stack: {}".format(stack))

    elif (char == "s"):
        session_info()

    elif (char == "n"):
        new_session()
        print("New stack session: {}".format(stack))

    elif (char == "c"):
        path = os.path.join(PATH_DATA, stack)
        if not os.path.exists(path):
            os.makedirs(path)
        p = capture_and_download(path, stack, stack_pos)
        stack_pos += 1
        upload_image(stack, p)
        print("Ready")
        

    else:
        # print(hex(ord(char)))
        pass

print("Done!")
