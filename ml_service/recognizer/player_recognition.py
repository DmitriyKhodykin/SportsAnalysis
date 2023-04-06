"""
Модуль определяет активного игрока, ведущего мяч.
"""

import cv2
import numpy as np

# Загрузка изображения и обработка с помощью OpenCV
image = cv2.imread("football.jpg")

# Преобразование изображения в черно-белое
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Применение фильтра Canny для выделения контуров объектов на изображении
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Применение алгоритма Хафа для обнаружения окружностей на изображении
circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, 20,
                           param1=50, param2=30, minRadius=0, maxRadius=0)

# Преобразование координат окружностей в целочисленные значения
circles = np.round(circles[0, :]).astype("int")

# Нахождение координат мяча
for (x, y, r) in circles:
    cv2.circle(image, (x, y), r, (0, 255, 0), 2)
    cv2.circle(image, (x, y), 2, (0, 0, 255), 3)
    ball_x, ball_y = x, y

# Обнаружение и классификация объектов на изображении
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Применение алгоритма HOG для обнаружения футболистов на изображении
rects, weights = hog.detectMultiScale(gray, winStride=(4, 4), padding=(8, 8), scale=1.05)

# Нахождение футболиста, находящегося ближе всего к мячу
closest_distance = float("inf")
closest_player = None
for (x, y, w, h) in rects:
    center_x = x + w / 2
    center_y = y + h / 2
    distance = ((center_x - ball_x) ** 2 + (center_y - ball_y) ** 2) ** 0.5
    if distance < closest_distance:
        closest_distance = distance
        closest_player = (x, y, w, h)

# Отображение результата на изображении
if closest_player is not None:
    (x, y, w, h) = closest_player
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(image, "Football Player", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
