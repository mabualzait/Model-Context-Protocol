# 📖 Chapter: Chapter 5: MCP Clients: Building Integrations
# 📖 Section: 5.10 Real-World Client Implementation Example

"""
Production-Ready MCP Client
Complete implementation with error handling, retry logic, caching, and monitoring.
"""

import json
import time
import logging
import uuid
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass
from queue import Queue
from threading import Lock

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ClientConfig:
    """Configuration for MCP client."""
    endpoint: str
    transport: str = "stdio"
    timeout: int = 30
    max_retries: int = 3
    retry_delays: List[int] = None
    cache_ttl: int = 300
    enable_caching: bool = True
    enable_monitoring: bool = True
    
    def __post_init__(self):
        if self.retry_delays is None:
            self.retry_delays = [1, 2, 4]

class ProductionMCPClient:
    """Production-ready MCP client implementation."""
    
    def __init__(self, config: ClientConfig):
        self.config = config
        self.session_id = str(uuid.uuid4())
        self.connected = False
        self.lock = Lock()
        
        # Caching
        self.cache: Dict[str, tuple] = {}
        
        # Metrics
        self.metrics = {
            "requests_total": 0,
            "requests_successful": 0,
            "requests_failed": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "retries_total": 0,
            "avg_latency_ms": 0
        }
        
        # Connection
        self._connection = None
        self._initialize_connection()
    
    def _initialize_connection(self):
        """Initialize connection to MCP server."""
        # In real implementation, establish stdio or HTTP connection
        logger.info(f"Initializing connection to {self.config.endpoint}")
        self._connection = self._create_connection()
    
    def _create_connection(self):
        """Create connection based on transport type."""
        if self.config.transport == "stdio":
            return self._create_stdio_connection()
        elif self.config.transport == "http":
            return self._create_http_connection()
        else:
            raise ValueError(f"Unsupported transport: {self.config.transport}")
    
    def connect(self):
        """Connect to MCP server."""
        with self.lock:
            if self.connected:
                return
            
            try:
                # Send initialize request
                init_request = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {},
                        "clientInfo": {
                            "name": "production-client",
                            "version": "1.0.0"
                        }
                    }
                }
                
                response = self._send_request(init_request)
                
                if response.get("error"):
                    raise RuntimeError(f"Initialize failed: {response['error']}")
                
                # Send initialized notification
                self._send_notification({
                    "jsonrpc": "2.0",
                    "method": "notifications/initialized"
                })
                
                self.connected = True
                logger.info("Connected to MCP server")
            
            except Exception as e:
                logger.error(f"Connection failed: {e}")
                raise
    
    def list_resources(self, use_cache: bool = True) -> List[Dict]:
        """List resources with caching."""
        cache_key = "resources:list"
        
        if use_cache and self.config.enable_caching:
            cached = self._get_cached(cache_key)
            if cached is not None:
                self.metrics["cache_hits"] += 1
                return cached
        
        result = self._call_with_retry("resources/list", {})
        resources = result.get("resources", [])
        
        if use_cache and self.config.enable_caching:
            self._set_cached(cache_key, resources)
            self.metrics["cache_misses"] += 1
        
        return resources
    
    def read_resource(self, uri: str, use_cache: bool = True) -> str:
        """Read resource with caching."""
        cache_key = f"resource:{uri}"
        
        if use_cache and self.config.enable_caching:
            cached = self._get_cached(cache_key)
            if cached is not None:
                self.metrics["cache_hits"] += 1
                return cached
        
        result = self._call_with_retry("resources/read", {"uri": uri})
        contents = result.get("contents", [])
        
        if contents:
            content = contents[0].get("text", "")
            
            if use_cache and self.config.enable_caching:
                self._set_cached(cache_key, content)
                self.metrics["cache_misses"] += 1
            
            return content
        
        raise ValueError(f"No content found for resource: {uri}")
    
    def call_tool(self, name: str, arguments: Dict, cacheable: bool = False) -> Dict:
        """Call tool with optional caching."""
        if cacheable and self.config.enable_caching:
            cache_key = f"tool:{name}:{json.dumps(arguments, sort_keys=True)}"
            cached = self._get_cached(cache_key)
            if cached is not None:
                self.metrics["cache_hits"] += 1
                return cached
        
        result = self._call_with_retry("tools/call", {
            "name": name,
            "arguments": arguments
        })
        
        if cacheable and self.config.enable_caching:
            cache_key = f"tool:{name}:{json.dumps(arguments, sort_keys=True)}"
            self._set_cached(cache_key, result)
            self.metrics["cache_misses"] += 1
        
        return result
    
    def _call_with_retry(self, method: str, params: Dict) -> Dict:
        """Call method with retry logic."""
        last_exception = None
        
        for attempt in range(self.config.max_retries):
            start_time = time.time()
            
            try:
                request = {
                    "jsonrpc": "2.0",
                    "id": self._get_next_id(),
                    "method": method,
                    "params": params
                }
                
                response = self._send_request(request)
                
                if response.get("error"):
                    error = response["error"]
                    error_code = error.get("code", -1)
                    
                    # Check if retryable
                    if error_code in [-32603, -32000] and attempt < self.config.max_retries - 1:
                        # Internal error or MCP error, retry
                        delay = self.config.retry_delays[attempt] if attempt < len(self.config.retry_delays) else self.config.retry_delays[-1]
                        time.sleep(delay)
                        self.metrics["retries_total"] += 1
                        continue
                    else:
                        raise MCPServerError(
                            error.get("message", "Unknown error"),
                            error_code,
                            error.get("data")
                        )
                
                # Record metrics
                duration = (time.time() - start_time) * 1000
                self._record_metric("success", duration)
                
                return response.get("result", {})
            
            except (ConnectionError, TimeoutError) as e:
                last_exception = e
                if attempt < self.config.max_retries - 1:
                    delay = self.config.retry_delays[attempt] if attempt < len(self.config.retry_delays) else self.config.retry_delays[-1]
                    time.sleep(delay)
                    self.metrics["retries_total"] += 1
                    # Try to reconnect
                    self._reconnect()
                    continue
                else:
                    self._record_metric("failure", (time.time() - start_time) * 1000)
                    raise
        
        # All retries failed
        self._record_metric("failure", 0)
        raise last_exception or RuntimeError(f"Call failed after {self.config.max_retries} retries")
    
    def _send_request(self, request: Dict) -> Dict:
        """Send request via connection."""
        # In real implementation, send via stdio or HTTP
        # This is a placeholder
        self.metrics["requests_total"] += 1
        return {}
    
    def _send_notification(self, notification: Dict):
        """Send notification via connection."""
        # In real implementation, send via stdio or HTTP
        pass
    
    def _get_next_id(self) -> int:
        """Get next request ID."""
        # Simple counter for request IDs
        if not hasattr(self, '_request_id_counter'):
            self._request_id_counter = 0
        self._request_id_counter += 1
        return self._request_id_counter
    
    def _get_cached(self, key: str) -> Optional[Any]:
        """Get cached value if not expired."""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.config.cache_ttl:
                return value
            else:
                del self.cache[key]
        return None
    
    def _set_cached(self, key: str, value: Any):
        """Set cached value."""
        self.cache[key] = (value, time.time())
    
    def _record_metric(self, status: str, duration_ms: float):
        """Record metric."""
        if status == "success":
            self.metrics["requests_successful"] += 1
        else:
            self.metrics["requests_failed"] += 1
        
        # Update average latency
        total = self.metrics["requests_total"]
        current_avg = self.metrics["avg_latency_ms"]
        self.metrics["avg_latency_ms"] = (
            (current_avg * (total - 1) + duration_ms) / total
            if total > 0 else duration_ms
        )
    
    def _reconnect(self):
        """Reconnect to server."""
        logger.info("Reconnecting to server...")
        self.connected = False
        self._initialize_connection()
        self.connect()
    
    def get_metrics(self) -> Dict:
        """Get client metrics."""
        return self.metrics.copy()
    
    def disconnect(self):
        """Disconnect from server."""
        with self.lock:
            if self.connected:
                try:
                    shutdown_request = {
                        "jsonrpc": "2.0",
                        "id": self._get_next_id(),
                        "method": "shutdown"
                    }
                    self._send_request(shutdown_request)
                except Exception:
                    pass  # Ignore errors during shutdown
                
                self.connected = False
                logger.info("Disconnected from MCP server")