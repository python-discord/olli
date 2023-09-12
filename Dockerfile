FROM --platform=linux/amd64 ghcr.io/owl-corp/python-poetry-base:3.11-slim

# Set SHA build argument
ARG git_sha="development"
ENV GIT_SHA=$git_sha

# Install dependencies and lockfile, excluding development dependencies
WORKDIR /olli
COPY pyproject.toml poetry.lock /olli/
RUN poetry install --without dev

# Copy the rest of the project code
COPY . .

# Start Olli
ENTRYPOINT ["poetry"]
CMD ["run", "python", "-m", "olli"]
