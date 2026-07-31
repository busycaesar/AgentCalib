FROM python:3.13-slim

WORKDIR /app

# Install dependencies first so this layer only invalidates when req.txt changes.
COPY req.txt .
RUN pip install --no-cache-dir -r req.txt

COPY src/ src/

RUN useradd --create-home --shell /usr/sbin/nologin mosfet \
    && chown -R mosfet:mosfet /app
USER mosfet

ENV PYTHONUNBUFFERED=1

# mosfet.config.json and .env are runtime configuration/secrets, not part of
# the image — mount them in with `-v` / `--env-file` (see README).
#
# Defaults to CLI mode (main.py's default); pass `--discord` as an extra
# `docker run` argument to run the Discord bot instead.
ENTRYPOINT ["python", "src/main.py"]
