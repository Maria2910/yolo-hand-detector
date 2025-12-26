import cv2
from ultralytics import YOLO
import time
import numpy as np

# Загружаем лучшую модель
print("Загрузка модели...")
model = YOLO('runs/detect/hand_detector_v2/weights/best.pt')
print("Модель загружена!")
print(f"Метрики модели: mAP50=95.9%, Precision=93.1%, Recall=86.8%")

# Открываем камеру
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Ошибка: Не удалось открыть камеру!")
    exit()

prev_time = 0
fps_list = []
detection_history = []  # История последних 10 детекций для стабильности

print("\n=== РЕЖИМ РЕАЛЬНОГО ВРЕМЕНИ ===")
print("Инструкция:")
print("1. Покажите руку в камеру")
print("2. Уберите руку из кадра")
print("3. Нажмите 'q' для выхода")
print("=" * 40)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Ошибка: Не удалось получить кадр с камеры")
        break

    # Детекция
    results = model(frame, verbose=False, conf=0.5)[0]

    # Определяем, есть ли рука (класс 0) в кадре
    has_hand = any(box.cls == 0 for box in results.boxes) if results.boxes else False

    # Добавляем в историю (для стабильности)
    detection_history.append(has_hand)
    if len(detection_history) > 10:
        detection_history.pop(0)

    # Сглаживание: если в 7 из 10 последних кадров была рука - считаем что она есть
    smoothed_has_hand = sum(detection_history) >= 7

    # Расчет FPS
    current_time = time.time()
    fps = 1 / (current_time - prev_time) if (current_time - prev_time) > 0 else 0
    fps_list.append(fps)
    avg_fps = np.mean(fps_list[-20:]) if len(fps_list) > 0 else fps
    prev_time = current_time

    # Подготовка текста
    status = "HAND: DETECTED" if smoothed_has_hand else "HAND: NOT FOUND"
    color = (0, 255, 0) if smoothed_has_hand else (0, 0, 255)

    # Фон для текста (для лучшей читаемости)
    cv2.rectangle(frame, (5, 5), (450, 90), (0, 0, 0), -1)

    # Отрисовка результатов
    cv2.putText(frame, status, (10, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.putText(frame, f"FPS: {int(avg_fps)}", (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Отрисовка bounding boxes с уверенностью
    if results.boxes:
        for box in results.boxes:
            if box.cls == 0:  # Только для класса "hand"
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"hand {conf:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)

    # Отображение кадра
    cv2.imshow('YOLOv11 Hand Detector - FINAL PROJECT', frame)

    # Выход по нажатию 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("\nВыход по запросу пользователя")
        break

# Корректное завершение
cap.release()
cv2.destroyAllWindows()

# Статистика
if fps_list:
    print(f"\n=== СТАТИСТИКА ===")
    print(f"Средний FPS: {np.mean(fps_list):.1f}")
    print(f"Максимальный FPS: {np.max(fps_list):.1f}")
    print(f"Минимальный FPS: {np.min(fps_list):.1f}")
    print(f"Процент кадров с рукой: {sum(detection_history) / len(detection_history) * 100:.1f}%")