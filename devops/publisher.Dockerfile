FROM python:3.10

WORKDIR /app

COPY src/publisher/* .

RUN pip install  --no-cache-dir -r  /app/requirements.txt

ENTRYPOINT ["python"]

CMD ["/app/publisher.py"]