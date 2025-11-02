# 📖 Chapter: Chapter 5: MCP Clients: Building Integrations
# 📖 Section: 5.7 Advanced Client Patterns

from enum import Enum
from typing import Callable, Optional

class CircuitState(Enum):
    CLOSED = "closed"  # Normal operation
    OPEN = "open"      # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered

class ResilientMCPClient(MCPClient):
    """MCP client with resilience patterns."""
    
    def __init__(self, endpoint: str, transport: str = "stdio"):
        super().__init__(endpoint, transport)
        
        # Circuit breaker state
        self.circuit_state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.circuit_open_duration = 60  # seconds
        self.failure_threshold = 5
        
        # Retry configuration
        self.max_retries = 3
        self.retry_delays = [1, 2, 4]  # Exponential backoff in seconds
    
    def _check_circuit(self):
        """Check circuit breaker state."""
        if self.circuit_state == CircuitState.OPEN:
            # Check if enough time has passed to try again
            if self.last_failure_time:
                elapsed = time.time() - self.last_failure_time
                if elapsed >= self.circuit_open_duration:
                    self.circuit_state = CircuitState.HALF_OPEN
                    self.failure_count = 0
                else:
                    raise RuntimeError("Circuit breaker is OPEN")
        
        elif self.circuit_state == CircuitState.HALF_OPEN:
            # Allow request through, will close or reopen based on result
            pass
    
    def _record_success(self):
        """Record successful request."""
        if self.circuit_state == CircuitState.HALF_OPEN:
            self.circuit_state = CircuitState.CLOSED
            self.failure_count = 0
    
    def _record_failure(self):
        """Record failed request."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.circuit_state = CircuitState.OPEN
    
    def call_tool_with_retry(self, name: str, arguments: Dict) -> Dict:
        """Call tool with automatic retry."""
        self._check_circuit()
        
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                result = self.call_tool(name, arguments)
                self._record_success()
                return result
            
            except (ConnectionError, TimeoutError) as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    delay = self.retry_delays[attempt] if attempt < len(self.retry_delays) else self.retry_delays[-1]
                    time.sleep(delay)
                    continue
                else:
                    self._record_failure()
                    raise
        
        # If we get here, all retries failed
        self._record_failure()
        raise last_exception or RuntimeError("Tool call failed after retries")