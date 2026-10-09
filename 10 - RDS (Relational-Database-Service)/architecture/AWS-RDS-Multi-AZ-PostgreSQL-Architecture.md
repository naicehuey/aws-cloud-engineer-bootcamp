			        [ Internet / User ]
                                        │
                                        ▼
                               [ EC2 Web/App Server ]
                                (Public Subnet - SG)
                                         │
                                         │ (Port 5432 - Private Transit)
                                         ▼
                                 [ Security Group Rule ]
                            (Allows inbound only from EC2 SG)
                                         │
                   ┌───────────────┴───────────────┐
                   │                                           │
        [ Primary RDS Instance ]                   [ Standby RDS Instance ]
         (PostgreSQL - AZ 1)                        (Multi-AZ Sync - AZ 2)