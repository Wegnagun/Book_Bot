from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


@dataclass
class Config:
    tg_bot: TgBot


def load_config() -> Config:
    return Config(tg_bot=TgBot(
        token=os.environ.get('TOKEN'),
        admin_ids=[int(id) for id in os.environ.get('ADMIN_IDS').split(',')]
    ))
