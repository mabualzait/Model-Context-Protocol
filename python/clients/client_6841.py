# 📖 Chapter: Chapter 5: MCP Clients: Building Integrations
# 📖 Section: 5.8 Comprehensive Error Handling

class ErrorRecoveryManager:
    """Manage error recovery strategies."""
    
    def __init__(self, client: 'MCPClient'):
        self.client = client
        self.recovery_strategies: Dict[str, Callable] = {
            "connection_error": self._recover_connection,
            "server_error": self._recover_server_error,
            "timeout_error": self._recover_timeout
        }
    
    def recover(self, error_info: Dict, operation: Callable, *args, **kwargs):
        """Attempt to recover from error."""
        error_type = error_info.get("type")
        retryable = error_info.get("retryable", False)
        
        if not retryable:
            raise RuntimeError(f"Non-retryable error: {error_info['message']}")
        
        recovery_strategy = self.recovery_strategies.get(error_type)
        if recovery_strategy:
            return recovery_strategy(operation, *args, **kwargs)
        else:
            # Default: retry operation
            return self._default_retry(operation, *args, **kwargs)
    
    def _recover_connection(self, operation: Callable, *args, **kwargs):
        """Recover from connection error."""
        logger.info("Attempting to reconnect...")
        
        # Reconnect
        self.client.disconnect()
        time.sleep(1)
        self.client.connect()
        
        # Retry operation
        return operation(*args, **kwargs)
    
    def _recover_server_error(self, operation: Callable, *args, **kwargs):
        """Recover from server error."""
        # Check if server is still responsive
        try:
            self.client.list_tools()
            # Server is responsive, retry operation
            time.sleep(0.5)
            return operation(*args, **kwargs)
        except Exception:
            # Server not responsive, reconnect
            return self._recover_connection(operation, *args, **kwargs)
    
    def _recover_timeout(self, operation: Callable, *args, **kwargs):
        """Recover from timeout."""
        # Increase timeout and retry
        original_timeout = self.client.timeout
        self.client.timeout = original_timeout * 2
        
        try:
            return operation(*args, **kwargs)
        finally:
            self.client.timeout = original_timeout
    
    def _default_retry(self, operation: Callable, *args, **kwargs):
        """Default retry strategy."""
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                return operation(*args, **kwargs)
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise