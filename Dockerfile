# Use a larger image for building
FROM python:3.12 as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --no-input

# Use a smaller image for deployment
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Copy necessary files from the builder stage
COPY --from=builder /app/staticfiles /app/staticfiles
COPY --from=builder /app/manage.py /app/manage.py
COPY --from=builder /app/studiohub /app/studiohub
COPY --from=builder /app/tracker /app/tracker
COPY --from=builder /app/requirements.txt /app/requirements.txt

# Install production dependencies
RUN pip install --no-cache-dir --only-binary -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "studiohub.wsgi:application", "--bind", "0.0.0.0:8000"]
