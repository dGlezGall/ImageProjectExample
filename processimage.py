# @Author            : Dario Gonzalez
# @Date              : 2020-02-23
# @Last Modified by  : Dario Gonzalez
# @Last Modified time: 2020-02-23

import io
import os

from flask import (Flask, abort, jsonify, make_response, request, send_from_directory)

from imglibexploiters import image
from properties.properties import IMAGE_LIB, MAXIMUM_RESIZE, SERVER_URL, IMAGE_REPOSITORY
from utils import imglogger, commons
from utils.exceptions import ImageProcessorError, ResizingError, CompressionError

logger = imglogger.logger
app = Flask(__name__)


@app.errorhandler(400)
def bad_request(e):
    return make_response(str(e), 400)


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(str(e), 404)


@app.errorhandler(500)
def server_error(e):
    return make_response(str(e), 500)


@app.route(SERVER_URL + "helloworld", methods=['GET'])
def hello_world():
    logger.debug("Starting Hello, World!...")
    return jsonify({"Hello": "Hello, i am alive"}), 200


@app.route(SERVER_URL, methods=['GET'])
def no_image_getter():
    logger.debug("Starting...")
    logger.info("Bad request: {url}".format(
        url=request.url
    ))
    logger.debug("Ending...")
    abort(400, "no image was asked for")


@app.route(SERVER_URL + "<path:file_path>", methods=['GET'])
def image_getter(file_path):

    logger.debug("Starting...")

    width = request.args.get('width')
    height = request.args.get('height')

    folder_path, img_file_name = os.path.split(file_path)

    commons.abort_to_errors(width, height, img_file_name)

    img_instance = commons.get_instance(str(IMAGE_REPOSITORY + folder_path + "/"), str(img_file_name))

    final_img_name = commons.get_new_img_name(img_file_name, img_instance.get_file_ext(), width, height)
    img_instance.set_img_name(final_img_name)

    if commons.image_already_exists(img_instance):
        logger.debug("Successful ending")
        return send_from_directory(
                    img_instance.get_img_path(),
                    final_img_name,
                    attachment_filename=img_file_name,
                    mimetype=img_instance.get_mimetype()
        )

    commons.process_image(img_instance, width, height)

    logger.debug("Successful ending")

    return send_from_directory(
        img_instance.get_img_path(),
        img_instance.get_img_name(),
        attachment_filename=img_file_name,
        mimetype=img_instance.get_mimetype()
    )


if __name__ == "__main__":
    app.run()
