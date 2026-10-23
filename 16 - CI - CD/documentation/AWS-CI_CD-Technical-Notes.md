# Project 16 — Learning Notes

## CI and CD
- **CI (Continuous Integration):** merge small changes often and run build and tests automatically each time.
- **Continuous Delivery:** every tested change is made ready to release, and a person approves the release.
- **Continuous Deployment:** every tested change goes live automatically. My pipeline does this.
- **CI/CD pipeline:** the automatic path from a code change to the running app.

## My pipeline
```text
push to main -> test job -> deploy job
test:    check out -> Python 3.12 -> install requirements -> unittest
deploy:  OIDC credentials -> ECR login -> build + push image (tag = commit SHA)
         -> download current task definition -> put in the new image -> deploy to ECS -> wait
```

## Workflow behaviour
- `push` to `main` runs when the app folder or the workflow file changes.
- `pull_request` runs the tests only (the deploy job is skipped).
- `workflow_dispatch` lets me run it by hand.
- `needs: test` blocks deployment if tests fail.
- `permissions: id-token: write` lets the job ask GitHub for an OIDC token.
- `${{ github.sha }}` is the commit ID used as the image tag.
- `wait-for-service-stability: true` makes the job wait until ECS is stable.

## Actions used
| Action | Job |
|---|---|
| `actions/checkout` | get the code |
| `actions/setup-python` | install Python 3.12 |
| `aws-actions/configure-aws-credentials` | get short-lived AWS credentials via OIDC |
| `aws-actions/amazon-ecr-login` | log Docker in to ECR |
| `aws-actions/amazon-ecs-render-task-definition` | put the new image in the task definition |
| `aws-actions/amazon-ecs-deploy-task-definition` | deploy it and wait |

## OIDC
- GitHub gives the job a signed token that says which repository and branch it comes from.
- AWS checks the token against the role's trust policy (`sub` and `aud` claims).
- If it matches, AWS gives temporary credentials. No stored keys.
- Trust policy: `sts:AssumeRoleWithWebIdentity`, `aud = sts.amazonaws.com`, `sub = repo and branch`.

## Deploy permissions (what the role may do)
- Get an ECR login token.
- Push images to one repository, `project14-webapp`.
- Register and read task definitions.
- Update and read one ECS service.
- Pass `ecsTaskExecutionRole` to ECS tasks, only for `ecs-tasks.amazonaws.com`.

## Troubleshooting
```text
Not authorized to assume role -> CloudTrail: find the failed AssumeRoleWithWebIdentity
                                 compare sub and aud with the trust policy
Tests fail                    -> deploy is skipped; read the test step output
Docker push denied            -> role permissions or ECR repository name
Deployment never stable       -> ECS service events, stopped reason, container logs
Workflow didn't start         -> changed files outside the path filter? workflow must be in .github/workflows
```

## Caveats
- Public task IPs change. A durable setup needs a load balancer and HTTPS.
- Port 8000 was open to the world for the demo.
- Check action version warnings now and then.

## Self-test
1. What does CI mean?
2. What does CD mean?
3. Why does `deploy` have `needs: test`?
4. Why tag the image with the commit SHA?
5. What does OIDC replace?
6. What is the difference between a trust policy and a permissions policy?
7. How do I fix an OIDC login failure?
8. Why skip deployment on pull requests?

### Answers
1. Continuous Integration: build and test automatically on every change.
2. Continuous Delivery or Deployment: automatically deliver the tested change to where it runs.
3. So a failed test stops the deployment.
4. It tells me exactly which commit produced the image that is running.
5. Stored long-lived AWS access keys in GitHub.
6. The trust policy says who can use the role. The permissions policy says what it can do.
7. Find the failed event in CloudTrail and compare the subject and audience with the trust policy.
8. Pull requests aren't approved code yet, so they are tested but never go live.

## One-sentence memory rule
> **Push the code, the tests run, the image is built and tagged, and ECS rolls out the new version without any stored AWS keys.**
