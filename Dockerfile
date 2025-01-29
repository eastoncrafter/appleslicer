# Use the slim Python image as a base
FROM python:3.13.1-bullseye

# Set environment variables to reduce interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install Python dependencies
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Set permissions if needed for binaries or scripts
RUN chmod +x /app/prusaslicer/prusa-slicer

# Expose the port your Flask app runs on
EXPOSE 5000

# Set the command to run the Flask app or handle custom commands
CMD ["flask", "run", "--host=0.0.0.0"]
