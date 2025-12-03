from uuid import uuid4
from sqlalchemy import BigInteger, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from models.db.Base import Base


class UserException(Base):
    __tablename__ = 'user_exeptions'

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[int] = mapped_column(BigInteger())
    exeptions = mapped_column(Text())
