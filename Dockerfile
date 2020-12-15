FROM python:3.8.0-buster

#make work directory in docker container
WORKDIR /app

#install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

#copy source code
COPY /app .

#run app
CMD ["python", "routes.py"]