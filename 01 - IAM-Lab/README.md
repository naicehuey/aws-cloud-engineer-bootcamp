# Project 01 — IAM Lab

## Overview

My first hands-on lab with AWS Identity and Access Management (IAM). I created three users for different jobs (an administrator, an auditor and a developer), put each one in its own group, and then tested them: logging in with the right and wrong passwords, using actions their group allows, and trying actions it does not. I also created an admin user so I don't have to use the root account for everyday work. I'm a beginner with IAM, so this README records what I did and what I understood so far.

## Stack

AWS IAM · AWS Management Console

## What I practiced

* Creating IAM users and groups
* Attaching permissions to groups instead of to each user
* Giving different jobs different permissions (administrator, auditor, developer)
* Creating an admin user instead of using the root account every day
* Logging in with the right and wrong passwords
* Resetting an IAM user's console password
* Testing allowed and not-allowed actions
* Reading an `AccessDenied` message

## Project structure

```text
01 - project/
02 - documentation/
03 - screenshots/
```

## What I did

1. Looked around the IAM dashboard.
2. Created three groups: `Administrators`, `Auditors` and `Developer`.
3. Attached permissions to each group. The `Administrators` group uses the AWS managed policy `AdministratorAccess`.
4. Created three users, one in each group: `admin-user`, `auditor-user` and `developer-user`.
5. Used `admin-user` for admin work so the root account can stay for rare tasks.
6. Logged in as each user and tried actions their group allows.
7. Tried actions their group does not allow and read the `AccessDenied` errors.
8. Typed wrong passwords on purpose to see the login fail.
9. Reset a user's console password and logged in again.
10. Organised the screenshots and wrote this documentation.

## Users and groups I created

|User|Group|Job|
|-|-|-|
|`admin-user`|`Administrators`|Administrator, uses `AdministratorAccess` (AWS managed)|
|`auditor-user`|`Auditors`|Auditor|
|`developer-user`|`Developer`|Developer|

## Key ideas (in my own words)

* **IAM user:** one identity for one person or job, with its own credentials.
* **IAM group:** a collection of users. I attach permissions to the group, so users with the same job get the same permissions.
* **IAM policy:** a JSON document that says which actions are allowed or denied.
* **Authentication vs authorization:** authentication is "who are you?" (the password). Authorization is "what are you allowed to do?" (the policy).
* **Least privilege:** give each account only the permissions its job needs.
* **Root account:** has full access to everything, so I avoid using it for daily work and use an admin IAM user instead.

## Challenge

Testing showed me that logging in successfully doesn't mean you can do everything. When `developer-user` opened the IAM Users page, the console showed `Access denied to iam:ListUsers` with the reason "no identity-based policy allows the action". That means nothing in the user's permissions allowed it, and access is denied by default. Wrong passwords were rejected as expected, and I fixed that by resetting the password.

## Validation checklist

* \[x] Three IAM groups created (`Administrators`, `Auditors`, `Developer`)
* \[x] Three IAM users created (`admin-user`, `auditor-user`, `developer-user`)
* \[x] Permissions attached through groups
* \[x] Admin user created so the root account is not used every day
* \[x] Logged in with a correct password
* \[x] Failed login tested with a wrong password
* \[x] Password reset and tested
* \[x] Allowed and not-allowed actions tested
* \[x] `AccessDenied` response observed
* \[x] Screenshots captured (see `03 - screenshots/`)
* \[ ] MFA on the IAM users (not done yet)

## Notes

IAM itself has no extra charge, and no billable resources were created in this project. MFA is not enabled on these practice users yet. Best practice is to turn it on, and to protect the root account with MFA too. I'm still learning IAM, so writing my own policies is something I want to practice next.

Documentation was written with AI assistance (Claude) for structure and clarity. I did the lab in the AWS Console myself and checked what is written here against what I did.

