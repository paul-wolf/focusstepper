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


def get_files(stack, spec):
    path = os.path.join(PATH_DATA, stack)
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(PATH_DATA, stack, spec)
    files = glob.glob(path)
    for fp in files:
        key = os.path.join(stack, fp.split("/")[-1])
        print("uploading: {} => {}".format(fp, key))
        store_stream_s3(BUCKET, open(fp, "rb"), key)


def get_files(stack, spec):
    path = PATH_DATA
    s3 = get_s3()
    keys = get_matching_s3_keys(s3, BUCKET, prefix=stack, suffix=spec)
    for key in keys:
        filepath = os.path.join(path, key)
        stack_dir = os.path.join(*filepath.split("/")[:-1])
        if not os.path.exists(stack_dir):
            os.makedirs(stack_dir)
        print("{} => {}".format(key, filepath))

        get_object_to_file(BUCKET, key, filepath)


if __name__ == "__main__":
    sys.exit(get_files(sys.argv[1], sys.argv[2]))
