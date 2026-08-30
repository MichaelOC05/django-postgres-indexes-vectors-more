FROM postgres:17

# Install pgvector's files into the image. This is the "install" layer —
# it puts the extension's files on the server so CREATE EXTENSION can find them.
# Add more apt-packaged extensions to this same line as you adopt them.
RUN apt-get update \
    && apt-get install -y --no-install-recommends postgresql-17-pgvector \
    && rm -rf /var/lib/apt/lists/*