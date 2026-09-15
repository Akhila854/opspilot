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

    return METRICS.get(service, {}).copy()


def simulate_remediation(service: str, incident_type: str) -> dict:
    """
    Simulate an operational remediation by updating mock metrics.
    """

    metrics = METRICS.get(service)

    if not metrics:
        raise ValueError(f"Unknown service: {service}")

    if incident_type == "database_connection_exhaustion":
        metrics["database_connections"] = 42
        metrics["error_rate"] = 2.0
        metrics["latency_ms"] = 180

    elif incident_type == "high_api_latency":
        metrics["error_rate"] = 1.5
        metrics["latency_ms"] = 180

    elif incident_type == "authentication_failure":
        metrics["error_rate"] = 1.0
        metrics["latency_ms"] = 220

    else:
        raise ValueError(
            f"No simulated remediation available for incident type: {incident_type}"
        )

    return metrics.copy()

def reset_metrics() -> None:
    """
    Reset simulated metrics to their initial operational state.
    """

    METRICS["payment-api"] = {
        "error_rate": 34.0,
        "latency_ms": 2400,
        "requests_per_minute": 1250,
        "database_connections": 100,
        "database_connection_limit": 100,
    }

    METRICS["user-service"] = {
        "error_rate": 8.5,
        "latency_ms": 850,
        "requests_per_minute": 900,
        "database_connections": 42,
        "database_connection_limit": 100,
    }