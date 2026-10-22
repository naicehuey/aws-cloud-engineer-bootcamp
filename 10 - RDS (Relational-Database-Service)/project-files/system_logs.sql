-- Project 10: table, sample rows and query (run inside psql on appdb)

CREATE TABLE system_logs (
    log_id SERIAL PRIMARY KEY,
    service_name VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO system_logs (service_name, status)
VALUES
    ('AuthService', 'HEALTHY'),
    ('PaymentGateway', 'HEALTHY'),
    ('NotificationEngine', 'DEGRADED');

SELECT log_id, service_name, status, created_at
FROM system_logs;
