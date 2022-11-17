FROM python:3.9.1

WORKDIR /app

ENV FLASK_APP=app.py

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY config.py config.py 
COPY . .

CMD ["python3", "app.py"] 