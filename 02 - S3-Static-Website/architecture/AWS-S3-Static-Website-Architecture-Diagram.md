# Project 02 — Architecture

```
              Developer (me)
                    |
                    v
       Website files built locally
   index.html, error.html, style.css,
        script.js, Image-1.png
                    |
                    v  upload
     +-------------------------------+
     |  Amazon S3 bucket             |
     |  kidyadidi-aws-lab-s3-001     |
     |  (files stored as objects)    |
     +-------------------------------+
                    |
                    v
      Static website hosting turned on
        Index document: index.html
        Error document: error.html
     Bucket permissions allow visitors to read
                    |
                    v
            S3 website endpoint
                    |
          +---------+----------+
          |                    |
          v                    v
     Page exists          Page not found
     -> index.html        -> error.html
                             (custom 404 page)
                    |
                    v
           Browser / visitor
```

