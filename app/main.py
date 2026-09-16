from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.llm import MODEL, explain

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

app = FastAPI(title="Explainer App")


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ExplainRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=2000)
    history: list[Message] = []


class ExplainResponse(BaseModel):
    answer: str
    model: str


@app.post("/api/explain", response_model=ExplainResponse)
def explain_topic(req: ExplainRequest) -> ExplainResponse:
    try:
        answer = explain(req.topic, [m.model_dump() for m in req.history])
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return ExplainResponse(answer=answer, model=MODEL)


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
