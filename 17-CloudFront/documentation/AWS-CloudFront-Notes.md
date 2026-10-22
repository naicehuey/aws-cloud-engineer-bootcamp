# Project 17 — Learning Notes

## Core flow
```text
Browser --HTTPS--> CloudFront --(OAC signed request on a miss)--> private S3 bucket
```

## Components
| Component | Role |
|---|---|
| S3 bucket | origin that stores the files, public access blocked |
| CloudFront distribution | CDN with edge caching and HTTPS |
| OAC | lets CloudFront sign requests to S3 |
| Bucket policy | allows `s3:GetObject` only from my distribution |
| Default root object | `index.html`, served for the bare domain |

## Why OAC
Instead of making the bucket public, CloudFront proves who it is with a signed request. The bucket policy then allows only that distribution (the `AWS:SourceArn` condition). OAC replaces the older Origin Access Identity (OAI).

## Bucket policy (`project/bucket-policy.json`)
- `Principal: cloudfront.amazonaws.com`: the CloudFront service
- `Action: s3:GetObject`: read files only
- `Resource`: files in my bucket
- `Condition AWS:SourceArn`: only my distribution

## The two tests
```text
S3 URL directly          -> 403 AccessDenied   (bucket is private)
CloudFront URL           -> 200, page loads over HTTPS
```

## Cache check
```bash
curl -I https://<distribution>.cloudfront.net/index.html
```
- First run: `x-cache: Miss from cloudfront` (fetched from S3)
- Second run: `x-cache: Hit from cloudfront` (served from the edge)

## Cache keys, TTL and invalidation
- **Cache key:** by default the URL and host decide whether a cached copy matches.
- **TTL:** how long CloudFront keeps a copy before checking S3.
- **Invalidation:** tells CloudFront to drop cached copies, for example `/*` after I change a file.

## Troubleshooting
```text
403 from CloudFront -> bucket policy applied? right bucket and distribution ID? default root object set?
Old page still shown -> cache; wait for TTL or create an invalidation
Distribution won't delete -> disable it first and wait
Direct S3 URL works  -> Block Public Access is off or a public policy exists
```

## Cost awareness
Check current pricing. Disable and delete the distribution, then empty and delete the bucket.

## Self-test
1. What is a CDN?
2. What is the origin here?
3. What does OAC do?
4. Why must the direct S3 URL fail?
5. What do Miss and Hit mean?
6. What is TTL?
7. How do I show a changed file quickly?

### Answers
1. A network of edge locations that cache content near users.
2. The S3 bucket.
3. It lets CloudFront sign requests to S3, so the bucket can stay private.
4. It proves the bucket is private and CloudFront is the only way in.
5. Miss: CloudFront fetched from S3. Hit: it served its cached copy.
6. How long a cached copy is kept before CloudFront checks again.
7. Create an invalidation.

## One-sentence memory rule
> **S3 stays private, CloudFront is the only door, OAC is the key, and the cache makes repeat visits fast.**
