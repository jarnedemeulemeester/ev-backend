from ..utils.singleton import singleton
from .base import Settings


@singleton
class FastApiConfig(Settings):
    origin: str

    class Config:
        env_prefix = "fastapi_"
