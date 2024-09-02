# Python base
FROM python:3.10.12

# Work Dir
WORKDIR /app

# Copy all
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 8000

# Start the uvicorn server
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]