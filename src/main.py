from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config.fastapi import FastApiConfig
from .routers.health import health_router

fastapi_config = FastApiConfig()

app = FastAPI(
    title="Race API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[fastapi_config.origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
