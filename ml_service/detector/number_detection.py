"""
Модуль определяет квадрат видео, где находится номер игрока (на футболке).
"""

import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# cap = cv2.VideoCapture(0)  # Используем камеру
cap = cv2.VideoCapture('video.mp4')  # Используем видеофайл

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, image = cap.read()
        # Если видео, то 'break' вместо 'continue'
        if not success:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            # Отображаем ключевые точки на изображении
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Определяем номер футболиста
            left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]

            x1, y1 = int(left_shoulder.x * image.shape[1]), int(left_shoulder.y * image.shape[0])
            x2, y2 = int(right_shoulder.x * image.shape[1]), int(right_shoulder.y * image.shape[0])
            x3, y3 = int(left_hip.x * image.shape[1]), int(left_hip.y * image.shape[0])
            x4, y4 = int(right_hip.x * image.shape[1]), int(right_hip.y * image.shape[0]) 
            # Отслеживаем футболиста по номеру на футболке
            # Например, если футболист с номером 10, то ищем прямоугольник в районе его номера
            if 0.45 < left_shoulder.y < 0.55 and 0.45 < right_shoulder.y < 0.55 and \
                    0.65 < left_hip.y < 0.75 and 0.65 < right_hip.y < 0.75:
                roi = image[y1:y3, x1:x2]
                hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                lower_red = np.array([0, 50, 50])
            upper_red = np.array([10, 255, 255])
            mask = cv2.inRange(hsv, lower_red, upper_red)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)
                if w > 20 and h > 20:
                    cv2.rectangle(image, (x1+x, y1+y), (x1+x+w, y1+y+h), (0, 255, 0), 2)

    cv2.imshow('Football player tracking', image)
