FROM python:3.13-slim

WORKDIR /app

# Install dependencies first so this layer only invalidates when req.txt changes.
COPY req.txt .
RUN pip install --no-cache-dir -r req.txt

COPY src/ src/

RUN printf '#!/usr/bin/env bash\nexec python /app/src/main.py "$@"\n' > /usr/local/bin/mosfet \
    && chmod +x /usr/local/bin/mosfet

RUN useradd --create-home --shell /usr/sbin/nologin mosfet \
    && chown -R mosfet:mosfet /app
USER mosfet

ENV PYTHONUNBUFFERED=1

# Idles by default. Nothing runs until you exec in and invoke `mosfet` yourself (e.g. `docker exec -it <container> mosfet`), same as the installed app does nothing until you run `mosfet`.
ENTRYPOINT ["sleep", "infinity"]