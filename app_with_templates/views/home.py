import fastapi
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import api.weather_api as weather_api

templates = Jinja2Templates("templates")

router = fastapi.APIRouter()


@router.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})