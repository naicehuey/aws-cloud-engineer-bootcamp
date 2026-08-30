# 01 - IAM Lab

## Overview

This project demonstrates my practical learning and implementation of AWS Identity and Access Management (IAM).

The purpose of this lab was to understand AWS identities, users, groups, policies, permissions, authentication, authorization, and the principle of least privilege.

This project was completed as part of my AWS Cloud Engineer Bootcamp.

---

## Objectives

The objectives of this lab were to:

- Understand AWS IAM.
- Understand IAM users.
- Understand IAM groups.
- Understand IAM policies.
- Understand permissions.
- Create and manage IAM users and groups.
- Assign permissions through groups.
- Practice the principle of least privilege.
- Configure and test AWS Console access.
- Practice resetting an IAM user's console password.
- Test authentication with an IAM user.
- Test permissions using a restricted developer account.
- Observe an AWS `AccessDenied` response.
- Document the practical work using screenshots.

---

## AWS Service Used

### AWS IAM

AWS Identity and Access Management (IAM) is an AWS service used to control access to AWS resources.

IAM allows identities to be created and permissions to be assigned through policies.

---

## Key Concepts Learned

### IAM User

An IAM user represents an individual identity within an AWS account.

An IAM user can have credentials and permissions that allow the user to interact with AWS resources.

---

### IAM Group

An IAM group is a collection of IAM users.

Groups make permission management easier because permissions can be assigned to a group instead of configuring every user individually.

For example, if multiple developers require the same permissions, they can be placed into a developer group and the required permissions can be assigned to that group.

---

### IAM Policy

An IAM policy is a document that defines permissions.

Policies specify which AWS actions an identity is allowed or denied to perform on resources.

AWS IAM policies are commonly written using JSON.

---

### Permissions

Permissions determine what an identity is allowed to do within AWS.

For example:

```text
iam:ListUsers