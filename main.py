from fastapi import FastAPI
import uvicorn
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.api.user import user_router
from app.api.login import login_router
from app.api.company import company_router
from app.api.employee import employee_router
from app.api.process import proccess_router
from app.api.process_employee import process_employees_router
from app.api.company_user import company_user_router

app = FastAPI(title="Blackngine")
app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)


app_router = APIRouter()

app_router.include_router(user_router, prefix="/users", tags=['users'])
app_router.include_router(login_router, prefix="/login", tags=['login'])
app_router.include_router(company_router, prefix="/companies", tags=['companies'])
app_router.include_router(employee_router, prefix="/employees", tags=['employees'])
app_router.include_router(proccess_router, prefix="/proccesses", tags=['proccesses'])
app_router.include_router(process_employees_router, prefix="/process_employees", tags=['process_employees'])
app_router.include_router(company_user_router, prefix="/company_useres", tags=['company_useres'])
app.include_router(app_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)