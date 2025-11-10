from yandex_cloud_ml_sdk import YCloudML
from dotenv import load_dotenv
import os

root_path = os.path.dirname(__file__)
env_path = os.path.join(root_path, '..', '.env')

load_dotenv(dotenv_path=env_path)

FOLDER_ID = os.getenv("AI_FOLDER_ID")
TOKEN = os.getenv("AI_TOKEN")

sdk = YCloudML(
    folder_id=FOLDER_ID,
    auth=TOKEN,
)
model = sdk.models.completions("yandexgpt")


def preprocess_text(text: str):
    return text.replace("```", "").replace("html", "")


def get_answer_ai(lesson_name: str, desc: str, material: str, user_question: str, temp=0.5):
    global model
    model = model.configure(temperature=temp)
    ai_answer = model.run(f"Ты - AI-репетитор. \n"
                          f"Название урока: {lesson_name}\n"
                          f"Описание урока: {desc}\n"
                          f"Контекст урока: '{material}\n'."
                          f"Вопрос студента: '{user_question}'.\n"
                          "Дай развернутый, но четкий ответ, основанный на предоставленных данных. Если ответа в данных нет, так и скажи.")
    return preprocess_text(ai_answer.alternatives[0].text)


def compare_answers(user_answer, true_answer, temp=0.5):
    global model
    model = model.configure(temperature=temp)
    ai_answer = model.run(
        f"Ты - AI-репетитор. Сравни ответ студента '{user_answer}' с эталонным решением '{true_answer}'. Является ли ответ студента верным? Ответь ТОЛЬКО 'true' или 'false'.")
    return preprocess_text(ai_answer.alternatives[0].text)


def generate_comp_profile(statistic: str, temp=0.5):
    global model
    model = model.configure(temperature=temp)
    ai_answer = model.run(
        f"Ты - AI-репетитор. \n"
        f"Формат: Название области компетенции: уровень знаний, после каждой компетенции переносить на новую строку. Разметка в виде HTML и тег только <b> и <i> по желанию, ВСЕ ТЕГИ ОБЯЗАТЕЛЬНО НУЖНО ЗАКРЫВАТЬ. В начале не указывай ``` и тип текста. Добавляй смайлики строго по контексту.\n"
        f"Условие: сгенерируй в красивом формате под response в телеграмм боте. В начале должна быть надпись 'Результат анализа Ваших тестов:' жирным шрифтом, потом уровень компетенций и ниже комментарии и направления для развития.\n"
        f"По нижеприведенным данным о результатах выполнения тестов по разным темам сгенерируй профиль компетенций: \n" + statistic)
    f"Если тебе присылают текст, не соответствующий формату: question,theme,user_answer,true_answer и текст не содержит информации о прохождении тестов пользователя, то не генерируй профиль, а сообщи об этом пользователю.\n"
    return preprocess_text(ai_answer.alternatives[0].text)


def generate_theme_blocks(text: str, temp=0.5):
    global model
    model = model.configure(temperature=temp)
    ai_answer = model.run(
        f"Ты - AI-репетитор. \n"
        f"Формат: JSON, где каждая тема - ключ, а текст к нему - значение."
        f"По нижеприведенному тексту сгенерируй четкий формат данных, разделяя каждую тему и добавляя к ней текст строго по документу. Текст:\n" + text)
    return ai_answer.alternatives[0].text


def generate_task(profile_comp: str, material: str, temp=0.5):
    global model
    model = model.configure(temperature=temp)
    print("profile_comp", profile_comp)
    ai_answer = model.run(
        f"Ты - AI-репетитор. Сгенерируй тест по слабым местам студента, учитывая его профиль компетенций, который я тебе пришлю ниже.\n"
        f"Профиль компетенций студента: {profile_comp}\n Материал: {material}'. Задача должна быть уникальной и проверять понимание ключевых концепций. "
        f"Количество вопросов: 5, где 70% сфокусированы на слабых местах студента, а остальные по сильным. "
        f"Уровень сложности - в зависимости от уровня знаний в той или иной области студента. Предоставь также эталонное решение для проверки. Ответ пришли в формате 'Вопросы для студента' жирным шрифтом, и 'Ответы на вопросы:' жирным шрифтом (можно добавить смайлики строго по тематике в заголовки). Все должно быть оформлено красиво и лаконично. ФОРМАТИРОВАНИЕ СТРОГО В HTML, ИСПОЛЬЗУЯ ТОЛЬКО ТЕГ <b>. НЕ УКАЗЫВАЙ В НАЧАЛЕ ``` И НЕ ПИШИ ЧТО ЗА ТИП ДОКУМЕНТА. Так же предоставь небольшой конспект по темам вопросов.")
    return preprocess_text(ai_answer.alternatives[0].text)
