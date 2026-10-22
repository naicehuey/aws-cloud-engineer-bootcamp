# Project 02 — S3 Static Website

## Overview
My first website hosted on AWS. I built a simple personal portfolio page with HTML, CSS and JavaScript, uploaded the files to an Amazon S3 bucket, turned on static website hosting, and tested both the home page and a custom error page. I'm a beginner with S3, so this README records what I did and what I understood so far.

## Stack
HTML · CSS · JavaScript · Amazon S3 · AWS Management Console

## What I practiced
- Storing website files as objects in an S3 bucket
- Turning on S3 static website hosting
- Setting an index document and a custom error document
- Setting bucket permissions so the website can be viewed
- Understanding the S3 website endpoint
- Testing the site and the error page in a browser

## Website files
```text
website/
├── index.html
├── error.html
├── style.css
├── script.js
└── Image-1.png
```

## Project structure
```text
01 - project/
02 - documentation/
03 - screenshots/
```

## What the website has
- **Home page (`index.html`):** a profile section with my photo, name and skills, an About section with three cards (AWS, Development, Infrastructure), a Contact section and a footer.
- **Error page (`error.html`):** a "404 Page Not Found" message with a button back to the home page.
- **Styling (`style.css`):** a dark blue theme, with a layout that adjusts for smaller screens.
- **Script (`script.js`):** fills in the current year in the footer and fades each section in as I scroll.
- **Outside resources:** the Boxicons icons and the Poppins font are loaded from the internet, not from my bucket.

## What I did
1. Built the website files on my computer.
2. Used my S3 bucket `kidyadidi-aws-lab-s3-001` (I created it in an earlier practice).
3. Uploaded the five website files to the bucket.
4. Turned on static website hosting for the bucket.
5. Set `index.html` as the index document and `error.html` as the error document.
6. Set the bucket permissions so the website files can be read by visitors.
7. Opened the S3 website endpoint in a browser and checked the home page.
8. Typed a page that doesn't exist to check the custom error page.
9. Organised the screenshots and wrote this documentation.

## Key ideas (in my own words)
- **S3 object and bucket:** S3 stores files as objects inside a bucket.
- **Static website:** a site made only of files (HTML, CSS, JavaScript, images) that the browser runs. There is no server code or database.
- **Index document:** the page S3 shows when someone opens the site's address (`index.html`).
- **Error document:** the page S3 shows when the page asked for isn't found (`error.html`).
- **Website endpoint:** the web address S3 gives the bucket once hosting is on.
- **Permissions:** a bucket is private by default, so I had to set permissions that let visitors read the website files.

## Validation checklist
- [x] Website files built (HTML, CSS, JavaScript, image, error page)
- [x] Files uploaded to the S3 bucket
- [x] Static website hosting turned on
- [x] Index document and error document set
- [x] Bucket permissions set for website access
- [x] Website tested in a browser
- [x] Custom error page tested
- [x] Screenshots captured (see `03 - screenshots/`)

## Notes
S3 storage and requests can cost a little, so I delete the bucket and its files when I no longer need them. S3 website endpoints use plain HTTP, not HTTPS. I'm still learning about this and want to see how CloudFront adds HTTPS in a later project. The social media links, the CV button and the contact email on the page are placeholders I still need to fill in.

Documentation was written with AI assistance (Claude) for structure and clarity. I did the lab in the AWS Console myself and checked what is written here against what I did.
