import base64
import requests

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    meteomatics_auth: str
    allowed_origins: list[str]


settings = Settings()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/weather/{time}/{params}/{location}")
async def get_weather(time, params, location):
    token = base64.b64encode(settings.meteomatics_auth.encode())
    response = requests.get(
        'https://login.meteomatics.com/api/v1/token',
        headers={
            'Authorization': f'Basic {token.decode('ASCII')}'
        }
    )
    access_token = response.json().get('access_token')

    uri = '/'.join([
        'https://api.meteomatics.com',
        time,
        params,
        location,
        'json'
    ])

    response = requests.get(uri, {'access_token': access_token})

    return response.json()
