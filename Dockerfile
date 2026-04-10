FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set up a non-root user for Hugging Face
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:${PATH}"

# Ensure absolute imports work by adding /app to PYTHONPATH
ENV PYTHONPATH=/app

WORKDIR /app

# Copy and install dependencies
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY --chown=user . .

# Expose the port Hugging Face expects
EXPOSE 7860

# Run the OpenEnv server using standard uvicorn deployment
# This is more robust for Hugging Face than a main() script
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860", "--proxy-headers"]