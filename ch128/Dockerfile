# Stage 1: Install deps
FROM python:3.11-slim AS builder
WORKDIR /ch128
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Final image
FROM python:3.11-slim
WORKDIR /ch128

# Copy installed packages
COPY --from=builder /root/.local /root/.local

# Copy project files
COPY . .

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
