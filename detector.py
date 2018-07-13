import cv2
import motion3
from camera import VideoCamera
from fs_util import FsUtil
from rx import Observable, Observer

class VideoCameraDetector(object):
    def __init__(self, video_camera):
        self.image_detection_Observable = Observable.create(self.__initObservable)

        self.video_camera = video_camera
        self.fullbody = cv2.CascadeClassifier("models/fullbody_recognition_model.xml")
        self.upperbody = cv2.CascadeClassifier("models/upperbody_recognition_model.xml")
        self.human_facial = cv2.CascadeClassifier("models/facial_recognition_model.xml")
        self.cat_facial = cv2.CascadeClassifier("models/haarcascade_frontalcatface.xml")

    def detectFullBody(self):
        return self.__detect(self.fullbody)

    def detectFacial(self):
        return self.__detect(self.human_facial)

    def detectUpperBody(self):
        return self.__detect(self.upperbody)

    def detectCatFace(self):
        return self.__detect(self.cat_facial)

    def __initObservable(self, observer):
        self.observer = observer

    def __detect(self, classifier):
        frame = self.video_camera.get_frame()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detected_objects = classifier.detectMultiScale(gray,
                                                        scaleFactor=1.1,
                                                        minNeighbors=5,
                                                        minSize=(30, 30),
                                                        flags=cv2.CASCADE_SCALE_IMAGE)
        self.draw_detection_area(frame, detected_objects)
        detected = len(detected_objects) > 0
        return (frame, detected)

    def draw_detection_area(self, frame, objects):
        for (x, y, w, h) in objects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    def __detect_and_save_to_fs(self, detection_func, detection_type):
        frame, is_detected = detection_func()
        if is_detected:
            print('Detected:', detection_type)
            #self.observer.on_next('Detected: ' + detection_type)
            img_path = FsUtil.save_detection_img(frame, detection_type)
            self.observer.on_next((img_path, detection_type))

    def __detection_co(self):
        while True:
            self.__detect_and_save_to_fs(self.detectFacial, FsUtil.HUMAN_FACIAL)
            self.__detect_and_save_to_fs(self.detectFullBody, FsUtil.HUMAN_FULL_BODY)
            self.__detect_and_save_to_fs(self.detectUpperBody, FsUtil.HUMAN_UPPER_BODY)
            self.__detect_and_save_to_fs(self.detectCatFace, FsUtil.CAT_FACIAL)

    def start_detection_thread(self):
        FsUtil.create_dirs()
        t = threading.Thread(target=self.__detection_co, args=())
        t.daemon = True
        t.start()
