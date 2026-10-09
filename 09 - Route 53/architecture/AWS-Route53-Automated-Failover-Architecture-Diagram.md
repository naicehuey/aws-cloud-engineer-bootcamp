			              [ Web Client / User ]
                                               │
                                               ▼
                                      [ Amazon Route 53 ]
                                   (Public Hosted Zone & DNS)
                                               │
                  ┌────────────────────┴────────────────────┐
                  │                                                         │
          (Primary: Healthy)                                      (Secondary: Unhealthy)
                  │                                                         │
                  ▼                                                         ▼
        [ Amazon EC2 Server ]                                      [ Amazon S3 Bucket ]
     (Active Web Application)                                    (Static Maintenance Page)