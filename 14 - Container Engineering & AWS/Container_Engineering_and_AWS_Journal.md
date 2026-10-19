# Project 14 — Project Journal

## Goal
Containerize a Flask application, test it locally, and publish the image to Amazon ECR.

## Work completed
1. Created `app.py` with `/` and `/health` GET routes.
2. Pinned Flask `3.1.2` in `requirements.txt`.
3. Built a Docker image using `python:3.12-slim`, installing dependencies and copying the application.
4. Ran the container on port 8000 and tested both endpoints.
5. Configured Docker Compose with service `web`, image `project14-webapp:1.0`, container name `project14-app`, port mapping `8000:8000`, and restart policy `unless-stopped`.
6. Created ECR repository `project14-webapp` in `us-east-1`; image scanning on push was enabled and AES256 encryption selected.
7. Authenticated Docker to ECR, tagged the local image with the ECR URI, and pushed tag `1.0`.
8. Verified the image with `aws ecr describe-images`.

## Verified result
Image URI: `881027529328.dkr.ecr.us-east-1.amazonaws.com/project14-webapp:1.0`

Image digest: `sha256:577447e05391ae29420bb68d531f9561c072b8996040abc12157e3d678cb3ae4`

## Issue and lesson
An ECR table query failed because the response included an untagged OCI attestation manifest. The query assumed all image details had the same tag fields. The full JSON response confirmed the tagged image was present. Lesson: inspect API output and account for optional fields before formatting results.

The ECR Permissions tab displayed “No statements.” This did not mean the push failed; repository policies are separate from the IAM identity's permissions. A repository policy is not required merely to push an image within the same account when the identity is authorized.

## Evidence
Seven screenshots were captured. Screenshot 8 was omitted because it duplicated existing image-tag evidence.

## Outcome
The local container workflow and ECR publishing workflow are complete. The next step is Project 15: deploying the image with Amazon ECS and AWS Fargate.

## Cost reminder
Review AWS billing and clean up unused resources. Fargate tasks, load balancers, NAT gateways, public IPv4 addresses, and ECR image storage can incur charges.
