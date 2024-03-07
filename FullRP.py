import keyboard
import speech_recognition as sr

# Словарь для замены слов на соответствующие знаки препинания, присоединенные к предыдущему слову
replacement_dict = {
    "запятая": ",",
    "точка": ".",
    "вопросительный знак": "?",
    "восклицательный знак": "!",
    "двоеточие": ":",
    "многоточие": "...",
    "тире": "–"
}

def listen_microphone():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Слушаю...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language="ru-RU")
        print(f"Результат: {text.capitalize()}.")

        # Замена слов на соответствующие знаки препинания, если необходимо
        for word, replacement in replacement_dict.items():
            text = text.replace(word, replacement)

        # Удаление пробела перед знаками препинания
        punctuation_marks = [",", ".", "?", "!", ":", "...", "–"]
        for mark in punctuation_marks:
            text = text.replace(f" {mark}", mark)
        
        # Проверка и исправление заглавной буквы для следующего слова после точки, восклицательного и вопросительного знаков
        text = text.strip()  # Удаление лишних пробелов в начале и конце текста

        if not text.endswith((".", "!", "?", "...")):
            text += "."  # Добавление точки, если текст не оканчивается на знак препинания

        text = text.capitalize()  # Первая буква текста заглавная
        print(f"Пунктуация: {text}")
        keyboard.write(f"{text}")
    except sr.UnknownValueError:
        print("Не удалось распознать речь.")
    except sr.RequestError as e:
        print(f"Ошибка сервиса распознавания речи: {e}")


def handle_hotkey():
    keyboard.wait('Page Down')
    listen_microphone()
    keyboard.press_and_release('End')
    handle_hotkey()


handle_hotkey()