import time
import calendar
from os import path
import pathlib
import cv2

class FsUtil(object):
    JPEG_EXTENTION = '.jpg'
    IMG_DIR = './img'
    CAT_FACIAL = 'cat_facial'
    HUMAN_FACIAL = 'human_facial'
    HUMAN_FULL_BODY = 'human_full_body'
    HUMAN_UPPER_BODY = 'human_upper_body'
    IMG_GLOBAL = 'global'

    @staticmethod
    def __create_img_dir(name):
        full_path = path.join(FsUtil.IMG_DIR, name)
        pathlib.Path(full_path).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def create_dirs():
        for dir_name in FsUtil.__get_dir_names():
            FsUtil.__create_img_dir(dir_name)

    @staticmethod
    def __get_dir_names():
        return [FsUtil.CAT_FACIAL,
                FsUtil.HUMAN_FACIAL,
                FsUtil.HUMAN_FULL_BODY,
                FsUtil.HUMAN_UPPER_BODY,
                FsUtil.IMG_GLOBAL]

    @staticmethod
    def save_detection_img(image, folder_name):
        img_name = FsUtil.__generate_img_name();
        full_name = path.join(FsUtil.IMG_DIR, folder_name, img_name)
        cv2.imwrite(full_name, image)
        return full_name

    @staticmethod
    def __generate_img_name():
        return FsUtil.__get_timestamp_str() + FsUtil.JPEG_EXTENTION

    @staticmethod
    def __get_timestamp_str():
        return str(calendar.timegm(time.gmtime()))
