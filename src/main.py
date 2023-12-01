from fastapi import FastAPI
from src.employees.router import router as employee_router
from src.tasks.router import router as task_router


app = FastAPI(
    title='Task Tracker'
)

app.include_router(employee_router)
app.include_router(task_router)
