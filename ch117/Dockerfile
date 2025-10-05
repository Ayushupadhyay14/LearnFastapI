FROM python:3.13.5

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /ch117

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# RUN pip install "fastapi[standard]"

COPY . /ch117/

CMD ["sleep", "infinity"]

# CMD ["fastapi", "dev", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

