import os

# Путь к папке с размеченными файлами
labels_folder = "raw_data/hand"

# Проходим по всем .txt файлам в папке
for filename in os.listdir(labels_folder):
    if filename.endswith(".txt"):
        filepath = os.path.join(labels_folder, filename)

        with open(filepath, 'r') as file:
            lines = file.readlines()

        # Создаем новый список исправленных строк
        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if parts:
                parts[0] = '0'
                new_lines.append(" ".join(parts) + "\n")

        # Перезаписываем файл с исправленными данными
        with open(filepath, 'w') as file:
            file.writelines(new_lines)

        print(f"Исправлен файл: {filename}")

print("Готово! Все файлы исправлены.")