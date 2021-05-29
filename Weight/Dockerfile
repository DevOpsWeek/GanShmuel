FROM python:3.8-slim-buster
#RUN python -m pip install --upgrade pip
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
#RUN chmod 744 app.py
#RUN export PATH=app.py:$PATH
ENV FLASK_APP=app.py
CMD [ "flask", "run", "--debugger" ]
#CMD [ "python3", "-m" ]
#ENTRYPOINT [ "app.py" ]
