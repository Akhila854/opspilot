RUNBOOKS = {
    ("payment-api", "database_connection_exhaustion"): {
        "title": "Database connection pool exhaustion",
        "steps": [
            "Check database connection utilization",
            "Investigate connection leaks",
            "Verify PostgreSQL health",
            "Restart affected workers if approved"
        ],
    },
    ("payment-api", "high_api_latency"): {
        "title": "High API latency",
        "steps": [
            "Check API latency and error rate",
            "Identify slow upstream dependencies",
            "Review recent application changes",
            "Validate dependency health"
        ],
    },
    ("user-service", "authentication_failure"): {
        "title": "Authentication service failure",
        "steps": [
            "Check authentication service logs",
            "Review authentication error rate",
            "Verify authentication dependencies",
            "Review recent authentication changes"
        ],
    },
}


def get_runbook(service: str, incident_type: str) -> dict:
    """Return the operational runbook for a service and incident type."""
    return RUNBOOKS.get((service, incident_type), {})
