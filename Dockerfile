# Use the official lightweight Python image.
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all files to working dir
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Setup Streamlit config to run on port 8080
RUN mkdir -p ~/.streamlit
RUN echo "\
[server]\n\
port = 8080\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
headless = true\n\
" > ~/.streamlit/config.toml

# Expose port 8080 (required by Cloud Run)
EXPOSE 8080

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.enableCORS=false"]

