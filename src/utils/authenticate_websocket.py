# Source - https://stackoverflow.com/a
# Posted by Harry Z., modified by community. See post 'Timeline' for change history
# Retrieved 2025-12-12, License - CC BY-SA 4.0

import base64

from argon2 import PasswordHasher
from fastapi import WebSocket, status
from sqlmodel import Session, select

from ..models.charger import Charger


async def authenticate_websocket(websocket: WebSocket, session: Session):
    ph = PasswordHasher()
    auth_header = websocket.headers.get("Authorization")
    if not auth_header:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None

    try:
        scheme, credentials = auth_header.split()
        if scheme.lower() != "basic":
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return None

        decoded = base64.b64decode(credentials).decode("ascii")
        username, _, password = decoded.partition(":")
        stmt = select(Charger).where(Charger.serial_number == username)
        charger = session.exec(stmt).first()
        if not charger:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return None
        ph.verify(charger.password_salt, password)

        if not (ph.verify(charger.password_salt, password)):
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return None

        return username
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None
