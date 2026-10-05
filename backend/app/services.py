"""Demo logic: no hiring decisions or messages are stored or sent."""

import secrets

from app.schemas import MatchResponse

MESSAGES = (
    "Это знак. Возможно, нам стоит поработать вместе.💙",
    "Кнопка работает. Я тоже хочу работать с вами.💙",
    "Она реально работает. А я реально хочу работать с вами.💙",
    "Ищу работу. А вы ищете DevOps. Мы идеально подходим друг-другу.💙",
    "Пасхалку вы уже нашли ;)",
)


def create_demo_match() -> MatchResponse:
    return MatchResponse(
        matched=True,
        message="Вы ищете DevOps. Я ищу команду. Мы идеально подходим друг-другу 💙",
    )


def choose_notification() -> str:
    return secrets.choice(MESSAGES)
