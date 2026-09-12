METRICS = {
    "payment-api": {
        "error_rate": 34.0,
        "latency_ms": 2400,
        "requests_per_minute": 1250,
        "database_connections": 100,
        "database_connection_limit": 100,
    },
    "user-service": {
        "error_rate": 8.5,
        "latency_ms": 850,
        "requests_per_minute": 900,
        "database_connections": 42,
        "database_connection_limit": 100,
    },
}


def get_metrics(service: str) -> dict:
    """
    Return current operational metrics for a service.
    """

    return METRICS.get(service, {})
