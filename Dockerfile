# Dockerfile
# Author: Karina Solis
# Resource: https://docs.streamlit.io/deploy/tutorials/docker

FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8501


ENTRYPOINT ["streamlit", "run", "src/app.py", "--server.port=8501"]