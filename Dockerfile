# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.13.5
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Download dependencies as a separate step
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Copy the source code into the container.
COPY . .

# --- NEW LINE ADDED HERE ---
# Change ownership of the /app directory to appuser
# This ensures the appuser can write the SQLite database file.
RUN chown -R appuser:appuser /app

# Switch to the non-privileged user to run the application.
USER appuser

EXPOSE 8000

# Add migrations to the CMD (as discussed previously)
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000