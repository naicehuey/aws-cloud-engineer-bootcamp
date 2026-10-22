# Project 09 — Architecture

```
                     Browser
                        |
                        v
          +---------------------------+
          | Amazon Route 53           |
          | Public hosted zone        |
          | Failover routing          |
          +------+------------+-------+
                 |            |
      Primary    |            |   Secondary
      (healthy)  |            |   (primary unhealthy)
                 v            v
        +-------------+   +----------------+
        | EC2         |   | S3 website     |
        | Apache      |   | index.html     |
        | port 80     |   | backup page    |
        +------+------+   +----------------+
               ^
               | HTTP :80 /
        +------+-----------------+
        | Route 53 health check  |
        | Primary-EC2-HealthCheck|
        +------------------------+
```

