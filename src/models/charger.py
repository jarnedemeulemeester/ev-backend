from sqlmodel import Field, SQLModel


class Charger(SQLModel, table=True):
    serial_number: str = Field(primary_key=True)
    password_salt: str
