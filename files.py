# -*- coding: utf-8 -*-
import os
import sys
import logging
import uuid
import time
import glob

from dotenv import load_dotenv

from s3 import store_stream_s3


load_dotenv()
BUCKET = os.environ.get("BUCKET")

def upload_stack(stack):
    path = os.path.join("./data/", stack, "*.nef")
    print("Stack data: ", path)
    files = glob.glob(path)
    for fp in files:
        key = os.path.join(stack, fp.split("/")[-1])
        print("uploading: {} => {}".format(fp, key))
        store_stream_s3(BUCKET, open(fp, 'rb'), key)
