FROM python:3.8-alpine3.12
WORKDIR /app
COPY ./app.py .
COPY ./requirements.txt .
RUN pip install -r requirements.txt
ENTRYPOINT [ "python3" ]
CMD ["app.py"]
