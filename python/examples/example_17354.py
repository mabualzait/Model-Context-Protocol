# 📖 Chapter: Chapter 14: MCP and Enterprise Integration
# 📖 Section: 14.1 Connecting to Enterprise Systems

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

class EnterpriseAPIMCP:
    """MCP server for enterprise REST API integration."""
    
    def __init__(self, api_config: Dict):
        self.api_config = api_config
        self.base_url = api_config['base_url']
        self.api_key = api_config.get('api_key')
        self.session = self._create_session()
        self.rate_limiter = RateLimiter(
            calls_per_minute=api_config.get('rate_limit', 60)
        )
    
    def _create_session(self):
        """Create HTTP session with retry strategy."""
        session = requests.Session()
        
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Add authentication headers
        if self.api_key:
            session.headers.update({
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            })
        
        return session
    
    def list_resources(self) -> List[Dict]:
        """List API endpoints as resources."""
        endpoints = self.api_config.get('endpoints', [])
        
        return [
            {
                "uri": f"api://{endpoint['path']}",
                "name": endpoint['name'],
                "description": endpoint.get('description', ''),
                "mimeType": "application/json"
            }
            for endpoint in endpoints
        ]
    
    def read_resource(self, uri: str) -> str:
        """Read resource from API endpoint."""
        if not uri.startswith("api://"):
            raise ValueError(f"Invalid resource URI: {uri}")
        
        path = uri.replace("api://", "")
        url = f"{self.base_url}/{path}"
        
        # Rate limiting
        self.rate_limiter.wait_if_needed()
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise Exception(f"API request failed: {e}")

class RateLimiter:
    """Simple rate limiter for API calls."""
    
    def __init__(self, calls_per_minute: int):
        self.calls_per_minute = calls_per_minute
        self.call_times: List[float] = []
        self.lock = Lock()
    
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded."""
        with self.lock:
            now = time.time()
            
            # Remove calls older than 1 minute
            self.call_times = [t for t in self.call_times if now - t < 60]
            
            if len(self.call_times) >= self.calls_per_minute:
                # Wait until oldest call expires
                oldest = min(self.call_times)
                wait_time = 60 - (now - oldest) + 0.1
                if wait_time > 0:
                    time.sleep(wait_time)
                    # Recalculate after wait
                    now = time.time()
                    self.call_times = [t for t in self.call_times if now - t < 60]
            
            self.call_times.append(now)