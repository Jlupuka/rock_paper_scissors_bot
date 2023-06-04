from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message

from keyboards.keyboards import game_kb, yes_no_kb
from lexicon.lexicon_ru import LEXICON_RU
from services.services import get_bot_choice, get_winner
from database.database import DataBase


router: Router = Router()
db: DataBase = DataBase()


# Этот хендлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=yes_no_kb)


# Этот хендлер срабатывает на команду /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=yes_no_kb)


# Этот хендлер срабатывает на отказ пользователя играть в игру
@router.message(Text(text=[LEXICON_RU['no_button']]))
async def process_no_answer(message: Message):
    await message.answer(text=LEXICON_RU['no'])


# Этот хендлер срабатывает на согласие пользователя играть в игру
@router.message(Text(text=[LEXICON_RU['yes_button']]))
async def process_no_answer(message: Message):
    db.user(message.from_user.id)
    await message.answer(text=LEXICON_RU['yes'], reply_markup=game_kb)


# Этот хендел срабатывает на любую из игровых кнопок
@router.message(Text(text=[LEXICON_RU['rock'],
                           LEXICON_RU['paper'],
                           LEXICON_RU['scissors']]))
async def process_game_button(message: Message):
    db.add_game(message.from_user.id)
    bot_choice: str = get_bot_choice()
    await message.answer(text=f'{LEXICON_RU["bot_choice"]} - {LEXICON_RU[bot_choice]}')
    winner: str = get_winner(message.text, bot_choice)
    if winner == 'user_won':
        db.add_win(message.from_user.id)
    elif winner == 'bot_won':
        db.add_lose(message.from_user.id)
    await message.answer(text=LEXICON_RU[winner], reply_markup=yes_no_kb)


# Этот хендлер срабатывает на нажатие кнопки "Получить свою статистику"
@router.message(Text(text=[LEXICON_RU['get_info']]))
async def proces_information_user_button(message: Message):
    user_id: int = message.from_user.id
    db.user(user_id=user_id)
    count_wins: int = db.get_count_win(user_id=user_id)
    count_games: int = db.get_count_game(user_id=user_id)
    count_loses: int = db.get_count_lose(user_id=user_id)
    percent_wins: float = float(db.get_percent_user_win(user_id=user_id))
    count_draws: int = count_games - count_loses - count_wins
    text = LEXICON_RU['information_user'].format(count_wins, count_loses, count_draws, count_games, percent_wins)
    await message.answer(text=text, reply_markup=yes_no_kb)


# Этот хендлер будет срабатывать на команду очищения статистики пользователя
@router.message(Text(text=[LEXICON_RU['clear_info']]))
async def proces_clear_information_user(message: Message):
    db.user(message.from_user.id)
    db.clear_statistic(message.from_user.id)
    await message.answer(text=LEXICON_RU['clear_message'], reply_markup=yes_no_kb)
