from fastapi import APIRouter # type: ignore
from fastapi import Depends # type: ignore
from fastapi import HTTPException # type: ignore
import random
from sqlalchemy.orm import Session # type: ignore

from app.dependencies import get_db

from app.models.employee_model import Employee

from app.models.user_model import User
from app.schemas.employee_schema import EmployeeCreate,EmployeeUpdate

from app.auth.rbac import role_required


router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)

@router.post("/")
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(
        role_required(["admin", "hr"])
    )
):

    user = db.query(User).filter(
        User.email == employee.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="No user found with this email"
        )

    existing_employee = db.query(Employee).filter(
        Employee.email == employee.email
    ).first()

    if existing_employee:

        raise HTTPException(
            status_code=400,
            detail="Employee already exists"
        )

    new_employee = Employee(
        # employee_id=employee.employee_id,
        name=employee.name,
        email=employee.email,
        department=employee.department,
        designation=employee.designation,
        joining_date=employee.joining_date,
        base_salary=employee.base_salary,
        salary_type=employee.salary_type
    )

    new_employee.employee_id = (f"{new_employee.department[:3].upper()}_{random.randint(1000, 9999)}")

    new_employee.user_id = user.id

    db.add(new_employee)

    db.commit()

    db.refresh(new_employee)

    return {
        "message": "Employee created successfully"
    }

@router.get("/{employee_id}")
def get_single_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(
        role_required(
            ["admin", "hr", "employee"]
        )
    )
):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee

@router.put("/{employee_id}")
def update_employee(
    employee_id: int,
    updated_data: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(
        role_required(["admin", "hr"])
    )
):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    update_dict = updated_data.dict(
        exclude_unset=True
    )

    for key, value in update_dict.items():

        setattr(employee, key, value)

    db.commit()

    db.refresh(employee)

    return {
        "message": "Employee updated successfully"
    }

@router.delete("/{employee_id}")
def deactivate_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(
        role_required(["admin"])
    )
):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    employee.is_active = False

    db.commit()

    return {
        "message": "Employee deactivated"
    }