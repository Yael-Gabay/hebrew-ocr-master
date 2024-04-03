From seriallab/python3.6dev

COPY requirements.txt /opt/requirements.txt

RUN pip install -r /opt/requirements.txt

WORKDIR opt

COPY . /opt/

EXPOSE 8010

RUN pip install uvicorn fastapi pytesseract

CMD ["uvicorn", "model-api:app", "--host", "0.0.0.0", "--port", "8010"]

