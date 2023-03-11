# imports for yolo
import base64
import numpy as np
from PIL import Image
import io
import cv2
from bs4 import BeautifulSoup
import math

import os
from paddleocr import PaddleOCR,PPStructure,draw_structure_result,save_structure_res

os.environ["KMP_DUPLICATE_LIB_OK"]="True"

# Import for blur check


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

def get_table():
  table_engine = PPStructure(layout=False,lang='en',show_log=True)

  save_folder = './output'
  img_path = 'table4.png'
  img = cv2.imread(img_path)
  result = table_engine(img)
  save_structure_res(result, save_folder,os.path.basename(img_path).split('.')[0])

  img = []
  for line in result:
      img = line.pop('img')

  
  print(len(result[0]["res"]["cell_bbox"]))
  soup = BeautifulSoup(result[0]["res"]["html"], 'html.parser')

  table = soup.find('table')
  rows = table.find_all('tr')

  bbox = result[0]["res"]["cell_bbox"]

  for x in bbox:
     x[2] -= x[0]
     x[3] -= x[1]
  
  data = []
  for i in range(len(rows)):
      row = rows[i]
      cols = row.find_all('td')
      cols = { "key_type": "", "description": cols[0].text.strip(), "value": cols[1].text.strip(), "bboxKey": bbox[2*i], "bboxValue": bbox[2*i + 1]}
      data.append(cols)

  # print(len(data))

  # for x in data:
  #   xmin = math.ceil(x["bboxKey"][0])
  #   xmax = math.ceil(xmin + x["bboxKey"][2])
  #   ymin = math.ceil(x["bboxKey"][1])
  #   ymax = math.ceil(ymin + x["bboxKey"][3])
  #   cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)
  #   cv2.putText(img, x["description"] , (xmin, ymin),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

# Draw the rectangle on the image

  # Display the image with the rectangle
  # cv2.imshow('image', img)
  # cv2.waitKey(0)
  # cv2.destroyAllWindows()
  
  return data