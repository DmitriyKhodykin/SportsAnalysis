"""Модуль определяет положение игрока на футбольном поле.
"""

import cv2
import mediapipe as mp

# Создаем объект класса Holistic, использующего предобученную модель Mediapipe
mp_holistic = mp.solutions.holistic.Holistic()

# Открываем видеопоток
cap = cv2.VideoCapture(0) # 0 для камеры по умолчанию, либо имя файла

while True:
    # Считываем текущий кадр видеопотока
    ret, frame = cap.read()

    # Конвертируем кадр в цветовое пространство RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Обрабатываем кадр с помощью предобученной модели Mediapipe
    results = mp_holistic.process(frame)

    # Извлекаем координаты ключевых точек тела футболиста из результатов
    keypoints = []
    for data_point in results.pose_landmarks.landmark:
        keypoints.append((int(data_point.x * frame.shape[1]), int(data_point.y * frame.shape[0])))

    # Рисуем футболиста на кадре, используя ключевые точки тела
    if keypoints:
        cv2.polylines(frame, [keypoints[:17]], False, (0, 255, 0), thickness=2)
        cv2.polylines(frame, [keypoints[17:22]], False, (255, 0, 0), thickness=2)
        cv2.polylines(frame, [keypoints[22:27]], False, (255, 0, 0), thickness=2)
        cv2.polylines(frame, [keypoints[27:31]], False, (255, 0, 0), thickness=2)
        cv2.polylines(frame, [keypoints[31:36]], False, (255, 0, 0), thickness=2)
        cv2.polylines(frame, [keypoints[36:42]], True, (0, 0, 255), thickness=2)
        cv2.polylines(frame, [keypoints[42:48]], True, (0, 0, 255), thickness=2)
        cv2.polylines(frame, [keypoints[48:60]], True, (0, 0, 255), thickness=2)
        cv2.polylines(frame, [keypoints[60:65]], True, (0, 0, 255), thickness=2)
        cv2.polylines(frame, [keypoints[65:70]], True, (0, 0, 255), thickness=2)

    # Конвертируем кадр обратно в цветовое пространство BGR
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Отображаем кадр в окне
    cv2.imshow('Holistic Model - Mediapipe Detection', frame)

    # Выход из цикла, если нажата клавиша q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
