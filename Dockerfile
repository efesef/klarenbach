FROM python:3.9.1

WORKDIR /app

ENV FLASK_APP=app.py

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["python3", "app.py"]