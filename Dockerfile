# Use official Python image
FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Copy all files to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (if your app runs on a specific port like 5000 or 8000, update this)
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
