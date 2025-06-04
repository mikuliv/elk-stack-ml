# ELK Stack with Machine Learning API

This repository provides a Docker Compose configuration for running an ELK (Elasticsearch, Logstash, Kibana) stack together with a simple machine learning API. The ML API exposes a prediction endpoint built with FastAPI and can be consumed by Logstash or other clients.

## Requirements

- Docker
- Docker Compose (either `docker compose` or `docker-compose`)

## Configuration

The services require the `ELK_VERSION` environment variable to determine which Elastic images to pull. You can set it in your shell or place it in a `.env` file at the repository root.

```bash
# Example of setting the variable in your shell
export ELK_VERSION=8.10.2
```

Alternatively, copy `.env.example` to `.env` and adjust the value if needed.

## Running the stack

From the repository root run:

```bash
docker compose -f elk-stack/docker-compose.yml up
```

Docker Compose will start Elasticsearch, Kibana, Logstash and the `ml-api` service using the version specified in `ELK_VERSION`.

## Repository layout

- `elk-stack/` – Docker Compose file and service configurations.
- `elk-stack/ml-api` – FastAPI application exposing the prediction endpoint.
- `tests/` – basic tests for the ML API.

