from fastapi import APIRouter, WebSocket

from ..ocpp.charge_point import ChargePoint
from ..utils.websocket_interface import WebSocketInterface

ocpp_router = APIRouter(tags=["ocpp"])


@ocpp_router.websocket("/ocpp/{charge_point_id}")
async def ocpp(websocket: WebSocket, charge_point_id: str):
    await websocket.accept(subprotocol="ocpp2.0.1")

    interface = WebSocketInterface(websocket)
    cp = ChargePoint(charge_point_id, interface)
    await cp.start()
