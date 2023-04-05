import cv2
import numpy as np

# Загрузка изображения
img = cv2.imread('image.jpg')

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
        resized_digit = cv2.resize(digit, (18, 18))

        # Преобразование образца в формат, необходимый для обученной модели
        sample = np.array(resized_digit, dtype=np.float32)
        sample = sample.reshape((1, 1, 18, 18))

        # Распознавание образца с использованием обученной модели
        result = model.predict(sample)

        # Вывод распознанной цифры на изображение
        cv2.putText(img, str(np.argmax(result)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# Отображение результата
cv2.imshow('Result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
