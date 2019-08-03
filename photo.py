import logging
import os
import subprocess
import sys

import gphoto2 as gp

logger = logging.getLogger(__name__)


def capture_and_download(data_path, stack, stack_pos):

    # get camera
    callback_obj = gp.check_result(gp.use_python_logging())
    camera = gp.check_result(gp.gp_camera_new())
    gp.check_result(gp.gp_camera_init(camera))

    # capture image
    print("Capturing image")
    file_path = gp.check_result(gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE))

    # download file
    print("Camera file source path: {0}/{1}".format(file_path.folder, file_path.name))
    fn, ext = file_path.name.split(".")
    filename = "{}_{}.{}".format(fn, str(stack_pos), ext)
    target = os.path.join(data_path, filename)
    print("Copying image to destination:", target)
    camera_file = gp.check_result(
        gp.gp_camera_file_get(
            camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL
        )
    )
    gp.check_result(gp.gp_file_save(camera_file, target))

    # exit camera
    gp.check_result(gp.gp_camera_exit(camera))

    return target


if __name__ == "__main__":
    sys.exit(main())
