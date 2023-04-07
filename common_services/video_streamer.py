"""
Модуль запускает видеопоток для аналитики.

В этом классе используется библиотека OpenCV для чтения видеопотока из файла. 
Класс имеет три метода:

__init__(self, video_path) - конструктор, который принимает путь к видеофайлу 
и создает объект VideoCapture для чтения видеопотока из этого файла.

__del__(self) - деструктор, который освобождает ресурсы, занятые объектом VideoCapture.

read_frame(self) - метод, который читает один кадр видеопотока и возвращает его 
в виде объекта numpy array. Если видеопоток закончился, метод возвращает None.
"""

import cv2

from get_config import open_config


class VideoStream:
    def __init__(self, video_path):
        self.video_path = video_path
        self.video_stream = cv2.VideoCapture(video_path)
        
    def __del__(self):
        self.video_stream.release()
        
    def read_frame(self):
        ret, frame = self.video_stream.read()
        if not ret:
            return None
        return frame


if __name__ == "__main__":
    config = open_config()
    video_path = config["video"]["path"]
    video_stream = VideoStream(video_path)

    while True:
        frame = video_stream.read_frame()
        if frame is None:
            break
        cv2.imshow('Video Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()
