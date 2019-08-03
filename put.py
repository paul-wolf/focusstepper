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


def put_files(stack, spec):
    p = os.path.join(PATH_DATA, stack)
    if not os.path.exists(p):
        print("Path does not exist: {}".format(p))
        raise SystemExit
    path = os.path.join(PATH_DATA, stack, spec)
    files = glob.glob(path)
    for fp in files:
        key = os.path.join(stack, fp.split("/")[-1])
        print("uploading: {} => {}".format(fp, key))
        store_stream_s3(BUCKET, open(fp, "rb"), key)


if __name__ == "__main__":
    sys.exit(put_files(sys.argv[1], sys.argv[2]))
