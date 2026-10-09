
---

# 2. `journal.md`

```markdown
# AWS Project Journal

**Project:** 01 - IAM Lab  
**Date:** August 2026

---

## Today's Objective

Today I completed the documentation and additional testing for my AWS IAM practical.

I had already performed most of the IAM configuration earlier, but I had not properly documented the work in my AWS Cloud Engineer Bootcamp GitHub project.

My goal was to organize the screenshots, review what I had learned, test the developer account, and document the practical experience.

---

## What I Worked On

Today I reviewed and documented:

- IAM Dashboard
- IAM Users
- IAM Groups
- IAM Policies
- Group permissions
- Console authentication
- Failed login
- Password reset
- Developer console login
- Developer permissions
- IAM access restrictions

---

## IAM Concepts Reviewed

I reviewed the difference between:

- IAM users
- IAM groups
- IAM policies
- Permissions
- Authentication
- Authorization
- Least privilege

One important concept I reinforced was that a user represents an individual identity, while a group allows users with similar responsibilities to be managed together.

---

## Password Reset Practice

I practiced resetting the developer user's AWS Console password.

I also tested the login process after the password reset.

This helped me understand the practical process of managing an IAM user's console credentials.

---

## Failed Login Test

I performed an unsuccessful login attempt with the developer account.

This demonstrated that having an IAM user does not automatically mean that every login attempt will succeed.

The credentials used during authentication must be correct.

---

## Developer Account Testing

After resetting the developer user's password, I successfully used the developer account to access the AWS Console.

I then tested what the account was actually allowed to do.

This was important because it allowed me to see IAM authorization in practice instead of only reading about it.

---

## Permission Testing

While logged in as `developer-user`, I attempted to access the IAM Users section.

AWS returned:

```text
Access denied to iam:ListUsers