def classify_request(request: str) -> dict:
    """
    Classify an operational request into a service and incident type.
    """

    text = request.lower()

    # Identify the affected service.
    if "payment" in text:
        service = "payment-api"
    elif "user" in text or "authentication" in text or "login" in text or "profile" in text:
        service = "user-service"
    else:
        service = "payment-api"

    # Identify the incident pattern.
    if "database" in text or "db" in text or "connection pool" in text:
        incident_type = "database_connection_exhaustion"
        log_query = "database"
    elif "timeout" in text or "latency" in text or "slow" in text:
        incident_type = "high_api_latency"
        log_query = "timeout"
    elif "authentication" in text or "login" in text or "unauthorized" in text:
        incident_type = "authentication_failure"
        log_query = "authentication"
    else:
        incident_type = "unknown"
        log_query = ""

    return {
        "service": service,
        "incident_type": incident_type,
        "log_query": log_query,
    }
