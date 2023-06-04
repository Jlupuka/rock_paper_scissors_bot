from random import choice

from lexicon.lexicon_ru import LEXICON_RU


# Функция возвращает случайный выбор бота в игре
def get_bot_choice() -> str:
    return choice(['rock', 'paper', 'scissors'])


# Функция, возвращающая ключ из словаря, по которому хранится значение,
#  передаваемое как аргумент - выбор пользователя
def _normalize_user_answer(user_answer: str) -> str:
    for key in LEXICON_RU:
        if LEXICON_RU[key] == user_answer:
            return key
    raise Exception


# Функция, определяющая победителя
def get_winner(user_choice: str, bot_choice: str) -> str:
    user_choice: str | Exception = _normalize_user_answer(user_choice)
    rules: dict[str: str] = {'rock': 'scissors',
                             'scissors': 'paper',
                             'paper': 'rock'}

    if bot_choice == user_choice:
        return 'nobody_won'
    elif rules[user_choice] == bot_choice:
        return 'user_won'
    return 'bot_won'
