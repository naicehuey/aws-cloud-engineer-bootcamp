                    Internet
                       │
                       ▼
            Application Load Balancer
                       │
                HTTP : Port 80
                       │
                 Target Group
                  /         \
                 ▼           ▼
          EC2 Web Server 1  EC2 Web Server 2
              Apache            Apache