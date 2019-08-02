# -*- coding: utf-8 -*-
import os
import sys
import logging
import uuid
import time

from dotenv import load_dotenv

from photo import capture_and_download
from stepper import move
from s3 import store_stream_s3
from files import upload_stack

load_dotenv()

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

stack = uuid.uuid4()
stack_size = 20
stack_pos = 0

print(stack)
path = "./data/{stack}".format(stack=stack)
print(path)
if not os.path.exists(path):
    os.makedirs(path)

files = []
while stack_pos < stack_size:
    capture_and_download(path, stack, stack_pos)
    move()
    stack_pos += 1
    time.sleep(0.5)

time.sleep(1)

upload_stack(str(stack))
    
print("Done!")
