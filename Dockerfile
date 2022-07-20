FROM python

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "-m", "main.py"]
