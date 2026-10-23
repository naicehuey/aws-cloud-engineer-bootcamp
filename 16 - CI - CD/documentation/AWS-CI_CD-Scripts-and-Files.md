# Project 16 — Scripts and Files

A list of every file in this project, what it is for, and where it goes in the repository.

## Scripts and configuration
| File | Purpose | Where it lives |
|---|---|---|
| `project/project16-ci.yml` | GitHub Actions workflow: test, build image, push to ECR, deploy to ECS | The working copy must be at `.github/workflows/project16-ci.yml` in the repository root. This copy is a reference with `<ACCOUNT_ID>` in place of the real one. |
| `project/iam/project16-github-oidc-trust-policy.json` | Trust policy: lets GitHub Actions assume the role, for one repository and the `main` branch only | Pasted into the IAM role's trust relationship |
| `project/iam/project16-ecr-ecs-deploy-policy.json` | Permissions policy: what the role may do in ECR and ECS | Attached to the role `GitHubActionsProject16Role` |

## Documentation
| File | Purpose |
|---|---|
| `README.md` | Project overview, configuration, folder structure, checklist |
| `documentation/CICD-Journal.md` | What I did, the OIDC error and the lesson |
| `documentation/CICD-Notes.md` | Workflow, OIDC, IAM, troubleshooting, self-test |
| `documentation/CICD-Scripts-and-Files.md` | This inventory |
| `architecture/CICD-Architecture-Diagram.md` | Pipeline diagram |
| `screenshots/` | 7 screenshots, with the account ID and public IP hidden |

## Reused from Project 14
The Flask app, Dockerfile, `requirements.txt`, compose file and unit tests (`tests/`) are in the Project 14 folder. Projects 14, 15 and 16 all use them, so they are not copied here.

## Placeholders
`<ACCOUNT_ID>` is my 12-digit AWS account ID. I keep the real value out of public files.
