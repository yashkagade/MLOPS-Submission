# Stage 1: Build dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --user -r requirements.txt

# Stage 2: Final image
FROM python:3.11-slim

ENV PATH=/root/.local/bin:$PATH

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY app.py .

# Expose Streamlit default port
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
