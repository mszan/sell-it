FROM python:3.8-bookworm
WORKDIR /app
COPY ../source/requirements.txt .
RUN pip install -r requirements.txt
COPY ./source .