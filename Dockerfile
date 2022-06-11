FROM python:3.9-alpine

RUN apk add gcc python3-dev musl-dev

RUN mkdir /code

COPY ./app /code/app
COPY ./requirements.txt /code/requirements.txt

WORKDIR /code

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--port", "8000"]

RUN adduser -D user
USER user
