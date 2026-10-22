# Project 14 — Learning Notes

## Image, container, registry

* **Image:** packaged application and runtime template.
* **Container:** running instance of an image.
* **Registry:** stores and distributes images; ECR is AWS's managed registry.

Local flow: source code → Docker image → running container.
Cloud flow: Docker image → ECR → deployment platform such as ECS/Fargate.

## Dockerfile concepts

* `FROM`: chooses the base image.
* `WORKDIR`: sets the working directory inside the image.
* `COPY`: copies files into the image.
* `RUN`: executes a command while building the image.
* `EXPOSE`: documents the intended container port; it does not publish a host port.
* `CMD`: sets the default process when the container starts.

Copying `requirements.txt` before `app.py` can help Docker reuse dependency-installation cache layers when application code changes.

## Ports and Compose

`8000:8000` means `HOST\_PORT:CONTAINER\_PORT`. A request to `localhost:8000` is forwarded to port 8000 in the container.

Useful commands, run from `01 - project`:

```powershell
docker compose up -d --build
docker compose ps
docker compose logs --tail 50 web
docker compose down
```

`up` starts services; `ps` shows state and port mapping; `logs` helps troubleshoot; `down` stops and removes Compose-managed containers/network, but does not delete an ECR repository.

## Health endpoint

`/health` returns HTTP 200 and `{"status":"healthy"}`. It is a basic response check, not a complete production readiness test.

## ECR image URI

`<ACCOUNT\_ID>.dkr.ecr.us-east-1.amazonaws.com/project14-webapp:1.0`

* `<ACCOUNT\_ID>`: AWS account ID.
* `us-east-1`: region.
* `project14-webapp`: repository.
* `1.0`: image tag.

Tags are readable labels; digests such as `sha256:...` identify image content more precisely.

## ECR query troubleshooting

The ECR response contained a tagged image and an untagged OCI attestation manifest. A table query failed because it expected every record to contain tag data. First inspect the full JSON response, then filter the relevant tagged record before formatting a table.

## IAM and repository policy

“No statements” on the repository Permissions tab means no repository policy statements are configured. This is distinct from the identity's IAM permissions. Use least-privilege IAM credentials for routine work and enable MFA on root.

## Production consideration

Flask's built-in server is for development. Before a production deployment, use a production WSGI server such as Gunicorn and rebuild/repush the image.

## Cost awareness

ECR storage may cost money. ECS/Fargate tasks, load balancers, NAT gateways, and public IPv4 addresses may create ongoing charges. Verify what is running and remove resources when no longer required.

## Self-test

1. How does an image differ from a container?
2. What does `8000:8000` mean?
3. Does `EXPOSE` publish a port on the host?
4. Why use an image digest as well as a tag?
5. Why did the ECR table query fail?
6. Which resources in an ECS/Fargate design may incur charges even with little traffic?

### Answers

1. Image is the package/template; container is a running instance.
2. Host port 8000 maps to container port 8000.
3. No; host port publishing is configured separately.
4. The digest identifies image content, while tags are labels.
5. One result had no tag data, so the assumed table shape did not hold.
6. Depending on the architecture: tasks, load balancers, NAT gateways, public IPv4 addresses, and image storage.

