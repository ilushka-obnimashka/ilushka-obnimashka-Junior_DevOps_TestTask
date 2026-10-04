"""Demo logic: no hiring decisions or messages are stored or sent."""

import secrets

from app.schemas import MatchResponse

MESSAGES = (
    "Это знак. Возможно, нам стоит поработать вместе.💙",
    "Кнопка работает.",
    "Она реально работает",
    "Ищу работу",
    "Возьмите меня на работу. Пасхалку вы уже нашли ;)",
)


def create_demo_match() -> MatchResponse:
    return MatchResponse(
        matched=True,
        message="Вы ищете DevOps. Я ищу команду. Мы идеально подходим друг-другу",
    )


def choose_notification() -> str:
    return secrets.choice(MESSAGES)
