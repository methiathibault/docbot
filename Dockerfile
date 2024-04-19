# image python
FROM python:3.11.9

RUN mkdir code
WORKDIR /code

ADD requirements.txt /code/
ADD src/* /code/


RUN pip install -r requirements.txt

CMD [ "uvicorn","main:app","--host=0.0.0.0" ]