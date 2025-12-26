from ultralytics import YOLO
import os

# Указываем полный путь к файлу конфигурации данных
data_yaml_path = os.path.abspath('data.yaml')
print(f"Using data config from: {data_yaml_path}")

model = YOLO('yolo11n.pt')

# Обучаем модель
results = model.train(
    data=data_yaml_path,
    epochs=50,
    imgsz=640,
    batch=8,
    name='hand_detector_v2',
    device='cpu',
    patience=10,
    lr0=0.01,
    lrf=0.01,
    optimizer='SGD'
)

print("Обучение завершено!")