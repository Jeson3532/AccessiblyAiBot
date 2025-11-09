import re


def check_html_tags(text: str) -> bool:
    """
    Проверяет, что все HTML-теги закрыты корректно.
    Работает с простыми тегами <b>, <i>, <u> и т.д.
    """
    # Находим все открывающие и закрывающие теги
    tags = re.findall(r'<(/?)([a-zA-Z0-9]+)>', text)
    stack = []

    for slash, tag_name in tags:
        if slash == '':
            # открывающий тег
            stack.append(tag_name)
        else:
            # закрывающий тег
            if not stack or stack[-1] != tag_name:
                return False
            stack.pop()

    return len(stack) == 0


def remove_html_tags(text: str) -> str:
    """
    Удаляет все HTML-теги из текста.
    """
    clean_text = re.sub(r'<[^>]+>', '', text)
    return clean_text
