# @Author            : Dario Gonzalez
# @Date              : 2020-02-23
# @Last Modified by  : Dario Gonzalez
# @Last Modified time: 2020-02-23

import os


#####################
# Server properties #
#####################
SERVER_URL = "/processimg/"


######################
# General properties #
######################
LOCAL_IMGPRCSSR_PATH = os.path.dirname(os.path.dirname(__file__))
IMAGE_REPOSITORY = LOCAL_IMGPRCSSR_PATH + "/imageexamples/"


#####################
# Logger properties #
#####################
LOG_PATH = LOCAL_IMGPRCSSR_PATH + "/logs/"

LOG_NAME = "imageprocessor"
LOG_TERMIN = ".log"

LOG_FORMATTER = "[%(asctime)s] %(levelname)s [%(process)d%(thread)d %(funcName)s] - %(message)s"
LOG_LVL = 10  # 10 DEBUG, 20 INFO, 30 WARNING, 40 ERROR, 50 CRITICAL
LOG_ROTATE_WHEN = "d"
LOG_ROTATE_INTERVAL = 1


########################
# Libraries properties #
########################
IMAGE_LIB = "ImagePIL" # Name of one of the classes in image.py
COMPRESSION_PARAM = 75 # With 85: No difference for 6-10Mb files - Lowest reasonable compression: 65
RESAMPLING_PARAM = 3   # NEAREST->0, LANCZOS->1, BILINEAR->2, BICUBIC->3, BOX->4, HAMMING->5
MAXIMUM_RESIZE = 10000 # In pixels
LIB_ACCCEPTED_IMG_FORMATS = {
    "image_formats":
    {
        "JPEG":
        {
            "file_extensions" : [".jpg", ".jpeg", ".jfif", ".pjpeg", ".pjp"],
            "mimetype": "image/jpeg"
        },
        "PNG":
        {
            "file_extensions" : [".png"],
            "mimetype": "image/png"
        }
    }
}
