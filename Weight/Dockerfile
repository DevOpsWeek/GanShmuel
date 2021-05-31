FROM python:3.8
EXPOSE 5000
#RUN python -m pip install --upgrade pip
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
RUN chmod 777 entrypoint.sh
#RUN chmod 744 app.py
#RUN export PATH=app.py:$PATH
# ENV FLASK_APP=app.py
CMD ./entrypoint.sh
#CMD [ "python3", "-m" ]
#ENTRYPOINT [ "app.py" ]
