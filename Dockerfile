FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV NODE_MAJOR=22

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    gnupg \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_${NODE_MAJOR}.x | bash - \
    && apt-get install -y nodejs

# Create app directory
WORKDIR /app

# Copy package files
COPY package*.json ./
COPY adhd_research_api/requirements.txt ./adhd_research_api/

# Install Node.js dependencies
RUN npm ci --only=production

# Install Python dependencies
RUN pip install --no-cache-dir -r adhd_research_api/requirements.txt

# Copy application code
COPY . .

# Generate Prisma client
RUN npx prisma generate

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Expose port
EXPOSE 5000

# Start command
CMD ["python", "adhd_research_api/src/main.py"]

