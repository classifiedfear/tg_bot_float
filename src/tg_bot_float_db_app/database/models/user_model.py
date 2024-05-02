import datetime

from sqlalchemy import VARCHAR, Date, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from tg_bot_float_db_app.database.models.base import Base

class UserModel(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(
        BigInteger, unique=True, nullable=False, primary_key=True
    )
    username: Mapped[VARCHAR] = mapped_column(
        VARCHAR(32), unique=False, nullable=True
    )
    full_name: Mapped[VARCHAR] = mapped_column(
        VARCHAR(100), unique=False, nullable=True
    )
    reg_date: Mapped[Date] = mapped_column(Date, default=datetime.date.today())

    def __repr__(self) -> str:
        return (f'{self.username}: '
                f'reg_day:{self.reg_date}; '
                f'id-{self.id} ')