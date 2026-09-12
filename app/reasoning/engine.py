from app.reasoning.schemas import Diagnosis


def diagnose(evidence: dict) -> Diagnosis:
    """
    Analyze collected operational evidence and produce a diagnosis.
    """

    service = evidence.get("service", "")
    incident_type = evidence.get("incident_type", "")
    logs = evidence.get("logs", [])
    metrics = evidence.get("metrics", {})

    database_connections = metrics.get("database_connections", 0)
    database_connection_limit = metrics.get("database_connection_limit", 0)
    error_rate = metrics.get("error_rate", 0)
    latency_ms = metrics.get("latency_ms", 0)

    connection_pool_exhausted = (
        database_connection_limit > 0
        and database_connections >= database_connection_limit
    )

    timeout_errors = [
        log
        for log in logs
        if "connection timeout" in log.get("message", "").lower()
    ]

    if incident_type == "database_connection_exhaustion" and connection_pool_exhausted and timeout_errors:
        return Diagnosis(
            diagnosis="Database connection pool exhaustion",
            severity="critical",
            confidence=0.94,
            evidence=[
                f"Database connections are at {database_connections}/{database_connection_limit}",
                f"{len(timeout_errors)} database connection timeout log(s) found",
                f"Error rate is {error_rate}%",
                f"Latency is {latency_ms} ms",
            ],
            recommended_action="Investigate connection leaks and verify PostgreSQL health",
            requires_human_approval=True,
        )

    if incident_type == "high_api_latency" and latency_ms >= 1000:
        return Diagnosis(
            diagnosis="High API latency",
            severity="high",
            confidence=0.88,
            evidence=[
                f"API latency is {latency_ms} ms",
                f"Error rate is {error_rate}%",
            ],
            recommended_action="Investigate slow dependencies and review recent application changes",
            requires_human_approval=True,
        )

    if incident_type == "authentication_failure" and error_rate >= 5:
        return Diagnosis(
            diagnosis="Authentication service failure",
            severity="high",
            confidence=0.86,
            evidence=[
                f"Authentication-related error rate is {error_rate}%",
                f"API latency is {latency_ms} ms",
            ],
            recommended_action="Review authentication service logs and dependency health",
            requires_human_approval=True,
        )

    return Diagnosis(
        diagnosis="Insufficient evidence to determine root cause",
        severity="medium",
        confidence=0.40,
        evidence=[
            "Available operational evidence does not match a known failure pattern.",
        ],
        recommended_action=f"Collect additional logs and metrics for {service}.",
        requires_human_approval=True,
    )
