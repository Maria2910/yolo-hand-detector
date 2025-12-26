import cv2
import os
import time

current_class = 'hand'

# Создаем папку для класса, если её нет
save_dir = f'raw_data/{current_class}'
os.makedirs(save_dir, exist_ok=True)

cap = cv2.VideoCapture(0)
counter = 0
print(f"Сбор данных для класса: '{current_class}'. Нажмите SPACE для снимка, ESC для выхода.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Показываем инструкцию на экране
    cv2.putText(frame, f"Class: {current_class}. Collected: {counter}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, "SPACE: Capture  |  ESC: Exit", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow('Collect Data', frame)

    key = cv2.waitKey(1)

    if key == 27:  # ESC - выход
        break
    elif key == 32:  # SPACE - сохранить кадр
        filename = os.path.join(save_dir, f"{current_class}_{counter:04d}.jpg")
        cv2.imwrite(filename, frame)
        print(f"Saved: {filename}")
        counter += 1
        time.sleep(0.5)

cap.release()
cv2.destroyAllWindows()
print(f"Собрано {counter} изображений для класса '{current_class}'.")