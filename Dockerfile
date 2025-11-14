FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY app.py .
RUN pip install --no-cache-dir discord.py plexapi
CMD ["python", "-u", "app.py"]
