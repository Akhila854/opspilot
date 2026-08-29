from app.tools.logs import search_logs
from app.tools.metrics import get_metrics
from app.tools.services import get_service_info
from app.tools.runbooks import get_runbook


def collect_evidence(
    service: str,
    incident_type: str,
    log_query: str,
) -> dict:
    """
    Collect operational evidence for an investigation.

    This function orchestrates the available operational tools
    and combines their results into a single evidence package.
    """

    logs = search_logs(service, log_query)
    metrics = get_metrics(service)
    service_info = get_service_info(service)
    runbook = get_runbook(service, incident_type)

    return {
        "service": service,
        "logs": logs,
        "metrics": metrics,
        "service_info": service_info,
        "runbook": runbook,
    }