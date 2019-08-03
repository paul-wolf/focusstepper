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
PATH_DATA = os.environ.get("PATH_DATA", "./data")

def convert_stack(stack):
    p = os.path.join(PATH_DATA, stack)
    if not os.path.exists(p):
        print("Path does not exist: {}".format(p))
        raise SystemExit
    path = os.path.join(PATH_DATA, stack, "*.nef")
    print("Stack data: ", path)
    files = glob.glob(path)
    for fp in files:
        dest = fp.replace(".nef", ".tiff")
        print("converting: {} => {}".format(fp, dest))
        o = subprocess.call(['convert', fp, dest])
        print(o)

def enfuse_merge(stack):
    path = os.path.join(PATH_DATA, stack, "output.tif")
    s = """enfuse --exposure-weight=0 --saturation-weight=0 --contrast-weight=1 --hard-mask --gray-projector=l-star --contrast-window-size=5  --output=output.tif {stack}/*.tiff""".format(stack=stack)
    o = subprocess.call(s.split(" "))
    print(o)
    
if __name__ == "__main__":
    sys.exit(convert_stack(sys.argv[1]))
