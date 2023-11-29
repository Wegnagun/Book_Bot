import os
import string
import sys

BOOK_PATH = 'book/book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}


def _get_last_index(
    text: str,
    puncts_indexs: list,
    last_punct_index: int
) -> int:
    """ Рекурсивно получаем индекс последнего символа пунктуации. """
    if (
        text[last_punct_index + 1] in string.punctuation
        or text[last_punct_index - 1] in string.punctuation
    ):
        puncts_indexs.pop()
        _get_last_index(text, puncts_indexs, puncts_indexs[-1])
    return puncts_indexs[-1]


def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    """
    Получаем срез страницы
    после получения индекса последнего символа пунктуации.
    """
    puncts_indexs = [
        i for i, ltr in enumerate(text[start:start+size])
        if ltr in string.punctuation and i < size + 1
    ]
    last_punct_index = _get_last_index(text, puncts_indexs, puncts_indexs[-1])
    result = text[start:start + last_punct_index + 1]
    return result, len(result)


# text = 'Раз. Два. Три. Четыре. Пять. Прием!'
# print(*_get_part_text(text, 5, 9), sep='\n')
text = 'Да? Вы точно уверены? Может быть, вам это показалось?.. Ну, хорошо, приходите завтра, тогда и посмотрим, что можно сделать. И никаких возражений! Завтра, значит, завтра!'
print(*_get_part_text(text, 0, 54), sep='\n')
# Да? Вы точно уверены? Может быть,
# 33

def prepare_book(path: str) -> None:
    pass


prepare_book(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))
