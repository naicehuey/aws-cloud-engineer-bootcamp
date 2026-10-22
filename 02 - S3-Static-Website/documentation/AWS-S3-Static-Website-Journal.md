# Project 02 — Project Journal

**Date:** July 31, 2026

## Goal
Use Amazon S3 to host a static website. I had already learned the basics of S3 and created a bucket, so this lab focused only on website hosting, not on S3 as a whole.

## Work completed
1. Built a simple personal portfolio website with HTML, CSS and JavaScript, plus an image and a custom error page.
2. Used my bucket `kidyadidi-aws-lab-s3-001` and uploaded the website files to it.
3. Turned on static website hosting.
4. Set `index.html` as the index document and `error.html` as the error document.
5. Set the bucket permissions so the website can be viewed.
6. Opened the website endpoint and checked the home page.
7. Tested the custom error page with a page that doesn't exist.

## What I built
- `index.html`: profile, About section with three cards (AWS, Development, Infrastructure), Contact section and footer
- `error.html`: "404 Page Not Found" with a button back to the home page
- `style.css`: dark blue theme that adjusts for smaller screens
- `script.js`: adds the current year to the footer and fades sections in as I scroll
- `Image-1.png`: my profile photo

## What I learned
- S3 stores files as objects in a bucket, and a bucket can serve them as a website.
- A static website needs an index document and, if I want one, an error document.
- Buckets are private by default, so visitors can only see the site if the permissions allow it.
- A static site has no server code or database. The browser does all the work.
- S3 website endpoints use HTTP, not HTTPS.

## Mistakes to avoid (for my future projects)
- Putting private files in a bucket that has public website access.
- Forgetting to set the index and error documents.
- Leaving a bucket running after I'm finished with it.
- Leaving placeholder links in a page I plan to share.

## Evidence
Screenshots: S3 bucket with the uploaded files, static website hosting settings, bucket permissions, the website home page and the custom error page.

## Outcome
I now have a website running from an S3 bucket, with a working custom error page. I'm still a beginner with S3, and I enjoyed this project. The page still has placeholder social links, CV button and contact email to fill in. Next is Project 03: running a web server on EC2.

## Cost reminder
S3 storage and requests can cost a little. I check my billing page and delete the bucket and its files when I no longer need them.
