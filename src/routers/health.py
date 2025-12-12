from fastapi import APIRouter, Response

health_router = APIRouter(tags=["health"])


@health_router.get("/health")
async def health():
    return Response(status_code=200)
