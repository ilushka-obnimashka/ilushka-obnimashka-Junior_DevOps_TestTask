"""FastAPI application. Nginx serves the frontend independently."""

from fastapi import FastAPI, Response

from app.schemas import HealthResponse, MatchResponse, NotificationResponse
from app.services import choose_notification, create_demo_match

app = FastAPI(
    title="Jobmatch API",
    description="Демонстрационный API тестового задания Junior DevOps.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url=None,
    openapi_url="/api/openapi.json",
)


@app.get(
    "/health/",
    tags=["Состояние сервиса"],
    summary="Проверка доступности backend",
    description=(
        "Возвращает ответ, если приложение FastAPI может обработать запрос. " "ВАЖНО: Не проверяет frontend, nginx."
    ),
    response_description="Backend ответил: status равен ok.",
    response_model=HealthResponse,
    status_code=200,
)
def health(response: Response) -> HealthResponse:
    response.headers["Cache-Control"] = "no-store"
    return HealthResponse()


@app.get(
    "/api/match/",
    tags=["Знакомство"],
    summary="Получить демонстрационный мэтч",
    description=(
        "Используется при свайпе вправо или нажатии кнопки «В команду». "
        "Возвращает положительный результат и сообщение для экрана мэтча. "
    ),
    response_description="Результат демо-мэтча и текст для пользователя.",
    response_model=MatchResponse,
    status_code=200,
)
def match(response: Response) -> MatchResponse:
    response.headers["Cache-Control"] = "no-store"
    return create_demo_match()


@app.get(
    "/api/notification/",
    tags=["Знакомство"],
    summary="Получить случайную шуточную фразу",
    description=(
        "Выбирает одну фразу из заданного в приложении списка. "
        "При повторных запросах фразы могут совпадать. "
        "Возвращает текст; его показ на странице выполняет frontend."
    ),
    response_description="Случайная фраза в поле message.",
    response_model=NotificationResponse,
    status_code=200,
)
def notification(response: Response) -> NotificationResponse:
    response.headers["Cache-Control"] = "no-store"
    return NotificationResponse(message=choose_notification())
