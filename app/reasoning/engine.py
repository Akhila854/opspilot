from app.reasoning.schemas import Diagnosis


def diagnose(evidence: dict) -> Diagnosis:
    """
    Analyze collected operational evidence and produce a diagnosis.
    """

    service = evidence.get("service", "")
    logs = evidence.get("logs", [])
    metrics = evidence.get("metrics", {})
    runbook = evidence.get("runbook", {})

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

    if connection_pool_exhausted and timeout_errors:
        evidence_items = [
            f"Database connections are at "
            f"{database_connections}/{database_connection_limit}",
            f"{len(timeout_errors)} database connection timeout log(s) found",
            f"Error rate is {error_rate}%",
            f"Latency is {latency_ms} ms",
        ]

        return Diagnosis(
            diagnosis="Database connection pool exhaustion",
            severity="critical",
            confidence=0.94,
            evidence=evidence_items,
            recommended_action=(
                "Investigate connection leaks and verify PostgreSQL health"
            ),
            requires_human_approval=True,
        )

    return Diagnosis(
        diagnosis="Insufficient evidence to determine root cause",
        severity="medium",
        confidence=0.40,
        evidence=[
            "Available operational evidence does not match a known failure pattern."
        ],
        recommended_action=(
            f"Collect additional logs and metrics for {service}."
        ),
        requires_human_approval=True,
    )