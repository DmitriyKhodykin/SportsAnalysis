"""
Модуль определяет момент удара игрока по мячу.
"""

import cv2
import mediapipe as mp
import numpy as np


cap = cv2.VideoCapture(0)
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            # Переводим картинку в серый цвет для лучшей работы алгоритма
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Используем алгоритм Canny для выделения контуров объектов на изображении
            edges = cv2.Canny(gray, 100, 200)

            # Определяем точки на теле футболиста с помощью Mediapipe
            results = pose.process(frame)
            landmarks = results.pose_landmarks

            if landmarks is not None:
                # Определяем координаты ключевых точек на теле футболиста
                lankle = [int(landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].x * frame.shape[1]),
                          int(landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].y * frame.shape[0])]
                rfoot = [int(landmarks.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].x * frame.shape[1]),
                         int(landmarks.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].y * frame.shape[0])]

                # Определяем координаты мяча на изображении
                ball_cascade = cv2.CascadeClassifier('ball_cascade.xml')
                balls = ball_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
                for (x, y, w, h) in balls:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Определяем, был ли сделан удар по мячу
                if lankle[1] < rfoot[1] and (rfoot[0] - x) < 30 and (rfoot[1] - y) < 30:
                    cv2.putText(frame, 'KICK!', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)

            # Отображаем результат на экране
            cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()