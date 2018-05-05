# Use ubuntu as a parent image
FROM python

# Install python3.6 and pip and clean up the apt cache
# RUN apt-get update && apt-get install -y \
#     python3.6 \
#     python-pip python-dev build-essential \
#  && rm -rf /var/lib/apt/lists/*

# Still install pip
# RUN pip install --upgrade pip
# RUN pip install --upgrade virtualenv

# Set the working directory to /app
WORKDIR /usr/src/app

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make ports available to the world outside this container
EXPOSE 80
EXPOSE 9042
EXPOSE 9142
EXPOSE 9242
EXPOSE 7199
EXPOSE 9160
EXPOSE 8778
EXPOSE 4242
EXPOSE 8083
EXPOSE 3000
EXPOSE 9000

# Define environment variable


# Deploy the cassandra cluster first
# WORKDIR /usr/src/app
# RUN docker-compose up -d

# Run app.py when the container launches
WORKDIR /usr/src/app
CMD ["python", "./main.py"]
