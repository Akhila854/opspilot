RUNBOOKS = {
    "payment-api": {
        "database_connection_exhaustion": {
            "title": "Payment API Database Connection Exhaustion",
            "severity": "critical",
            "steps": [
                "Check current database connection usage.",
                "Review application logs for connection timeout errors.",
                "Verify PostgreSQL health and availability.",
                "Check for long-running or leaked database connections.",
                "Review recent deployment changes.",
                "If approved, restart affected application instances.",
            ],
            "requires_human_approval": True,
        }
    }
}


def get_runbook(service: str, incident_type: str) -> dict:
    """Return the approved operational runbook for an incident."""
    return RUNBOOKS.get(service, {}).get(incident_type, {})