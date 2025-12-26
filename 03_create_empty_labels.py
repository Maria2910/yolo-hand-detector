import os

# Путь к папке с изображениями БЕЗ руки
no_hand_folder = "raw_data/no_hand"

# Для каждого .jpg файла создаем пустой .txt файл с таким же именем
for filename in os.listdir(no_hand_folder):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        txt_filename = os.path.splitext(filename)[0] + ".txt"
        txt_filepath = os.path.join(no_hand_folder, txt_filename)

        # Создаем пустой файл
        with open(txt_filepath, 'w') as f:
            pass

        print(f"Создан пустой файл для: {filename}")

print("Готово! Все пустые файлы меток созданы.")