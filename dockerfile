FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y python3-dev build-essential

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make sure the entrypoint is executable
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Set entrypoint
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["python", "app.py"]  # Replace with your actual command to run your app
