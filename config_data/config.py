from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class DataBaseConfig:
    dbname: str
    user: str
    password: str
    host: str
    port: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DataBaseConfig


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path=path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')),
                  db=DataBaseConfig(dbname=env('dbname'), user=env('user'), password=env('password'), host=env('host'),
                                    port=env('port')))
