FROM python:3.8-alpine3.12
WORKDIR /app
COPY ./requirements.txt .
RUN apk get update \
    && apk add --no-cache git \
    && apk add --no-cache docker \
    && apk add docker-compose 
RUN pip install -r requirements.txt
COPY ./application.py .
ENTRYPOINT [ "python3" ]
CMD ["application.py"]
