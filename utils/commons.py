# @Author            : Dario Gonzalez
# @Date              : 2020-02-23
# @Last Modified by  : Dario Gonzalez
# @Last Modified time: 2020-02-23

import os

from flask import abort, request

from imglibexploiters import image
from properties.properties import (
    COMPRESSION_PARAM, IMAGE_LIB, IMAGE_REPOSITORY, LIB_ACCCEPTED_IMG_FORMATS,
    MAXIMUM_RESIZE)
from utils import imglogger
from utils.exceptions import (CompressionError, ImageProcessorError,
                              ResizingError)

logger = imglogger.logger


def get_mimetype_from_properties(ext_to_search):
    logger.debug("Searching for mimetype of {}".format(ext_to_search))
    for format_name, image_format in LIB_ACCCEPTED_IMG_FORMATS["image_formats"].items():
        for file_extension in image_format["file_extensions"]:
            if file_extension == ".{}".format(ext_to_search):
                logger.debug("{extension} found - it's mimetype is {mymetype}".format(
                    extension=ext_to_search,
                    mymetype=image_format["mimetype"]
                ))
                return image_format["mimetype"]
    logger.debug("{} not found in accepted image formats".format(ext_to_search))
    return ""


def get_format_from_properties(ext_to_search):
    logger.debug("Searching for image format of {}".format(ext_to_search))
    for format_name, image_format in LIB_ACCCEPTED_IMG_FORMATS["image_formats"].items():
        for file_extension in image_format["file_extensions"]:
            if file_extension == ".{}".format(ext_to_search):
                logger.debug("{extension} found - it's image format name is {format}".format(
                    extension=ext_to_search,
                    format=format_name
                ))
                return format_name
    logger.debug("{} not found in accepted image formats".format(ext_to_search))
    return ""


def get_valid_extensions():
    logger.debug("Getting valid file extensions...")
    valid_extensions = []
    for format_name, image_format in LIB_ACCCEPTED_IMG_FORMATS["image_formats"].items():
        for file_extension in image_format["file_extensions"]:
            valid_extensions.append(file_extension)
    logger.debug("Valid extensions: {}".format(valid_extensions))
    return tuple(valid_extensions)


def get_new_img_name(img_file_name, file_extension, width=None, height=None):

    logger.debug("Getting new image name...")

    image_name = os.path.splitext(img_file_name)[0]
    final_name = ""

    if width and height:
        final_name = "{image_name}-{width}x{height}-{compression}.{file_extension}".format(
                            image_name=str(image_name),
                            width=str(width),
                            height=str(height),
                            compression=str(COMPRESSION_PARAM),
                            file_extension=str(file_extension))
    else:
        final_name = "{image_name}-{compression}.{file_extension}".format(
                            image_name=str(image_name),
                            compression=str(COMPRESSION_PARAM),
                            file_extension=str(file_extension))

    return final_name


def image_already_exists(img_instance):
    return os.path.isfile(img_instance.get_img_path() + img_instance.get_img_name())



def abort_to_errors(width, height, image_file_name):

    if bool(width) != bool(height):
        logger.info("Bad request: error on width or height parameter - " + str(request.query_string))
        logger.debug("Ending...")
        abort(400, "Error in width or height parameter - " + str(request.query_string))
    elif not image_file_name.endswith(get_valid_extensions()):
        logger.info("Bad request: not an accepted file extension - " + image_file_name)
        logger.debug("Ending...")
        abort(400, "Not an accepted file extension - " + image_file_name)


def get_instance(img_path, img_name):

    img_cls = getattr(image, IMAGE_LIB)

    try:
        image_instance = img_cls(img_path, img_name)
    except ImageProcessorError:
        logger.critical("Could not find ALREADY VALIDATED extension in accepted image formats")
        logger.debug("Ending...")
        abort(500, "Internal server error")
    image_instance.open_img(img_name)

    if not image_instance.is_img_opened():
        logger.info("Image {} not found".format(img_path))
        logger.debug("Ending...")
        abort(404, "Image {path}{name} not found".format(
            path=img_path,
            name=img_name
        ))

    return image_instance


def process_image(image_instance, width, height):

    if width and height:
        try:
            width = int(width)
            height = int(height)
            image_instance.set_width(width)
            image_instance.set_height(height)
        except ValueError:
            logger.info("Bad request: width or height not an integer - " + str(request.query_string))
            logger.debug("Ending...")
            abort(400, "Width and height must be integers - " + str(request.query_string))

        if (width >= MAXIMUM_RESIZE) or (height >= MAXIMUM_RESIZE):
            logger.info("Bad request: width or height over maximum value, which is " + str(MAXIMUM_RESIZE))
            abort(400, "Width or height over maximum value, which is " + str(MAXIMUM_RESIZE))

        try:
            image_instance.resize(width, height)
        except ResizingError:
            logger.debug("Ending...")
            abort(400, "Resize error - check height or width")

    try:
        image_instance.compress()
    except CompressionError:
        logger.debug("Ending...")
        abort(500, "Internal server error")
