FROM python:3.9.1

WORKDIR /parsing

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY umweltreport_laender.xlsx umweltreport_laender.xlsx 

CMD ["python3", "main.py"] 