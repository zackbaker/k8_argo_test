FROM python:3.7
WORKDIR /src/
COPY ./python .
RUN pip install -r requirements.txt