
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    HF_HOME=/home/user/.cache/huggingface \
    PORT=7860

RUN useradd -m -u 1000 user

# Create the model cache and give ownership to the non-root user
RUN mkdir -p /home/user/.cache/huggingface && \
    chown -R user:user /home/user/.cache

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir torch==2.6.0 --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

COPY --chown=user:user . .

USER user

EXPOSE 7860

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-7860}"]
