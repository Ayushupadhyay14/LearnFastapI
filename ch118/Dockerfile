FROM python:3.13.5

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /ch118

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /ch118/

CMD ["sleep", "infinity"]

