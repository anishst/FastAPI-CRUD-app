import fastapi
from fastapi import Request
import httpx
from models.location import Location
from models.umbrella_status import UmbrellaStatus
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = fastapi.APIRouter()

templates = Jinja2Templates(directory="templates")

@router.post("/index.html", response_class=HTMLResponse)
async def weather_status(request:Request, boroughs_name: str = fastapi.Form(...)):
    url = f"https://weather.talkpython.fm/api/weather?city={boroughs_name}&country=us&state=ny&units=metric"
    # if location.state:
    #     url += f"&state={location.state}:
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()

        data = resp.json()
    weather = data.get('weather', {})
    description = weather.get('description', 'UNKNOWN')
    category = weather.get('category','UNKNOWN')
    forecast = data.get('forecast', {})
    temp = forecast.get('temp', 0.0)
    location = data.get('location',{})
    boroughs = location.get('city',{})
    bring = category.lower().strip() == 'rain'

    umbrella = UmbrellaStatus(bring_umbrella=bring, temp=temp, weather=category, city=boroughs, description=description)
    return templates.TemplateResponse("status.html", {"request":request, "status":umbrella})