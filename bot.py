import asyncio
import logging

from aiogram import Bot, Dispatcher

from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers
from config_data.set_menu import set_main_menu

# Инцилизация логгера
logger = logging.getLogger(__name__)


# Функция конфигурации и запуска бота
async def main():
    # Конфигурируем логгирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг
    config: Config = load_config()

    # Инцилизируем бота и диспетчера
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    # Настраиваем кнопку Menu
    await set_main_menu(bot=bot)

    # Регистрируем роутер и диспетчер
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
