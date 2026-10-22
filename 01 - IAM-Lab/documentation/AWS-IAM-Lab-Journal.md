# Project 01 — Project Journal

**Date:** August 2026 (lab set up in July 2026; the `Administrators` group was created on July 23, 2026)

## Goal

Learn how IAM works by creating users with different permissions and then testing them, including trying things that should fail.

## Work completed

1. Explored the IAM dashboard.
2. Created three groups: `Administrators`, `Auditors` and `Developer`.
3. Attached permissions to the groups. `Administrators` uses the AWS managed policy `AdministratorAccess`.
4. Created three users, one per group: `admin-user`, `auditor-user` and `developer-user`.
5. Used `admin-user` for admin work so I don't use the root account every day.
6. Logged in with each user and tried actions its group allows.
7. Tried actions each user was not allowed to do.
8. Tried wrong passwords on purpose.
9. Reset a user's console password and logged in again.
10. Later, organised the screenshots and wrote the documentation. I had done most of the setup earlier but had not documented it properly.

## What I learned

* A user is one identity. A group lets me manage users with the same job together.
* Policies decide what a user can do. Logging in doesn't give access to everything.
* By default, a user can do nothing unless a policy allows it.
* Authentication is proving who I am. Authorization is what I'm allowed to do.
* An admin IAM user lets me avoid the root account for everyday work.

## Issue and lesson

I tested the users by breaking things on purpose:

* A wrong password failed the login. I fixed it by resetting the password and logging in again.
* `developer-user` logged in to the console but got `Access denied to iam:ListUsers` when it opened the IAM Users page. The console explained why: "no identity-based policy allows the action".
* Actions that matched a user's group worked, and actions outside it were denied.

Lesson: seeing `AccessDenied` for myself explained authorization better than reading about it. It also showed me why least privilege matters.

## Mistakes to avoid (for my future projects)

* Using the root account for daily work.
* Giving every user admin permissions "to make it work".
* Attaching permissions to each user instead of to a group.
* Forgetting which user I'm logged in as when something fails.

## Evidence

Screenshots: IAM users list, IAM user groups list, `Administrators` group permissions (`AdministratorAccess`), policies list, failed login, password reset, developer console login, and the `AccessDenied` message for `iam:ListUsers`.

## Outcome

I now understand the basics of users, groups, policies and least privilege, and I've seen them work and fail in a real account. I'm still a beginner with IAM. MFA is not enabled on the practice users yet, and I want to practice writing my own policies. Next is Project 02: hosting a static website on S3.

## Cost reminder

IAM has no extra charge, and no billable resources were created. I still check my billing page before each project.

