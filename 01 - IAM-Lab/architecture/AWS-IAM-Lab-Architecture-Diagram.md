# Project 01 — Architecture

```
              Root account
        (kept for rare tasks only)
                   |
                   v
               admin-user
          (used for daily admin work)
                   |
                   v
        Create groups and attach permissions
                   |
     +-------------+--------------+
     |             |              |
     v             v              v
Administrators   Auditors      Developer
(Administrator-  (permissions   (permissions
   Access)        defined)       defined)
     |             |              |
     v             v              v
 admin-user    auditor-user  developer-user
     |             |              |
     +-------------+--------------+
                   |
                   v
     Log in and test with each user
        |                      |
        v                      v
 Allowed action           Not-allowed action
 (group allows it)   (AccessDenied, e.g. iam:ListUsers)
```

