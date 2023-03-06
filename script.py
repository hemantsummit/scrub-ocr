# imports for yolo
import base64
import numpy as np
from PIL import Image
import io

import os
from paddleocr import PaddleOCR
os.environ["KMP_DUPLICATE_LIB_OK"]="True"

# Import for blur check
import cv2


ocr = PaddleOCR(use_angle_cls=True, lang='en')

def converB64tofile(b64):
  b64 = b64.split(',')[1]
  image = Image.open(io.BytesIO(base64.b64decode(b64)))
  image.save("abc.png")
  
  return "abc.png"

def get_ocr_result(image_path):
  result = ocr.ocr(image_path, cls=True)
  results_dict = []

  for text in result[0]:
    top = max(text[0][0][1],text[0][1][1],text[0][2][1],text[0][3][1])
    bottom = min(text[0][0][1],text[0][1][1],text[0][2][1],text[0][3][1])
    left = min(text[0][0][0],text[0][1][0],text[0][2][0],text[0][3][0])
    right = max(text[0][0][0],text[0][1][0],text[0][2][0],text[0][3][0])
    results_dict.append({
        'word':text[1][0],
        'bounding_box':[left, top, right, bottom]
    })
  return results_dict

  if(len(ocr_result)==0):
   ocr_result =get_ocr_result()
  print(ocr_result)
  return predict_document_image(image_path, model, processor, ocr_result)

def get_scrub_data(image):
  # x = image.split(",")
  flag = False
  final_result = ""
  
  result = get_ocr_result(image)

  for value in result:
    if (flag == False):
        flag = True
        final_result += " "
    final_result += value["word"]

  return final_result