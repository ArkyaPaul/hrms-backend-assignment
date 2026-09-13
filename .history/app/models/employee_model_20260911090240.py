from sqlalchemy import Column # type: ignore
from sqlalchemy import Integer # type: ignore
from sqlalchemy import String # type: ignore
from sqlalchemy import Float # type: ignore
from sqlalchemy import Date # type: ignore
from sqlalchemy import Boolean # type: ignore

from app.database import Base


class Employee(Base):

    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    employee_id = Column(
        String,
        unique=True,
        nullable=False
    )

    name = Column(String, nullable=False)

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    department = Column(String)

    designation = Column(String)

    joining_date = Column(Date)

    base_salary = Column(Float)

    salary_type = Column(String)

    is_active = Column(
        Boolean,
        default=True
    )