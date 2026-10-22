# Project 14 — Container Engineering \& AWS

## Overview

Containerize a Python Flask application, run it locally with Docker Compose, and publish the image to Amazon Elastic Container Registry (Amazon ECR).

## Stack

Python 3.12 · Flask 3.1.2 · Docker · Docker Compose · AWS CLI · Amazon ECR

## Endpoints

* `http://localhost:8000/` — returns project information as JSON.
* `http://localhost:8000/health` — returns `{"status":"healthy"}` with HTTP 200.

## Project structure

```text
01 - project/
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── docker-compose.yml
02 - documentation/
03 - screenshots/
04 - AWS/
```

## Run locally

Run from the `01 - project` directory in PowerShell:

```powershell
docker compose up -d --build
docker compose ps
Invoke-RestMethod http://localhost:8000/
Invoke-RestMethod http://localhost:8000/health
docker compose logs --tail 50 web
```

Stop the Compose service with `docker compose down`.

## What the Dockerfile does

* `FROM python:3.12-slim` selects the base image.
* `WORKDIR /app` sets the working directory.
* Copies `requirements.txt` and installs Flask.
* Copies `app.py`.
* `EXPOSE 8000` documents the app port; it does not publish the host port by itself.
* `CMD` starts the Python app.

Compose config uses service `web`, image `project14-webapp:1.0`, container name `project14-app`, port mapping `8000:8000`, and restart policy `unless-stopped`.

## Amazon ECR

* Account: `<ACCOUNT\_ID>` (redacted — replace with your own 12-digit AWS account ID)
* Region: `us-east-1` (US East — N. Virginia)
* Repository: `project14-webapp`
* Tag: `1.0`
* Image URI: `<ACCOUNT\_ID>.dkr.ecr.us-east-1.amazonaws.com/project14-webapp:1.0`
* Verified image digest: `sha256:577447e05391ae29420bb68d531f9561c072b8996040abc12157e3d678cb3ae4`

### Authenticate, tag, and push

```powershell
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT\_ID>.dkr.ecr.us-east-1.amazonaws.com

docker tag project14-webapp:1.0 <ACCOUNT\_ID>.dkr.ecr.us-east-1.amazonaws.com/project14-webapp:1.0

docker push <ACCOUNT\_ID>.dkr.ecr.us-east-1.amazonaws.com/project14-webapp:1.0
```

### Verify

```powershell
aws ecr describe-images --repository-name project14-webapp --region us-east-1
```

The response also contained an untagged OCI attestation manifest. A table query that assumes every entry has a tag may therefore fail; inspect JSON or filter for tag `1.0` first.

## Validation checklist

* \[x] Flask app and endpoints tested
* \[x] Docker image built
* \[x] Container running
* \[x] Docker Compose configured and validated
* \[x] ECR repository created
* \[x] Image tagged, pushed, and verified
* \[x] Seven screenshots captured

## Notes

The app currently uses Flask's built-in development server. Before a production deployment, switch to a production WSGI server such as Gunicorn and rebuild the image. Lesson learned: this project was run with the AWS account root identity, which is not best practice. Routine work should use a least-privilege IAM identity, with MFA protecting root.

ECR storage may incur charges. Project 15 will build on this image and explore Amazon ECS with AWS Fargate; review resource costs before deploying.

