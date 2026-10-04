"""Response contracts shared by the API and its documentation."""

from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"


class MatchResponse(BaseModel):
    matched: bool
    message: str


class NotificationResponse(BaseModel):
    message: str
