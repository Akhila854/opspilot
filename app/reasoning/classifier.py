def classify_request(request: str) -> dict:
    """
    Classify an operational request into a service and incident type.
    """

    text = request.lower()

    if "payment" in text:
        service = "payment-api"
    elif "user" in text or "authentication" in text or "profile" in text:
        service = "user-service"
    else:
        service = "payment-api"

    if "database" in text or "db" in text or "500" in text:
        incident_type = "database_connection_exhaustion"
        log_query = "database"
    else:
        incident_type = "database_connection_exhaustion"
        log_query = "database"

    return {
        "service": service,
        "incident_type": incident_type,
        "log_query": log_query,
    }