# Stage 1: Install dependencies using uv
FROM python:3.12-slim-bookworm AS builder
COPY --from=ghcr.io/astral-sh/uv:0.5.5 /uv /uvx /bin/

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . .

# Install dependencies
RUN uv sync

# Expose the port your app runs on
EXPOSE 8000

# Run the Django application
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

