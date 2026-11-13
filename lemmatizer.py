
import re
import csv
from pathlib import Path
from collections import Counter
from pymystem3 import Mystem


# ==========================================
# 1. НАСТРОЙКИ
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

MYSTEM_PATH = BASE_DIR / "mystem"


# ==========================================
# 2. ЗАГРУЗКА ЛЮБОГО ТЕКСТА
# ==========================================

def read_text():

    filename = input(
        "Введите название текстового файла (.txt): "
    ).strip()

    # Если введён путь к файлу, используем его.
    # Если только название — ищем файл в папке программы.
    input_file = Path(filename).expanduser()

    if not input_file.is_absolute():
        input_file = BASE_DIR / input_file

    if not input_file.exists():
        raise FileNotFoundError(
            f"Файл {input_file} не найден."
        )

    text = input_file.read_text(encoding="utf-8")

    print("\nФайл успешно загружен:", input_file.name)

    return text, input_file.stem


# ==========================================
# 3. ПРЕДВАРИТЕЛЬНАЯ ОБРАБОТКА
# ==========================================

def clean_text(text):

    # Приведение к нижнему регистру
    text = text.casefold()

    # Удаление чисел
    text = re.sub(r"\d+", " ", text)

    # Удаление пунктуации и специальных символов
    text = re.sub(r"[^\w\s]", " ", text)

    # Удаление подчёркиваний
    text = text.replace("_", " ")

    # Удаление лишних пробелов
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ==========================================
# 4. ЛЕММАТИЗАЦИЯ
# ==========================================

def lemmatize_text(text):

    mystem = Mystem(
        mystem_bin=str(MYSTEM_PATH),
        disambiguation=True
    )

    result = mystem.lemmatize(text)

    lemmas = [
        lemma.strip()
        for lemma in result
        if lemma.strip()
    ]

    return lemmas


# ==========================================
# 5. ЧАСТОТНЫЙ АНАЛИЗ
# ==========================================

def calculate_frequency(lemmas):

    frequency = Counter(lemmas)

    return frequency


# ==========================================
# 6. СОХРАНЕНИЕ РЕЗУЛЬТАТОВ
# ==========================================

def save_results(name, cleaned_text, lemmas, frequency):

    # Очищенный текст
    clean_file = BASE_DIR / f"{name}_cleaned.txt"

    clean_file.write_text(
        cleaned_text,
        encoding="utf-8"
    )

    # Лемматизированный текст
    lemma_file = BASE_DIR / f"{name}_lemmas.txt"

    lemma_file.write_text(
        " ".join(lemmas),
        encoding="utf-8"
    )

    # Частотная таблица
    frequency_file = BASE_DIR / f"{name}_frequency.csv"

    with open(
        frequency_file,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Лемма",
            "Количество употреблений"
        ])

        for lemma, count in frequency.most_common():
            writer.writerow([lemma, count])

    print("\nРезультаты сохранены:")
    print(clean_file.name)
    print(lemma_file.name)
    print(frequency_file.name)


# ==========================================
# 7. ОСНОВНАЯ ПРОГРАММА
# ==========================================


def main():

    print("=" * 50)
    print("ЛЕММАТИЗАТОР ТЕКСТА")
    print("=" * 50)

    try:
        original_text, name = read_text()
        cleaned_text = clean_text(original_text)
        lemmas = lemmatize_text(cleaned_text)
        frequency = calculate_frequency(lemmas)

        print("\nЛЕММАТИЗИРОВАННЫЙ ТЕКСТ:")
        print(" ".join(lemmas))

        print("\nЧАСТОТНОСТЬ КАЖДОЙ ЛЕММЫ:")
        for lemma, count in frequency.most_common():
            print(f"{lemma}: {count}")

        print("\nОБЩАЯ СТАТИСТИКА:")
        print("Всего слов:", len(lemmas))
        print("Уникальных лемм:", len(frequency))

        save_results(name, cleaned_text, lemmas, frequency)

    except FileNotFoundError as error:
        print("\nОшибка:", error)

    except Exception as error:
        print("\nОшибка обработки:", error)


if __name__ == "__main__":
    main()

