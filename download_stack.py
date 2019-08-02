# -*- coding: utf-8 -*-
import os
import sys
import logging
import uuid
import time
import glob

from dotenv import load_dotenv

from files import download_stack

load_dotenv()

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


def main(stack):
    download_stack(stack)
    print("Done!")


if __name__ == "__main__":
    main(sys.argv[1])
    sys.exit()
