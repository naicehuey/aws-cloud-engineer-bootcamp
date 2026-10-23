# Project 16 — CI/CD with GitHub Actions, ECR and ECS

## Overview
In Project 14 I containerised a Flask app and in Project 15 I ran it on ECS Fargate by hand. In this project I automated the whole path. When I push a change to `main`, GitHub Actions runs my tests, builds the Docker image, pushes it to Amazon ECR, and deploys it to the ECS service. GitHub gets short-lived AWS access through OIDC, so I don't store AWS access keys in GitHub. I'm still learning CI/CD, so this README records what I did and what I learned.

## Stack
GitHub Actions · Docker · Amazon ECR · Amazon ECS (Fargate) · AWS IAM (OIDC) · AWS CloudTrail · Python 3.12 (`unittest`) · Flask app from Project 14

## What I practiced
- Writing a GitHub Actions workflow in YAML
- Running automated tests before a deployment
- Building and pushing a Docker image tagged with the Git commit
- Deploying a new task definition to an existing ECS service
- Using GitHub OIDC and an IAM role instead of stored AWS keys
- Reading CloudTrail to fix an OIDC login failure

## What CI and CD mean
- **CI, Continuous Integration:** every time code is pushed, it is built and tested automatically. In my workflow this is the `test` job.
- **CD, Continuous Delivery or Deployment:** the tested code is delivered to the place it runs. In my workflow the `deploy` job does this with no button to click, which is continuous deployment.

## Configuration
| Item | Value |
|---|---|
| Region | us-east-1 |
| ECR repository | `project14-webapp` |
| ECS cluster / service | `project15-flask-cluster` / `project15-flask-service` |
| Container / task definition | `project15-flask` / family `project15-flask` |
| Log group | `/ecs/project15-flask` |
| IAM role for GitHub | `GitHubActionsProject16Role` |
| Workflow file | `.github/workflows/project16-ci.yml` (in the repository root) |
| Triggers | push to `main` (when the app or workflow changes), pull request, manual run |
| Image tag | the commit SHA (`${{ github.sha }}`) |

## Project structure
```text
16-cicd/
├── project/
│   ├── project16-ci.yml                              # reference copy of the workflow
│   └── iam/
│       ├── project16-github-oidc-trust-policy.json   # who may assume the role
│       └── project16-ecr-ecs-deploy-policy.json      # what the role may do
├── documentation/
│   ├── CICD-Journal.md
│   ├── CICD-Notes.md
│   └── CICD-Scripts-and-Files.md
├── architecture/
│   └── CICD-Architecture-Diagram.md
├── screenshots/
│   ├── project16-01-github-actions-success.png
│   ├── project16-02-automated-tests.png
│   ├── project16-03-iam-oidc-trust.png
│   ├── project16-04-ecr-published-image.png
│   ├── project16-05-ecs-running-deployment.png
│   ├── project16-06a-application-response.png
│   └── project16-06b-health-endpoint.png
└── README.md
```
The Flask app, Dockerfile, requirements and tests live in the Project 14 folder and are reused here. The working workflow file must stay in `.github/workflows/` at the root of the repository, because GitHub only runs workflows from there. The copy in `project/` is for reading.

## Architecture
```text
Developer --push to main--> GitHub --> GitHub Actions
                                          |
                          [test job] install + unit tests
                                          | tests pass
                          [deploy job] OIDC token --> IAM role (short-lived credentials)
                                          |
                          build image --> push to ECR (tag = commit SHA)
                                          |
                          render ECS task definition with the new image
                                          |
                          deploy to ECS service, wait for stability
                                          v
                          Flask app on Fargate (port 8000): / and /health
```

## Screenshots
Add these after hiding the account ID and the public IP:

1. `project16-01-github-actions-success.png` — the green workflow run
2. `project16-02-automated-tests.png` — the test step output
3. `project16-03-iam-oidc-trust.png` — the role's trust policy
4. `project16-04-ecr-published-image.png` — image tagged with the commit SHA in ECR
5. `project16-05-ecs-running-deployment.png` — the ECS service after the deployment
6. `project16-06a-application-response.png` — the app root in the browser
7. `project16-06b-health-endpoint.png` — the `/health` endpoint

## What I did
1. Added `.github/workflows/project16-ci.yml` with a `test` job and a `deploy` job.
2. Set up Python 3.12 and ran `python -m unittest discover -s tests -v`.
3. Made `deploy` wait for `test` and skip pull requests.
4. Created the GitHub OIDC provider and the role `GitHubActionsProject16Role` in AWS, with a deploy policy for ECR and ECS.
5. The first runs could not assume the role. I looked up the failed `AssumeRoleWithWebIdentity` event in CloudTrail and saw the exact subject GitHub sent.
6. Updated the trust policy to match that subject, still limited to my repository and the `main` branch.
7. Re-ran the workflow and it passed (green run).
8. Checked that the root page and `/health` worked.

## Key ideas (in my own words)
- **Workflow:** the YAML file that tells GitHub what to run and when.
- **Job and step:** a job is a group of steps on one machine. The `deploy` job `needs` the `test` job, so a failed test stops the deployment.
- **Commit SHA tag:** each image is named after the commit that made it, so I can tell which code is running.
- **OIDC:** GitHub proves who it is to AWS, and AWS hands out short-lived credentials. No long-lived keys are stored.
- **Trust policy vs permissions policy:** the trust policy says who may use the role. The permissions policy says what the role may do.
- **Waiting for stability:** the pipeline only finishes when ECS has settled on the new version.

My one-sentence rule: **push the code, the tests run, the image is built and tagged, and ECS rolls out the new version without any stored AWS keys.**

## Challenge
The role assumption failed with `sts:AssumeRoleWithWebIdentity`. I didn't guess. I opened CloudTrail, found the failed event, and compared the subject GitHub sent with the one in my trust policy. They didn't match, because the subject includes GitHub's owner and repository IDs. I changed the trust policy to the observed subject and it worked. I kept it limited to one repository and the `main` branch.

## Validation checklist
- [x] Unit tests pass (`test_home_endpoint` and `test_health_endpoint`)
- [x] Workflow ran green
- [x] OIDC role assumption works
- [x] Root and `/health` endpoints reachable when tested
- [ ] Image in ECR tagged with the commit SHA (confirm in a screenshot)
- [ ] Screenshots saved
- [ ] Port 8000 rule restricted
- [ ] Resources cleaned up

## Notes
- **Public IP:** the task's public IP changes if ECS replaces the task. For a permanent address I would need a load balancer, DNS and HTTPS. I haven't built that.
- **Security:** port 8000 is open to the whole internet for the demo. I restrict it afterwards.
- **IAM:** the role is scoped to one ECR repository, one ECS service and one role it may pass. A few actions can't be limited to one resource, as far as I know. I'd still review it before real use.
- **Action versions:** GitHub may warn about old action versions. I check this from time to time.
- **Cost:** each deployment and the running Fargate task can charge. When I'm done I set the service to 0 tasks or delete it, and check Billing.

Documentation was written with AI assistance (Claude) for structure and clarity. I did the lab myself and checked what is written here against what I did.
