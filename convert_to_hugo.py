import os
import re

# Структура размещения бесед
ARTICLE_PLACEMENT = {
    1: ("introduction", "Общее введение"),
    2: ("1-thessalonians", "Беседа 2"),
    3: ("1-thessalonians", "Беседа 3"),
    4: ("1-thessalonians", "Беседа 4"),
    5: ("1-thessalonians", "Беседа 5"),
    6: ("1-thessalonians", "Беседа 6"),
    7: ("1-thessalonians", "Беседа 7"),
    8: ("1-thessalonians", "Беседа 8"),
    9: ("2-thessalonians", "Беседа 9"),
    10: ("2-thessalonians", "Беседа 10"),
}

SOURCE_DIR = "/Users/slava/Desktop/Pauline-epistles/iannuary_letters_md"
TARGET_DIR = "/Users/slava/Desktop/Pauline-epistles/iannuary/content/letters"

TITLES = {
    1: "Беседа 1. Послания апостола Павла. Общее введение",
    2: "Беседа 2. Первое послание к Фессалоникийцам и античные письма",
    3: "Беседа 3. Первое послание к Фессалоникийцам. История создания",
    4: "Беседа 4. Первое послание к Фессалоникийцам (1 Фесс.1.2-5)",
    5: "Беседа 5. Первое послание к Фессалоникийцам (1Фесс.1.6-2.12)",
    6: "Беседа 6. Первое послание к Фессалоникийцам (1 Фесс.2.13-4.12)",
    7: "Беседа 7. Первое послание к Фессалоникийцам (1 Фесс. 4.13 — 4.18)",
    8: "Беседа 8. Первое послание к Фессалоникийцам (1 Фесс. 5.1-28)",
    9: "Беседа 9. Второе послание к Фессалоникийцам. История создания",
    10: "Беседа 10. Второе послание к Фессалоникийцам. Обзорная беседа",
}

def convert_to_hugo(source_file, target_file, num):
    """Конвертирует markdown файл в формат Hugo"""
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Удаляем старый YAML front matter
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

    # Убираем дублирующийся заголовок (первый # заголовок)
    content = re.sub(r'^#\s+.+?\n', '', content)

    # Разбиваем на строки и обрабатываем
    lines = content.split('\n')
    cleaned_lines = []
    found_start = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Пропускаем до нахождения начала основного текста
        if not found_start:
            # Пропускаем пустые строки и точки
            if not stripped or stripped == '.':
                continue
            # Пропускаем метаданные
            if stripped.startswith('Цикл:') or stripped == 'Цикл':
                continue
            if stripped.startswith('Тематика:') or stripped == 'Тематика':
                continue
            if stripped.startswith('Текст набран:') or stripped == 'Текст набран':
                continue
            if 'Беседы о посланияx' in stripped:
                continue
            if 'Послания к Фессалоникийцам' in stripped:
                continue
            if stripped == 'Людмила Зотова' or stripped.startswith('Людмила'):
                continue

            # Нашли начало текста
            if stripped.startswith('Возлюбленные') or stripped.startswith('Здравствуйте') or stripped.startswith('Добрый'):
                found_start = True
                cleaned_lines.append(line)
            elif len(stripped) > 100:
                # Длинная строка без метаданных - тоже начало
                found_start = True
                cleaned_lines.append(line)
        else:
            cleaned_lines.append(line)

    content = '\n'.join(cleaned_lines)
    content = content.lstrip('\n')

    title = TITLES.get(num, f"Беседа {num}")

    # Создаём новый front matter
    front_matter = f'''---
title: "{title}"
weight: {num}
---

'''

    # Записываем результат
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(front_matter + content)

    print(f"  -> {target_file}")

def main():
    print("Конвертация статей в формат Hugo...")

    for num, (folder, _) in ARTICLE_PLACEMENT.items():
        source = os.path.join(SOURCE_DIR, f"beseda-{num:02d}.md")
        target_dir = os.path.join(TARGET_DIR, folder)
        target = os.path.join(target_dir, f"{num:02d}.md")

        if os.path.exists(source):
            convert_to_hugo(source, target, num)
        else:
            print(f"  !! Файл не найден: {source}")

    print("\nГотово!")

if __name__ == "__main__":
    main()
