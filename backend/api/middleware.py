from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


def add_cors(app: FastAPI, frontend_url: str | None = None) -> None:
    origins = [frontend_url] if frontend_url else [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


