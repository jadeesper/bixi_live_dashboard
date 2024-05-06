FROM python:3.9-slim-buster

# Update package lists and install required dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        nano \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ADD . /app

WORKDIR /app
COPY . .

COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir

# Specify the command to run the application
CMD ["python3","-m", "scripts.dashboard"]
# CMD ["python3","-m", "scripts.database_init"]
# CMD ["python3", "scripts/database_init2.py"]