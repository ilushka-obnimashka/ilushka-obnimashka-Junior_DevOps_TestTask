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


@app.get("/health/", response_model=HealthResponse, tags=["Health"])
def health(response: Response) -> HealthResponse:
    response.headers["Cache-Control"] = "no-store"
    return HealthResponse()


@app.get("/api/match/", response_model=MatchResponse, tags=["Demo"])
def match(response: Response) -> MatchResponse:
    """Return a stateless demo match without sending or saving anything."""
    response.headers["Cache-Control"] = "no-store"
    return create_demo_match()


@app.get(
    "/api/notification/",
    response_model=NotificationResponse,
    tags=["Знакомство"],
    summary="Получить случайную шуточную фразу",
    description=(
        "Вызывается кнопкой «Подкат от DevOps». Выбирает фразу из списка "
        "на backend и возвращает её для показа уведомления на frontend. "
        "Фразы могут повторяться. Данные не сохраняются."
    ),
    response_description="Текст уведомления в поле message.",
    status_code=200,
)
def notification(response: Response) -> NotificationResponse:
    response.headers["Cache-Control"] = "no-store"
    return NotificationResponse(message=choose_notification())
