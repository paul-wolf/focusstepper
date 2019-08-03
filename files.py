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
PATH_DATA = os.environ.get("PATH_DATA", "./data")

def stack_files(stack, spec="*.nef"):
    path = os.path.join(PATH_DATA, stack, spec)
    return glob.glob(path)

def upload_stack(stack):
    files = stack_files(stack)
    for fp in files:
        key = os.path.join(stack, fp.split("/")[-1])
        print("uploading: {} => {}".format(fp, key))
        store_stream_s3(BUCKET, open(fp, 'rb'), key)

def upload_image(stack, src_path):
    key = os.path.join(stack, src_path.split("/")[-1])
    print("uploading: {} => {}".format(src_path, key))
    store_stream_s3(BUCKET, open(src_path, 'rb'), key)

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
