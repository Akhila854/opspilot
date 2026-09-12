LOGS = [
    {
        "id": "LOG-001",
        "timestamp": "2026-08-23T19:55:21",
        "service": "payment-api",
        "level": "ERROR",
        "message": "Database connection timeout",
    },
    {
        "id": "LOG-002",
        "timestamp": "2026-08-23T19:55:22",
        "service": "payment-api",
        "level": "ERROR",
        "message": "Failed to process payment request",
    },
    {
        "id": "LOG-003",
        "timestamp": "2026-08-23T19:55:23",
        "service": "payment-api",
        "level": "ERROR",
        "message": "Database connection timeout",
    },
    {
        "id": "LOG-004",
        "timestamp": "2026-08-23T19:55:24",
        "service": "payment-api",
        "level": "INFO",
        "message": "Retrying database connection",
    },
    {
        "id": "LOG-005",
        "timestamp": "2026-08-23T19:55:25",
        "service": "payment-api",
        "level": "ERROR",
        "message": "Connection pool exhausted",
    },
    {
        "id": "LOG-006",
        "timestamp": "2026-08-23T19:56:01",
        "service": "payment-api",
        "level": "ERROR",
        "message": "Request timeout after 2400ms",
    },
    {
        "id": "LOG-007",
        "timestamp": "2026-08-23T19:56:02",
        "service": "payment-api",
        "level": "WARN",
        "message": "Upstream dependency response exceeded latency threshold",
    },
    {
        "id": "LOG-008",
        "timestamp": "2026-08-23T19:57:01",
        "service": "user-service",
        "level": "ERROR",
        "message": "Authentication failure for user request",
    },
    {
        "id": "LOG-009",
        "timestamp": "2026-08-23T19:57:02",
        "service": "user-service",
        "level": "ERROR",
        "message": "Authentication service rejected request",
    },
]


def search_logs(service: str, query: str) -> list[dict]:
    """
    Search application logs for a service and text query.
    """

    query_lower = query.lower()

    if not query_lower:
        return [log for log in LOGS if log["service"] == service]

    return [
        log
        for log in LOGS
        if log["service"] == service
        and query_lower in log["message"].lower()
    ]
