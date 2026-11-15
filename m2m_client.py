import requests

class M2MClient:
    """Cliente oficial para conectar agentes autónomos y scripts de Python al nodo M2M High-Ticket."""
    
    def __init__(self, node_url: str, api_key: str):
        self.node_url = node_url.rstrip("/")
        self.headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }
        
    def get_arbitrage_alpha(self):
        """Obtiene el feed de oportunidades de arbitraje de alto spread."""
        url = f"{self.node_url}/api/v1/highticket/arbitrage"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        raise Exception(f"Error {response.status_code}: {response.json().get('detail', 'Error desconocido')}")
        
    def post_risk_audit(self, entidad_id: str, sector: str):
        """Realiza una auditoría de risk scoring institucional sobre una contraparte."""
        url = f"{self.node_url}/api/v1/highticket/risk-audit"
        payload = {"entidad_id": entidad_id, "sector": sector}
        response = requests.post(url, json=payload, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        raise Exception(f"Error {response.status_code}: {response.json().get('detail', 'Error desconocido')}")
        
    def get_qualified_leads(self):
        """Extrae leads comerciales cualificados de alta intención."""
        url = f"{self.node_url}/api/v1/highticket/qualified-leads"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        raise Exception(f"Error {response.status_code}: {response.json().get('detail', 'Error desconocido')}")
