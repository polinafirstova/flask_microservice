FROM python:3.9.21

WORKDIR /app

COPY requirements.txt .

COPY . .

RUN python3 -m venv venv

ENV VIRTUAL_ENV=/app/venv
ENV PATH="/app/venv/bin:$PATH"

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "app.py"]
