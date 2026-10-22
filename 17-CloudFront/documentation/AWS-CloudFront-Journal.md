# Project 17 — Project Journal

**Date:** Not recorded

## Goal
Serve a web page through CloudFront from an S3 bucket that is not public, and see caching working.

## Work completed
- Documentation, `index.html` and the bucket policy template are written.
- The build steps are to confirm once I add screenshots.

## What I learned so far
- A bucket can stay fully private while a CDN serves its files.
- OAC lets CloudFront sign requests to S3, and a bucket policy trusts only my distribution.
- Direct S3 access should fail with 403 while the CloudFront address works.
- `x-cache` shows a Miss on the first request and a Hit on later ones.
- Changes to a cached file can take time to appear unless I invalidate the cache.

## Issue and lesson
Not recorded yet. Things to watch: a 403 from CloudFront (bucket policy or default root object wrong), and the policy needing the right bucket name and distribution ID.

## Mistakes to avoid (for my future projects)
- Making the bucket public to get around a permissions problem.
- Posting the distribution ID and account ID in screenshots.
- Claiming a cache Hit without the header screenshot.
- Leaving the distribution and bucket after the lab.

## Evidence
Screenshots 01 to 04 will go in `screenshots/`.

## Outcome
Documented, not confirmed. I'll update this after I run the project.

## Cost reminder
Delete the distribution (disable it first) and the bucket when finished, and check Billing.
