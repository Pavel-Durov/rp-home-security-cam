import cv2
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import numpy as np

class VideoCamera(object):
    def __init__(self):
        self.video_stream = PiVideoStream().start()
        time.sleep(2.0)

    def __del__(self):
        self.video_stream.stop()

    def flip(self, frame):
        return np.flip(frame, 0)

    def get_jpeg_frame(self):
        frame = self.flip(self.video_stream.read())
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def get_frame(self):
         return  self.flip(self.video_stream.read()).copy()