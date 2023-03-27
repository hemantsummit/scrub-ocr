# base image  
FROM python:3.9-slim
ENV PATH="/usr/local/cuda/bin:${PATH}"
ENV LD_LIBRARY_PATH="/usr/local/cuda/lib64:${LD_LIBRARY_PATH}"
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
# setup environment variable  
ENV DockerHOME=/paddleocr  
# set work directory  
RUN mkdir -p $DockerHOME  
# where your code lives  
WORKDIR $DockerHOME  
# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  
# install dependencies  
RUN pip install --upgrade pip  
# copy whole project to your docker home directory. 
COPY . $DockerHOME  

# run this command to install all dependencies  
RUN pip install -r requirements.txt  
# port where the Django app runs  
EXPOSE 5000  
# start server  
# Start the application server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]