# -*- coding: utf-8 -*-
import os
import sys
import logging
import uuid
import time
import glob

from dotenv import load_dotenv

from s3 import get_s3, store_stream_s3, get_matching_s3_keys, get_object_to_file


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

def download_stack(stack):
    path = "./data"
    s3 = get_s3()
    keys = get_matching_s3_keys(s3, BUCKET, prefix=stack)
    for key in keys:
        filepath = os.path.join(path, key)
        print("getting: {} => {}".format(key, filepath))
        
        stack_dir = os.path.join(*filepath.split("/")[:-1])
        if not os.path.exists(stack_dir):
            os.makedirs(stack_dir)

        get_object_to_file(BUCKET, key, filepath)
