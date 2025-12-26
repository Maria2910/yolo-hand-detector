import os

# Путь к папке с изображениями БЕЗ руки
no_hand_folder = "raw_data/no_hand"

# Для каждого .txt файла в папке no_hand
for filename in os.listdir(no_hand_folder):
    if filename.endswith(".txt"):
        filepath = os.path.join(no_hand_folder, filename)

        # Заменяем пустой файл на файл с классом 1
        with open(filepath, 'w') as f:
            f.write("1 0.05 0.05 0.02 0.02")

        print(f"Обновлен файл: {filename}")

print("Готово! Все фоновые изображения теперь имеют класс 1.")