FROM python:3.8-alpine3.12
WORKDIR /app
COPY ./application.py .
COPY ./requirements.txt .
COPY ./script.sh .
RUN pip install -r requirements.txt \
    && pip install GitPython \
    && chmod u+rx script.sh 
RUN apk update \
    && apk add git
ENTRYPOINT [ "python3" ]
CMD ["application.py"]
