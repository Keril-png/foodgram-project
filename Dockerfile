FROM python:3.8.5  
  
WORKDIR /code  
COPY . . 
RUN pip install -r requirements.txt  
CMD python /code/foodster/manage.py runserver 0:8000