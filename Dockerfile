FROM python:3.7-alpine3.8
WORKDIR /code
ENV FLASK_APP routes.py
ENV FLASK_RUN_HOST 0.0.0.0

RUN apk add --update --no-cache g++ gcc

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN python download_punkt.py
CMD ["flask", "run"]
