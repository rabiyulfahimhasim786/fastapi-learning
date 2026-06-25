from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app=FastAPI()

class Employees(BaseModel):
    id:int
    name:str
    department:str
    salary:int

employees=[]
@app.post("/employee")
def add_employee(employee:Employees):
    employees.append(employee)
    return {"message":"Employee is added"}


@app.get("/employee")
def get_employee():
    return employees


@app.get("/employee/department")
def get_employee_department(department:str):
    for employee in employees:
        if employee.department==department:
            return employee
    raise (404,"Employee not found")

@app.get("/employee/salary")
def get_salary_search(min_salary:int,max_salary:int):
    for employee in employees:
        if min_salary <= employee.salary <= max_salary:
            return employee
    raise (404,"Employee not found")

@app.get("/employee/{employee_id}")
def get_employee(employee_id: int):
    for employee in employees:
        if employee.id==employee_id:
            return employee
    raise (404,"Employee not found")


@app.get("/employee/{employee_id}")
def get_employee(employee_id: int):
    for employee in employees:
        if employee.id==employee_id:
            return employee
    raise (404,"Employee not found")

@app.put("/employee/{employee_id}")
def update_employee(employee_id:int,name:str,department:str,salary:int):
    for employee in employees:
        if employee.id==employee_id:
            employee.name=name
            employee.department=department
            employee.salary=salary
            return {"Message":"Updated"}
    raise HTTPException(404,"Employee is not found")

@app.delete("/employee/{employee_id}")
def delete_smployee(employee_id:int):
    for i, employee in enumerate(employees):
        if employee.id==employee_id:
            del employees[i]
            return {"Message":"Deleted"}
    raise HTTPException(404,"Employee is deleted")

