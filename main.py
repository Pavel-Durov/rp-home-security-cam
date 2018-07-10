from telegram_bot import TelegramBot
import server
import time
from camera import VideoCamera
from detector import VideoCameraDetector

video_camera = VideoCamera()
detector = VideoCameraDetector(video_camera)
telegram_bot = TelegramBot(video_camera);

def on_detection(detection):
    telegram_bot.notify_image(detection[0])
    time.sleep(0.5)
    telegram_bot.notify_text(detection[1])

if __name__ == '__main__':
    telegram_bot.start()
    detector.image_detection_Observable.subscribe(on_detection)
    detector.start_detection_thread()
    server.start(video_camera)
