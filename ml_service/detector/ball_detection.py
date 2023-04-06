"""
Модуль определяет положение мяча на футбольном поле.
"""

import cv2
import numpy as np


def detect_ball():
    # Открываем видеопоток
    cap = cv2.VideoCapture(0) # 0 для камеры по умолчанию, либо имя файла

    # Определяем диапазон цветов мяча в формате HSV
    lower_color = np.array([25, 100, 100])
    upper_color = np.array([35, 255, 255])

    while True:
        # Считываем текущий кадр видеопотока
        ret, frame = cap.read()

        # Преобразуем кадр в цветовое пространство HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Создаем маску, используя определенный диапазон цветов
        mask = cv2.inRange(hsv_frame, lower_color, upper_color)

        # Выполняем операцию морфологического закрытия, чтобы устранить шумы
        kernel = np.ones((5,5),np.uint8)
        closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Находим контуры объектов на кадре
        contours, hierarchy = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Определяем контур с максимальной площадью, это и будет мячом
        max_area = 0
        max_contour = None
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                max_contour = contour

        # Рисуем прямоугольник вокруг мяча, если он найден
        if max_contour is not None:
            x,y,w,h = cv2.boundingRect(max_contour)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        # Показываем кадр с результатом
        cv2.imshow('Ball Detection', frame)

        # Выходим из цикла, если нажата клавиша 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Освобождаем ресурсы и закрываем окна
    cap.release()
    cv2.destroyAllWindows()
