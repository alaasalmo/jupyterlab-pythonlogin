# Use Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the Flask app to the container
COPY app.py /app
COPY requirements.txt /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app will run on
EXPOSE 5000

# Run the Flask app
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

#ENTRYPOINT ["tail"]
#CMD ["-f","/dev/null"]
