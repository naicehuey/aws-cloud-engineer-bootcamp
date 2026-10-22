#!/bin/bash

dnf update -y
dnf install -y httpd

systemctl start httpd
systemctl enable httpd

echo "[PRIMARY ONLINE] Welcome to Huey's Production Application Server" > /var/www/html/index.html
