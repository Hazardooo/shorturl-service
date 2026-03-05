import uuid
from sqlalchemy import Column, UUID, String, Integer
from src.database import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_url = Column(String, nullable=False)
    short_id = Column(String(20), unique=True, nullable=False, index=True)

    clicks = Column(Integer, default=0)

    def __repr__(self) -> str:
        return f"<URL(short_id='{self.short_id}', clicks={self.clicks})>"
