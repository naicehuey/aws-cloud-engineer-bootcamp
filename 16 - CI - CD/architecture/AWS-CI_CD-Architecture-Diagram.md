# Project 16 — Architecture

```
  Developer
     |  git push to main
     v
  +------------------+
  | GitHub repo      |
  +--------+---------+
           |
           v
  +--------------------------------------------------------------+
  | GitHub Actions: project16-ci.yml                             |
  |                                                              |
  |  Job 1: test                                                 |
  |    install dependencies, run unittest                        |
  |           | tests pass (needs: test)                         |
  |           v                                                  |
  |  Job 2: deploy (skipped on pull requests)                    |
  |    1. OIDC token --------------------+                       |
  |    2. build image, tag = commit SHA  |                       |
  |    3. push image                     |                       |
  |    4. render task definition         |                       |
  |    5. deploy and wait                |                       |
  +--------------------------------------+-----------------------+
                                         |
                                         v
                         +-------------------------------+
                         | AWS IAM role (via OIDC)       |
                         | GitHubActionsProject16Role    |
                         | short-lived credentials       |
                         +---------------+---------------+
                                         |
              +--------------------------+---------------------------+
              v                                                      v
   +-----------------------+                       +------------------------------+
   | Amazon ECR            |  image pulled by ECS  | ECS Fargate service          |
   | project14-webapp:     | --------------------> | project15-flask-service      |
   | <commit SHA>          |                       | task definition updated      |
   +-----------------------+                       +--------------+---------------+
                                                                  |
                                          +-----------------------+----------------+
                                          v                                        v
                                 Flask app :8000                       CloudWatch Logs
                                 GET /    GET /health                  /ecs/project15-flask
```

