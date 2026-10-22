# Project 01 — Learning Notes

## IAM

IAM stands for Identity and Access Management. It controls who can access AWS and what they can do.

## IAM user

One identity for one person or job, with its own credentials. My users: `admin-user`, `auditor-user`, `developer-user`.

## IAM group

A collection of users. Permissions attached to the group apply to every user in it. My groups: `Administrators`, `Auditors`, `Developer`.

```text
Group (permissions) ──> User A
                    ──> User B
```

## IAM policy

A JSON document that lists allowed or denied actions on resources. `Administrators` uses the AWS managed policy `AdministratorAccess`, which gives full access to AWS services.

## Permissions

What an identity is allowed to do. An action looks like this:

```text
iam:ListUsers
```

## Authentication vs authorization

* **Authentication:** proving who I am (username and password).
* **Authorization:** what I'm allowed to do once I'm in (the policy).

## Default deny

If no policy allows an action, it is denied. That is why `developer-user` got:

```text
Access denied to iam:ListUsers
Context: no identity-based policy allows the action
```

## Least privilege

Give each user only the permissions its job needs, and nothing more.

## Root account vs admin user

The root account has full access to everything. I created `admin-user` for daily admin work so the root account stays for rare tasks. Best practice is to protect root with MFA. MFA is not enabled on my practice users yet.

## What I tested

* Correct password: login worked.
* Wrong password: login failed.
* Password reset: login worked again with the new password.
* Allowed action: worked.
* Action outside the permissions: `AccessDenied`.

## Cost awareness

IAM has no extra charge. Still check Billing before creating other resources.

## Self-test

1. What is the difference between a user and a group?
2. What is a policy?
3. What is the difference between authentication and authorization?
4. Why did `developer-user` get `AccessDenied` on `iam:ListUsers`?
5. What is least privilege?
6. Why use `admin-user` instead of the root account every day?

### Answers

1. A user is one identity. A group is a collection of users that share permissions.
2. A JSON document that says which actions are allowed or denied.
3. Authentication proves who I am. Authorization decides what I can do.
4. No identity-based policy allowed that action, and access is denied by default.
5. Giving a user only the permissions it needs.
6. The root account has unlimited access, so using it daily is risky. An admin user can be controlled and changed.

