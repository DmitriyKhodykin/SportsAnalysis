"""
Модуль определяет номер игрока на футболке.
"""

import cv2
import numpy as np
from number_recognition import NumberRecognizer


# Загрузка изображения по кадрам
img = cv2.imread('image.jpg')
model = NumberRecognizer()
model.init() # create a model
model.load() # load the model

# Преобразование в градации серого
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Применение пороговой фильтрации для бинаризации изображения
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Поиск контуров на бинарном изображении
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Извлечение области, содержащей цифру
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    if w > 10 and h > 10:
        digit = gray[y:y+h, x:x+w]

        # Изменение размера образца до размера, соответствующего обученной модели
        resized_digit = cv2.resize(digit, (28, 28))

        # Преобразование образца в формат, необходимый для обученной модели
        sample = np.array(resized_digit, dtype=np.float32)
        sample = sample.reshape((1, 1, 28, 28))

        # Распознавание образца с использованием предобученной модели
        num = model.recognize(sample) # распознавание числа

        # Вывод распознанной цифры на изображение
        cv2.putText(img, str(np.argmax(num)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# Отображение результата
cv2.imshow('Result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
