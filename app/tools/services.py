SERVICES = {
    "payment-api": {
        "name": "Payment API",
        "description": "Handles payment processing requests.",
        "dependencies": [
            "postgresql",
            "redis",
            "payment-gateway",
        ],
        "owner": "payments-team",
        "environment": "production",
    },
    "user-service": {
        "name": "User Service",
        "description": "Handles user authentication and profile operations.",
        "dependencies": [
            "postgresql",
            "redis",
        ],
        "owner": "identity-team",
        "environment": "production",
    },
}


def get_service_info(service: str) -> dict:
    """
    Return architectural and ownership information for a service.
    """

    return SERVICES.get(service, {})