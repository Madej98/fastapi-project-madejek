import io
import pathlib
from datetime import datetime
from fastapi.templating import Jinja2Templates
import PIL.ImageOps
import pyprimes
import uvicorn
from PIL import Image
from fastapi import FastAPI, File, UploadFile, Response
from fastapi.security.api_key import APIKeyHeader
from starlette.responses import RedirectResponse, StreamingResponse

BASE_DIR = pathlib.Path(__file__).parent

API_KEY = "aksr134xk23xmkiop"
start = datetime.now()
app = FastAPI()
templates = Jinja2Templates(directory= BASE_DIR/"templates")

@app.get("/")
async def home():
    return Response(content="<h2>Hello! To see endpoints "
                            "<a href=\"http://localhost:8000/docs\">"
                            "click here<a></h2>", media_type="text/html")
    # return Response(content="<h2>Witaj, lista dostępnych endpointów jest tutaj: "
    #                         "<a href=\"https://fastapi-project-madejek.herokuapp.com/docs\">"
    #                         "https://fastapi-project-madejek.herokuapp.com/docs/<a></h2>", media_type="text/html")


@app.get("/prime/{number}")
async def prime(number: int):
    numberRange = range(0,9223372036854775807,1)
    if number in numberRange:
        if pyprimes.isprime(number) == 1:
            return (f'Liczba {number} jest pierwsza')
        elif pyprimes.isprime(number) != 1 or number==0 or number==1:
            return (f'Liczba {number} nie jest pierwsza.')
    else:
        return (f'Liczba {number} jest spoza zakresu')


@app.post("/picture/invert")
async def uploadImageToInvert(file: UploadFile = File()):
    im = Image.open(file.file)
    # im = im.convert("RGB")
    im_io = PIL.ImageOps.invert(im)
    im_response = io.BytesIO()
    im_io.save(im_response, "JPEG")
    im_response.seek(0)
    return StreamingResponse(im_response, media_type="image/jpeg")


@app.get("/show-time")
async def showTime(password=None):
    password = str(password)
    if password == API_KEY:
        datetime = start
        currentTime = start.strftime("%H:%M:%S")
        return {"Time": currentTime}
    else:
        return {"Niepoprawne hasło"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
