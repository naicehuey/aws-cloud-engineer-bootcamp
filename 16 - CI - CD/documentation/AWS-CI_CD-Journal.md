# Project 16 — Project Journal

**Date:** Not recorded

## Goal
Automate testing and deployment of my Flask app to AWS, so a push to `main` updates the running service without manual steps.

## Work completed
- Added the GitHub Actions workflow `project16-ci.yml`.
- Set up Python 3.12 and automatic `unittest` runs.
- Made deployment wait for tests and skip pull requests.
- Created the GitHub OIDC provider and the role `GitHubActionsProject16Role`, with ECR and ECS permissions.
- Fixed the role assumption failure using CloudTrail.
- Re-ran the workflow: green run.
- Checked the root page and `/health`.

## What I learned
- CI means tests run automatically on every change. CD means the tested change is delivered automatically.
- Tagging images with the commit SHA tells me exactly which code is deployed.
- OIDC gives GitHub short-lived AWS access, so no access keys are stored in GitHub.
- A trust policy must match the subject GitHub sends exactly.
- `needs: test` stops a deployment when a test fails.
- Pull requests should test but not deploy.

## Issue and lesson
`sts:AssumeRoleWithWebIdentity` failed. I looked at the failed STS event in CloudTrail and compared the subject and audience with my trust policy. The subject includes GitHub's immutable owner and repository IDs, so my original subject didn't match. I updated the policy to the observed value and kept it limited to my repository and the `main` branch.

Lesson: when access fails, read the exact event and compare values instead of guessing, and never widen trust to all repositories.

## Mistakes to avoid (for my future projects)
- Guessing at trust policy values.
- Allowing every repository or branch in a trust policy.
- Committing long-lived AWS keys.
- Leaving the demo port open and the service running.

## Evidence
Screenshots 01 to 06b: workflow run, tests, trust policy, ECR image, ECS deployment, app and health endpoints.

## Outcome
A working pipeline: push to `main`, tests, image build, ECR push, ECS deployment. Next I want to put a load balancer and HTTPS in front of the app and add a stronger health check.

## Cost reminder
Fargate and public IPv4 charge while running. Set the service to 0 tasks, delete resources when done, and check Billing.
