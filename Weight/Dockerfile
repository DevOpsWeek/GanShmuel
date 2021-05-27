FROM python:3.8-slim-buster
RUN python -m pip3 install --upgrade pip3
RUN pip install sentry-sdk[flask]
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]