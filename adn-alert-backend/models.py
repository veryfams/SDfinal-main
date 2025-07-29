# Modelo de tabla para PostgreSQL
CREATE_TABLE_ALERTS = """
CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(255) NOT NULL,
    payload TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL
);
"""