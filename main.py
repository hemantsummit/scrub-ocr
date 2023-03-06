from typing import Union
from fastapi import FastAPI, File, UploadFile
from typing import List
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from script import get_ocr_result, converB64tofile, get_scrub_data
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import io
import base64
from PIL import Image
origins = [
    "http://localhost",
    "http://localhost:3000",
    "*"
]



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {
        "Paddle" : "OCR"
    }

class ImageRequest(BaseModel):
    image_base64: str
    

@app.post("/scrub_ocr")
async def index(image_request: ImageRequest):
    # print(image_request.image_base64)
    # print(type(fileObject))

    # print(fileObject)
    fileObject = converB64tofile(image_request.image_base64)
    print(fileObject)
    # print(type(fileObject))
    data = get_scrub_data(fileObject)
    # print(data)
    # data = "OK"
    return data
