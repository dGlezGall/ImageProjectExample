# @Author            : Dario Gonzalez
# @Date              : 2020-02-23
# @Last Modified by  : Dario Gonzalez
# @Last Modified time: 2020-02-23

class ImageProcessorError(Exception):
    pass


class ResizingError(ImageProcessorError):
    pass


class CompressionError(ImageProcessorError):
    pass
