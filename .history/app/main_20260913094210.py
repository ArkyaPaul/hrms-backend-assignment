from fastapi import FastAPI # type: ignore

from app.database import Base
from app.database import engine

from app.models.user_model import User
from app.models.employee_model import Employee
from app.models.attendance_model import Attendance
from app.models.payroll_model import Payroll
from app.models.session_log import SessionLog

from app.routes.test_routes import router as test_router
from app.routes.auth_routes import router as auth_router
from app.routes.employee_routes import router as employee_router
from app.routes.attendance_routes import router as attendance_router
from app.routes.payroll_routes import router as payroll_router
from app.utils.exception_handler import global_exception_handler

app = FastAPI()

app.include_router(auth_router)
app.include_router(test_router)
app.include_router(employee_router)
app.include_router(attendance_router)
app.include_router(payroll_router)

app.add_exception_handler(
    Exception,
    global_exception_handler
)

@app.get("/")
def home():

    return {
        "message": "HRMS Backend Running"
    }
