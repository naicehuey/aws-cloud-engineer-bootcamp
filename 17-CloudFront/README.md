# Project 17 — CloudFront with a Private S3 Bucket (OAC)

## Overview
A static web page served through Amazon CloudFront from a private S3 bucket. The bucket blocks all public access. Only my CloudFront distribution can read it, using Origin Access Control (OAC). Visitors use the CloudFront address over HTTPS, and opening the S3 address directly should be denied. I'm still learning CloudFront, so this README records the plan and what I have evidence for so far.

> **Status:** the files and documentation are ready. Everything marked "to confirm" needs my screenshots and results before I treat it as done.

## Stack
Amazon CloudFront · Amazon S3 · Origin Access Control (OAC) · S3 bucket policy · `curl` · AWS Management Console

## What I practiced
- Keeping an S3 bucket private (Block Public Access on)
- Creating a CloudFront distribution with an S3 origin
- Using Origin Access Control instead of making the bucket public
- Applying the bucket policy CloudFront generates
- Testing that direct S3 access is denied and CloudFront access works
- Reading the `x-cache` header to see a cache Miss and then a Hit

## Configuration (plan)
| Item | Value |
|---|---|
| Bucket | `cdn-origin-static-<unique-id>` in us-east-1, Block all public access: ON |
| Page | `index.html` |
| Distribution origin | the S3 bucket |
| Origin access | Origin access control (OAC), sign requests ON |
| Viewer protocol policy | Redirect HTTP to HTTPS |
| Default root object | `index.html` |
| Bucket policy | allows `s3:GetObject` only from my distribution (`bucket-policy.json`) |

## Project structure
```text
17-cloudfront/
├── project/
│   ├── index.html            # the page
│   └── bucket-policy.json    # template, with placeholders
├── documentation/
│   ├── CloudFront-Journal.md
│   └── CloudFront-Notes.md
├── architecture/
│   └── CloudFront-Architecture-Diagram.md
├── screenshots/
│   ├── 01-cloudfront-distribution-deploying.png
│   ├── 02-s3-bucket-policy-oac.png
│   ├── 03-cloudfront-live-edge-response.png
│   └── 04-cloudfront-cache-hit-headers.png
└── README.md
```

## Architecture
```text
Browser --HTTPS--> CloudFront (edge cache)
                        |  cache miss: signed request (OAC)
                        v
                  S3 bucket (Block Public Access: ON)
                  bucket policy: only this distribution may read

Browser --> S3 URL directly  =>  403 AccessDenied
```

## Screenshots
Add these after hiding the account ID and distribution ID in the policy:

1. `01-cloudfront-distribution-deploying.png` — distribution page with its domain name and status
2. `02-s3-bucket-policy-oac.png` — bucket policy with the CloudFront rule
3. `03-cloudfront-live-edge-response.png` — the page on the `.cloudfront.net` address over HTTPS
4. `04-cloudfront-cache-hit-headers.png` — `curl -I` showing `x-cache: Hit from cloudfront`

I'd also like a screenshot of the 403 from the direct S3 URL, as proof of the private bucket.

## What I did (plan)
1. Create the private S3 bucket and upload `index.html`. (to confirm)
2. Create the CloudFront distribution with the S3 origin, OAC, HTTPS redirect and default root object `index.html`. (to confirm)
3. Copy the bucket policy from CloudFront and paste it into the bucket. (to confirm)
4. Open the S3 URL directly and get 403. (to confirm)
5. Open the CloudFront URL and see the page over HTTPS. (to confirm)
6. Run `curl -I https://<distribution>.cloudfront.net/index.html` twice and compare `x-cache`. (to confirm)
7. Disable and delete the distribution, then empty and delete the bucket. (to confirm)

## Key ideas (in my own words)
- **CDN:** copies of my content are cached at locations near the visitor, so pages load faster.
- **Origin:** where the real files live (the S3 bucket).
- **OAC:** CloudFront signs its requests to S3, and the bucket policy only trusts that distribution. The bucket never needs to be public.
- **Cache Miss and Hit:** the first request goes to S3 (Miss). The next ones come from the edge (Hit).
- **TTL:** how long CloudFront keeps a copy before checking S3 again.
- **Invalidation:** if I change `index.html`, I may need to invalidate the cache to see the new page sooner.

My one-sentence rule: **S3 stays private, CloudFront is the only door, OAC is the key, and the cache makes repeat visits fast.**

## Challenge
Not recorded yet. I'll add any problems and how I fixed them.

## Validation checklist
- [ ] Bucket created with Block Public Access ON
- [ ] `index.html` uploaded
- [ ] Distribution created and deployed
- [ ] OAC bucket policy applied
- [ ] Direct S3 URL returns 403
- [ ] CloudFront URL shows the page over HTTPS
- [ ] Second `curl` shows `x-cache: Hit from cloudfront`
- [ ] Resources deleted

## Notes
- I haven't confirmed that I ran this project yet, so I'm not claiming results.
- The original plan called this "enterprise-grade" and "global". I don't claim that. It is one distribution serving one page, and I'm learning how it works.
- CloudFront has an always-free allowance, but I verify the current pricing. I delete the distribution (it must be disabled first) and the bucket when I'm done, and I check Billing.
- I keep my account ID and distribution ID out of public screenshots.

Documentation was written with AI assistance (Claude) for structure and clarity. I do the labs in the AWS Console myself and check what is written here against what I did.
