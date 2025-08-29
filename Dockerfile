# Use a valid Python 3.12 slim image
FROM python:3.12-slim-bookworm

# Workdir
WORKDIR /app

# Install Python deps first to leverage layering
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY templates ./templates
COPY static ./static
COPY app.py .

# Expose and run
EXPOSE 5000
CMD ["python", "app.py"]
