from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config.fastapi import FastApiConfig
from .db import db
from .routers.health import health_router
from .routers.ocpp import ocpp_router

fastapi_config = FastApiConfig()


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.create_db_and_tables()
    yield


app = FastAPI(title="EV", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[fastapi_config.origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(ocpp_router)
