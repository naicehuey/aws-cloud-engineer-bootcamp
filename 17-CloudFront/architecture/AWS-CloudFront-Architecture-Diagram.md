# Project 17 — Architecture

```text
   Browser
      |
      | 1. HTTPS request
      v
 +--------------------------------------+
 | CloudFront distribution              |
 | edge cache, HTTP redirects to HTTPS  |
 | default root object: index.html      |
 +-------+------------------+-----------+
         |                  |
   cache hit:         cache miss:
   return from        2. signed request (OAC)
   the edge                |
                           v
              +--------------------------------+
              | S3 bucket (origin)             |
              | Block Public Access: ON        |
              | bucket policy: s3:GetObject    |
              | only from this distribution    |
              +--------------------------------+
                           |
                           v  3. file returned, cached at the edge

 Direct S3 URL from a browser  ->  403 AccessDenied
```
