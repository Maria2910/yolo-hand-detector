import os
import random
import shutil

# Исходные папки
source_hand = "raw_data/hand"
source_no_hand = "raw_data/no_hand"

# Папки назначения
image_train_dir = "dataset/images/train"
image_val_dir = "dataset/images/val"
label_train_dir = "dataset/labels/train"
label_val_dir = "dataset/labels/val"

# Создаем папки назначения
for dir_path in [image_train_dir, image_val_dir, label_train_dir, label_val_dir]:
    os.makedirs(dir_path, exist_ok=True)

# Собираем ВСЕ пары файлов (изображение + метка) из ОБЕИХ папок
all_files = []
# Из папки hand
for filename in os.listdir(source_hand):
    if filename.endswith(".jpg"):
        base_name = os.path.splitext(filename)[0]
        all_files.append(("hand", base_name))
# Из папки no_hand
for filename in os.listdir(source_no_hand):
    if filename.endswith(".jpg"):
        base_name = os.path.splitext(filename)[0]
        all_files.append(("no_hand", base_name))

# Перемешиваем все пары
random.shuffle(all_files)

# Определяем границу разделения (70% на обучение, 30% на валидацию)
split_idx = int(len(all_files) * 0.7)
train_files = all_files[:split_idx]
val_files = all_files[split_idx:]


# Функция для копирования файлов
def copy_files(file_list, source_type, image_dest, label_dest):
    for source_folder, base_name in file_list:
        # Определяем исходные папки
        if source_folder == "hand":
            src_img_folder = source_hand
            src_label_folder = source_hand
        else:  # "no_hand"
            src_img_folder = source_no_hand
            src_label_folder = source_no_hand

        # Копируем изображение
        for ext in ['.jpg', '.jpeg', '.png', '.JPG']:
            src_img = os.path.join(src_img_folder, base_name + ext)
            if os.path.exists(src_img):
                shutil.copy2(src_img, os.path.join(image_dest, base_name + ext))
                break

        # Копируем метку (файл .txt)
        src_label = os.path.join(src_label_folder, base_name + ".txt")
        if os.path.exists(src_label):
            shutil.copy2(src_label, os.path.join(label_dest, base_name + ".txt"))
        else:
            # Создаем пустой файл метки, если его нет
            open(os.path.join(label_dest, base_name + ".txt"), 'w').close()


# Копируем файлы
print(f"Копируем {len(train_files)} пар в тренировочный набор...")
copy_files(train_files, "mixed", image_train_dir, label_train_dir)
print(f"Копируем {len(val_files)} пар в валидационный набор...")
copy_files(val_files, "mixed", image_val_dir, label_val_dir)

print("Готово! Данные разделены.")