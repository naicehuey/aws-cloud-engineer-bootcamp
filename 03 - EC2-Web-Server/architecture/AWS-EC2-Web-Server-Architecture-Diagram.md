# Project 03 — Architecture

```
 Me (browser)                            Visitor (browser)
      |                                        |
      | EC2 Instance Connect                   | HTTP : port 80
      | (SSH : port 22)                        | (HTTPS : port 443 -> no SSL yet)
      v                                        v
+--------------------------------------------------------+
|  Security group: allows ports 22, 80 and 443           |
|  +--------------------------------------------------+  |
|  |  EC2 instance (t3.micro, 8 GB gp3)               |  |
|  |  Ubuntu Server 24.04 LTS (from an AMI)           |  |
|  |                                                  |  |
|  |  Apache2 web server                              |  |
|  |      |                                           |  |
|  |      v                                           |  |
|  |  /var/www/html/index.html (my HTML page)         |  |
|  +--------------------------------------------------+  |
+--------------------------------------------------------+
                       |
                       v
          Public IPv4 address
        (how visitors reach the server)
```

