FROM python:3.6

EXPOSE 5000

WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt
RUN chmod +x start.sh
CMD python app.py
#ENTRYPOINT ["./start.sh"]
