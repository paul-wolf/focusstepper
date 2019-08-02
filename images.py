from wand.image import Image
# -*- coding: utf-8 -*-
import os
import sys
import logging
import uuid
import time
import glob
import subprocess

from dotenv import load_dotenv

from s3 import get_s3, store_stream_s3, get_matching_s3_keys, get_object_to_file


load_dotenv()
BUCKET = os.environ.get("BUCKET")

def convert_stack(stack):
    path = os.path.join("./data/", stack, "*.nef")
    print("Stack data: ", path)
    files = glob.glob(path)
    for fp in files:
        dest = fp.replace(".nef", ".tiff")
        print("converting: {} => {}".format(fp, dest))
        o = subprocess.call(['convert', fp, dest])
        print(o)
