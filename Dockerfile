FROM python:3.11-slim-buster

WORKDIR /app

COPY . /app

RUN apt-get update
RUN apt-get -y install vim
RUN pip install --no-cache-dir -r ./requirements.txt

EXPOSE 80
EXPOSE 443
EXPOSE 8000
EXPOSE 8001


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

