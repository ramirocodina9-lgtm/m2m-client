"""HTTP client for the M2M High-Ticket endpoints.

This SDK does not execute payments or sign wallet transactions.
"""
from urllib.parse import urlsplit

import requests


class M2MClientError(RuntimeError):
    """A remote service or transport failure."""


class M2MClient:
    def __init__(self, node_url: str, api_key: str, timeout: float = 15):
        parsed = urlsplit(node_url)
        if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
            raise ValueError("node_url must be an HTTPS URL without embedded credentials")
        if not api_key or not api_key.strip():
            raise ValueError("api_key is required")
        if timeout <= 0:
            raise ValueError("timeout must be positive")
        self.node_url = node_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-KEY": api_key,
            "Accept": "application/json",
            "Content-Type": "application/json",
        })

    def _request(self, method: str, path: str, **kwargs):
        try:
            response = self.session.request(
                method, self.node_url + path, timeout=self.timeout,
                allow_redirects=False, **kwargs
            )
        except requests.RequestException as exc:
            raise M2MClientError("M2M service connection failed") from exc
        if response.status_code == 402:
            raise M2MClientError("Payment required (HTTP 402); no payment was made")
        if response.status_code >= 300:
            raise M2MClientError(f"M2M service returned HTTP {response.status_code}")
        try:
            return response.json()
        except ValueError as exc:
            raise M2MClientError("M2M service returned invalid JSON") from exc

    def get_arbitrage_alpha(self):
        return self._request("GET", "/api/v1/highticket/arbitrage")

    def post_risk_audit(self, entidad_id: str, sector: str):
        if not entidad_id or not sector:
            raise ValueError("entidad_id and sector are required")
        return self._request(
            "POST", "/api/v1/highticket/risk-audit",
            json={"entidad_id": entidad_id, "sector": sector},
        )

    def get_qualified_leads(self):
        return self._request("GET", "/api/v1/highticket/qualified-leads")

    def close(self):
        self.session.close()
