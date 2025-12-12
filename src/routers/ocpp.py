from fastapi import APIRouter, Depends, WebSocket
from sqlmodel import Session

from ..db import get_db
from ..ocpp.charge_point import ChargePoint
from ..utils.websocket_interface import WebSocketInterface

ocpp_router = APIRouter(tags=["ocpp"])


@ocpp_router.websocket("/ocpp/{charge_point_id}")
async def ocpp(
    websocket: WebSocket, charge_point_id: str, session: Session = Depends(get_db)
):
    await websocket.accept(subprotocol="ocpp2.0.1")

    interface = WebSocketInterface(websocket)
    cp = ChargePoint(id=charge_point_id, connection=interface, session=session)
    await cp.start()
