import server
from camera import VideoCamera
from detector import VideoCameraDetector

video_camera = VideoCamera()
detector = VideoCameraDetector(video_camera)

if __name__ == '__main__':
    detector.start_detection_thread()
    server.start(video_camera)