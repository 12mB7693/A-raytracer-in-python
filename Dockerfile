FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.9.9 /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# only for tests locally
# COPY docker-build/. .

COPY pyproject.toml uv.lock .
COPY src/. src/.

RUN uv sync --no-dev
ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "-m", "src.raytracer.main"]
