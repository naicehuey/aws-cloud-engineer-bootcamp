# Project 02 — Learning Notes

## Amazon S3
Amazon Simple Storage Service (S3) is an object storage service. It stores data as objects inside buckets.

## Bucket
A bucket is a container for objects. My bucket:

```text
kidyadidi-aws-lab-s3-001
```

## Object
A file stored in a bucket. My website files are objects.

## Static website
A website made only of files that the browser runs: HTML, CSS, JavaScript and images. No server code and no database.

```text
website/
├── index.html
├── error.html
├── style.css
├── script.js
└── Image-1.png
```

## Static website hosting
An S3 setting that lets a bucket serve its files as a website.

- **Index document:** `index.html`. Shown when someone opens the site address.
- **Error document:** `error.html`. Shown when the page asked for isn't found.

## Website endpoint
The web address S3 gives the bucket when hosting is on. S3 website endpoints use HTTP, not HTTPS.

## Permissions
A bucket is private by default. For a public website, the permissions must let visitors read the website files. This is also why a public bucket should hold only the website files.

## How the files work together
- `index.html` is the page. It loads `style.css` for looks and `script.js` for behaviour.
- `script.js` fills in the year and fades sections in as I scroll.
- `error.html` uses the same `style.css`, so it matches the home page.
- The Boxicons icons and the Poppins font come from the internet, not from my bucket.

## Cost awareness
S3 storage and requests can cost a little. Delete the bucket and its files when I no longer need them.

## Self-test
1. What is an S3 object, and what is a bucket?
2. What is a static website?
3. What do the index document and the error document do?
4. Why are the permissions important for a website bucket?
5. Why does my site use HTTP and not HTTPS?
6. Why should a public website bucket hold only the website files?

### Answers
1. An object is a stored file. A bucket is the container that holds objects.
2. A site made only of files the browser runs, with no server code or database.
3. The index document is the page shown for the site address. The error document is shown when a page isn't found.
4. A bucket is private by default, so visitors can only read the files if the permissions allow it.
5. S3 website endpoints only support HTTP. HTTPS needs another service in front, such as CloudFront.
6. Public permissions let anyone read what's in the bucket, so private files shouldn't be there.
