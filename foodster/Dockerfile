FROM python:3.8.5  

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1


WORKDIR /code
COPY ./requirements.txt /code
COPY ./entrypoint.sh /code
RUN pip install -r /code/requirements.txt
COPY . /code


ENTRYPOINT ["/code/entrypoint.sh"]