from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, String, text
from sqlalchemy.orm import relationship

from app.database import Base

class SessionLog(Base):
    __tablename__ = "session_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    

    login_time = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()")
    )

    logout_time = Column(
        TIMESTAMP(timezone=True),
        nullable=True
    )

    last_seen = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()")
    )

    status = Column(
        String,
        nullable=False,
        server_default="ACTIVE"
    )
